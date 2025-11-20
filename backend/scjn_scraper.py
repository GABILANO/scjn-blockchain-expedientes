#!/usr/bin/env python3
"""
SCJN Scraper - Sistema de Extracción Masiva de Jurisprudencias
Optimizado para uso con Manus AI con mínimo consumo de créditos
"""

import requests
from bs4 import BeautifulSoup
import json
import hashlib
import time
from datetime import datetime, timedelta
from pathlib import Path
import logging
import sys

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('scjn_scraper.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)


class SCJNScraper:
    """
    Scraper optimizado para SCJN con cache y manejo de errores
    """
    
    def __init__(self, año=2025, output_dir="./data"):
        self.año = año
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        self.base_url = "https://www2.scjn.gob.mx/ConsultasTematica/Resultados"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'es-MX,es;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        })
        
        self.cache_dir = self.output_dir / "cache"
        self.cache_dir.mkdir(exist_ok=True)
        
        self.stats = {
            'expedientes_procesados': 0,
            'documentos_descargados': 0,
            'errores': 0,
            'cache_hits': 0
        }
    
    def get_cache_path(self, url):
        """Genera ruta de cache para una URL"""
        url_hash = hashlib.md5(url.encode()).hexdigest()
        return self.cache_dir / f"{url_hash}.html"
    
    def get_cached_content(self, url, max_age_hours=24):
        """Obtiene contenido del cache si existe y no ha expirado"""
        cache_path = self.get_cache_path(url)
        
        if not cache_path.exists():
            return None
        
        # Verificar edad del cache
        age = time.time() - cache_path.stat().st_mtime
        if age > max_age_hours * 3600:
            logger.debug(f"Cache expirado para {url}")
            return None
        
        logger.debug(f"Cache hit para {url}")
        self.stats['cache_hits'] += 1
        return cache_path.read_text(encoding='utf-8')
    
    def save_to_cache(self, url, content):
        """Guarda contenido en cache"""
        cache_path = self.get_cache_path(url)
        cache_path.write_text(content, encoding='utf-8')
    
    def fetch_page(self, url, use_cache=True):
        """Obtiene contenido de una página con cache"""
        if use_cache:
            cached = self.get_cached_content(url)
            if cached:
                return cached
        
        try:
            logger.info(f"Descargando: {url}")
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            response.encoding = 'utf-8'
            
            content = response.text
            self.save_to_cache(url, content)
            
            # Delay para no saturar el servidor
            time.sleep(1)
            
            return content
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Error descargando {url}: {e}")
            self.stats['errores'] += 1
            return None
    
    def extraer_num_paginas(self, soup):
        """Extrae el número total de páginas de resultados"""
        try:
            # Buscar paginación
            paginacion = soup.find('div', class_='paginacion') or soup.find('ul', class_='pagination')
            
            if not paginacion:
                logger.warning("No se encontró paginación, asumiendo 1 página")
                return 1
            
            # Buscar todos los enlaces de página
            enlaces = paginacion.find_all('a')
            numeros = []
            
            for enlace in enlaces:
                texto = enlace.text.strip()
                if texto.isdigit():
                    numeros.append(int(texto))
            
            if numeros:
                return max(numeros)
            
            # Fallback: contar elementos <li>
            items = paginacion.find_all('li')
            if items:
                return len([i for i in items if i.text.strip().isdigit()])
            
            return 1
            
        except Exception as e:
            logger.error(f"Error extrayendo número de páginas: {e}")
            return 1
    
    def extraer_expedientes_de_pagina(self, soup, año):
        """Extrae expedientes de una página de resultados"""
        expedientes = []
        
        try:
            # Buscar tabla de resultados
            tabla = soup.find('table', class_='resultados') or soup.find('table')
            
            if not tabla:
                logger.warning("No se encontró tabla de resultados")
                return expedientes
            
            # Buscar filas (saltar encabezado)
            filas = tabla.find_all('tr')[1:]
            
            for idx, fila in enumerate(filas):
                try:
                    celdas = fila.find_all('td')
                    
                    if len(celdas) < 4:
                        continue
                    
                    # Extraer datos básicos
                    numero_expediente = celdas[0].text.strip()
                    
                    # Validar formato de expediente
                    if not numero_expediente or '/' not in numero_expediente:
                        continue
                    
                    tipo_asunto = celdas[1].text.strip() if len(celdas) > 1 else ""
                    organo = celdas[2].text.strip() if len(celdas) > 2 else ""
                    ponente = celdas[3].text.strip() if len(celdas) > 3 else ""
                    tema = celdas[4].text.strip() if len(celdas) > 4 else ""
                    organo_origen = celdas[5].text.strip() if len(celdas) > 5 else ""
                    
                    # Extraer enlaces a documentos
                    documentos = []
                    enlaces = celdas[0].find_all('a')
                    
                    for enlace in enlaces:
                        href = enlace.get('href', '')
                        texto = enlace.text.strip()
                        
                        if href and ('pdf' in href.lower() or 'documento' in href.lower()):
                            # Normalizar URL
                            if href.startswith('http'):
                                url_completa = href
                            elif href.startswith('/'):
                                url_completa = f"https://www2.scjn.gob.mx{href}"
                            else:
                                url_completa = f"https://www2.scjn.gob.mx/{href}"
                            
                            documentos.append({
                                'url': url_completa,
                                'tipo': self.identificar_tipo_documento(texto),
                                'texto_enlace': texto
                            })
                    
                    expediente = {
                        'numero_expediente': numero_expediente,
                        'año': año,
                        'tipo_asunto': tipo_asunto,
                        'organo_radicacion': organo,
                        'ministro_ponente': ponente,
                        'tema': tema,
                        'organo_origen': organo_origen,
                        'documentos': documentos,
                        'url_scjn': f"{self.base_url}/-0-0-0-0-{año}",
                        'fecha_extraccion': datetime.now().isoformat(),
                        'hash_expediente': self.generar_hash_expediente(numero_expediente, año)
                    }
                    
                    expedientes.append(expediente)
                    logger.debug(f"Extraído: {numero_expediente}")
                    
                except Exception as e:
                    logger.error(f"Error procesando fila {idx}: {e}")
                    continue
            
        except Exception as e:
            logger.error(f"Error extrayendo expedientes: {e}")
        
        return expedientes
    
    def identificar_tipo_documento(self, texto):
        """Identifica el tipo de documento por el texto del enlace"""
        texto = texto.lower()
        
        if 'engrose' in texto or 'engrose' in texto:
            return 'ENGROSE'
        elif 'sentencia' in texto:
            return 'SENTENCIA'
        elif 'resolución' in texto or 'resolucion' in texto:
            return 'RESOLUCION'
        elif 'acuerdo' in texto:
            return 'ACUERDO'
        elif 'voto' in texto:
            return 'VOTO'
        elif 'proyecto' in texto:
            return 'PROYECTO'
        else:
            return 'PDF'
    
    def generar_hash_expediente(self, numero_expediente, año):
        """Genera hash único para un expediente"""
        data = f"{numero_expediente}_{año}_{datetime.now().date().isoformat()}"
        return hashlib.sha256(data.encode()).hexdigest()
    
    def descargar_documento(self, doc_info, expediente_dir):
        """Descarga un documento PDF"""
        try:
            url = doc_info['url']
            tipo = doc_info['tipo']
            
            logger.info(f"  Descargando {tipo}: {url}")
            
            response = self.session.get(url, timeout=60)
            response.raise_for_status()
            
            # Calcular hash
            file_hash = hashlib.sha256(response.content).hexdigest()
            
            # Generar nombre de archivo
            filename = f"{tipo}_{file_hash[:12]}.pdf"
            filepath = expediente_dir / filename
            
            # Guardar archivo
            filepath.write_bytes(response.content)
            
            # Guardar metadata
            metadata = {
                'url': url,
                'tipo': tipo,
                'hash_sha256': file_hash,
                'tamano_bytes': len(response.content),
                'fecha_descarga': datetime.now().isoformat(),
                'nombre_archivo': filename
            }
            
            metadata_path = expediente_dir / f"{filename}.json"
            metadata_path.write_text(json.dumps(metadata, indent=2, ensure_ascii=False))
            
            self.stats['documentos_descargados'] += 1
            logger.info(f"  ✓ Descargado: {filename} ({len(response.content)} bytes)")
            
            return metadata
            
        except Exception as e:
            logger.error(f"  ✗ Error descargando documento: {e}")
            self.stats['errores'] += 1
            return None
    
    def scrape_año(self, descargar_pdfs=True):
        """
        Extrae todos los expedientes de un año
        """
        logger.info(f"═══════════════════════════════════════════════════")
        logger.info(f"Iniciando scraping para año {self.año}")
        logger.info(f"═══════════════════════════════════════════════════")
        
        # URL inicial
        url_inicial = f"{self.base_url}/-0-0-0-0-{self.año}"
        
        # Obtener primera página
        html = self.fetch_page(url_inicial)
        if not html:
            logger.error("No se pudo obtener la página inicial")
            return []
        
        soup = BeautifulSoup(html, 'html.parser')
        
        # Extraer número de páginas
        num_paginas = self.extraer_num_paginas(soup)
        logger.info(f"Total de páginas encontradas: {num_paginas}")
        
        # Extraer expedientes de todas las páginas
        todos_expedientes = []
        
        for pagina in range(1, num_paginas + 1):
            logger.info(f"Procesando página {pagina}/{num_paginas}...")
            
            if pagina == 1:
                # Ya tenemos el HTML de la primera página
                soup_pagina = soup
            else:
                # Construir URL de la página
                url_pagina = f"{self.base_url}/-0-0-0-{pagina}-{self.año}"
                html_pagina = self.fetch_page(url_pagina)
                
                if not html_pagina:
                    logger.error(f"Error obteniendo página {pagina}")
                    continue
                
                soup_pagina = BeautifulSoup(html_pagina, 'html.parser')
            
            # Extraer expedientes
            expedientes = self.extraer_expedientes_de_pagina(soup_pagina, self.año)
            logger.info(f"  Extraídos {len(expedientes)} expedientes")
            
            todos_expedientes.extend(expedientes)
            self.stats['expedientes_procesados'] += len(expedientes)
        
        logger.info(f"Total de expedientes extraídos: {len(todos_expedientes)}")
        
        # Guardar metadata de expedientes
        metadata_file = self.output_dir / f"expedientes_{self.año}.json"
        metadata_file.write_text(
            json.dumps(todos_expedientes, indent=2, ensure_ascii=False),
            encoding='utf-8'
        )
        logger.info(f"Metadata guardada en: {metadata_file}")
        
        # Descargar PDFs si se solicita
        if descargar_pdfs:
            logger.info("Iniciando descarga de documentos...")
            self.descargar_todos_documentos(todos_expedientes)
        
        # Mostrar estadísticas
        self.mostrar_estadisticas()
        
        return todos_expedientes
    
    def descargar_todos_documentos(self, expedientes):
        """Descarga todos los documentos de los expedientes"""
        documentos_dir = self.output_dir / "documentos"
        documentos_dir.mkdir(exist_ok=True)
        
        for idx, expediente in enumerate(expedientes, 1):
            numero = expediente['numero_expediente']
            logger.info(f"[{idx}/{len(expedientes)}] Procesando expediente: {numero}")
            
            # Crear directorio para el expediente
            exp_dir = documentos_dir / numero.replace('/', '_')
            exp_dir.mkdir(exist_ok=True)
            
            # Guardar metadata del expediente
            exp_metadata_file = exp_dir / "metadata.json"
            exp_metadata_file.write_text(
                json.dumps(expediente, indent=2, ensure_ascii=False),
                encoding='utf-8'
            )
            
            # Descargar documentos
            documentos = expediente.get('documentos', [])
            if not documentos:
                logger.warning(f"  No hay documentos para descargar")
                continue
            
            for doc in documentos:
                self.descargar_documento(doc, exp_dir)
                time.sleep(0.5)  # Delay entre descargas
    
    def mostrar_estadisticas(self):
        """Muestra estadísticas de la ejecución"""
        logger.info("═══════════════════════════════════════════════════")
        logger.info("ESTADÍSTICAS DE EJECUCIÓN")
        logger.info("═══════════════════════════════════════════════════")
        logger.info(f"Expedientes procesados: {self.stats['expedientes_procesados']}")
        logger.info(f"Documentos descargados: {self.stats['documentos_descargados']}")
        logger.info(f"Cache hits: {self.stats['cache_hits']}")
        logger.info(f"Errores: {self.stats['errores']}")
        logger.info("═══════════════════════════════════════════════════")


def main():
    """Función principal"""
    import argparse
    
    parser = argparse.ArgumentParser(description='SCJN Scraper - Extracción masiva de jurisprudencias')
    parser.add_argument('--año', type=int, default=2025, help='Año a extraer (default: 2025)')
    parser.add_argument('--output', type=str, default='./data', help='Directorio de salida')
    parser.add_argument('--no-pdfs', action='store_true', help='No descargar PDFs, solo metadata')
    parser.add_argument('--cache', action='store_true', default=True, help='Usar cache (default: True)')
    
    args = parser.parse_args()
    
    scraper = SCJNScraper(año=args.año, output_dir=args.output)
    expedientes = scraper.scrape_año(descargar_pdfs=not args.no_pdfs)
    
    logger.info(f"Proceso completado. Total de expedientes: {len(expedientes)}")


if __name__ == '__main__':
    main()
