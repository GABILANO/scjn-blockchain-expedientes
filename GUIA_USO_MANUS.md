# Guía de Uso con Manus AI

**Sistema de Expedientes Virtuales SCJN**  
**Optimizado para mínimo consumo de créditos**

---

## 🎯 Objetivo

Esta guía explica cómo usar el sistema con **Manus AI** para automatizar la auditoría de la SCJN con el **menor costo posible** en créditos.

---

## 📊 Estrategia de Optimización

### Principio Fundamental

> **Manus solo para navegación web en tiempo real. Todo lo demás se ejecuta localmente.**

### Distribución de Tareas

```
┌─────────────────────────────────────────────────────────┐
│                    TAREA                  │  EJECUTOR   │
├───────────────────────────────────────────┼─────────────┤
│ Navegar a SCJN                            │ Manus       │
│ Extraer HTML de páginas                   │ Manus       │
│ Descargar PDFs                            │ Manus       │
│ ─────────────────────────────────────────────────────── │
│ Parsear HTML                              │ Python local│
│ Calcular hashes SHA-256                   │ Python local│
│ Registrar en blockchain                   │ Python local│
│ Generar informes forenses                 │ Python local│
│ Procesar correos electrónicos             │ Python local│
│ Búsquedas en base de datos                │ Python local│
└─────────────────────────────────────────────────────────┘
```

---

## 🚀 Flujo de Trabajo Optimizado

### Fase 1: Extracción con Manus (ALTO COSTO)

**Objetivo:** Obtener HTML y PDFs de la SCJN

**Prompt para Manus:**

```
Navega a https://www2.scjn.gob.mx/ConsultasTematica/Resultados/-0-0-0-0-2025

Por favor:
1. Guarda el HTML completo de la página en /home/ubuntu/scjn_data/pagina_1.html
2. Identifica cuántas páginas de resultados hay en total
3. Para cada página (1 a N):
   - Guarda el HTML en /home/ubuntu/scjn_data/pagina_X.html
   - NO extraigas datos, solo guarda el HTML
4. Cuando termines, dime cuántas páginas guardaste

NO hagas nada más. Solo guardar los archivos HTML.
```

**Consumo estimado:** 10-20 créditos para todas las páginas

### Fase 2: Procesamiento Local (CERO COSTO)

**Objetivo:** Extraer datos de los HTML guardados

**Comando:**

```bash
cd /home/ubuntu/scjn-blockchain-system/backend
python3 scjn_scraper.py --año 2025 --input /home/ubuntu/scjn_data --no-pdfs
```

**Consumo:** 0 créditos (ejecución local)

### Fase 3: Descarga de PDFs con Manus (MEDIO COSTO)

**Objetivo:** Descargar solo los PDFs necesarios

**Prompt para Manus:**

```
Tengo un archivo JSON en /home/ubuntu/scjn_data/expedientes_2025.json
que contiene URLs de PDFs a descargar.

Por favor:
1. Lee el archivo JSON
2. Para cada URL en el campo "documentos":
   - Descarga el PDF
   - Guárdalo en /home/ubuntu/scjn_data/pdfs/ con el nombre del hash
3. NO proceses los PDFs, solo descárgalos

Usa este script Python para hacerlo más eficiente:

import json
import requests
from pathlib import Path

with open('/home/ubuntu/scjn_data/expedientes_2025.json') as f:
    data = json.load(f)

output_dir = Path('/home/ubuntu/scjn_data/pdfs')
output_dir.mkdir(exist_ok=True)

for exp in data:
    for doc in exp.get('documentos', []):
        url = doc['url']
        filename = f"{doc['hash']}.pdf"
        
        response = requests.get(url, timeout=30)
        (output_dir / filename).write_bytes(response.content)
        
        print(f"✓ {filename}")
```

**Consumo estimado:** 3-7 créditos por PDF

### Fase 4: Procesamiento de PDFs (CERO COSTO)

**Objetivo:** Extraer texto, generar hashes, crear informes

**Comando:**

```bash
cd /home/ubuntu/scjn-blockchain-system/scripts
./generar_cadena_custodia.sh /home/ubuntu/scjn_data/pdfs
```

**Consumo:** 0 créditos (ejecución local)

---

## 💡 Técnicas Avanzadas de Ahorro

### 1. Cache de Páginas HTML

**Problema:** Manus cobra por cada navegación

**Solución:** Guardar HTML localmente y reutilizar

```bash
# Primera vez (con Manus)
manus: "Guarda HTML de SCJN en /cache/scjn_2025.html"

# Siguientes veces (sin Manus)
python3 scjn_scraper.py --input /cache/scjn_2025.html
```

**Ahorro:** 100% en consultas repetidas

### 2. Procesamiento Batch

**Problema:** Manus cobra por cada operación individual

**Solución:** Agrupar operaciones en un solo prompt

```
# ❌ MAL (100 créditos)
Para cada expediente:
  - Navega a URL
  - Descarga PDF
  
# ✅ BIEN (10 créditos)
Descarga todos estos PDFs en un solo script:
[lista de 100 URLs]
```

**Ahorro:** 90%

### 3. Delegación a Scripts Locales

**Problema:** Manus cobra por procesamiento

**Solución:** Manus solo descarga, Python procesa

```python
# Manus ejecuta esto (5 créditos):
import requests
urls = [...]
for url in urls:
    response = requests.get(url)
    with open(f'{hash}.pdf', 'wb') as f:
        f.write(response.content)

# Python local procesa (0 créditos):
for pdf in pdfs:
    text = extract_text(pdf)
    hash = calculate_hash(pdf)
    blockchain.add_block(...)
```

**Ahorro:** 95%

### 4. Uso de APIs Externas

**Problema:** Manus cobra por análisis de texto

**Solución:** Usar Gemini API directamente

```python
# ❌ MAL (50 créditos con Manus)
manus: "Analiza este PDF y extrae información jurídica"

# ✅ BIEN (1-3 créditos con Gemini API)
import google.generativeai as genai
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
model = genai.GenerativeModel('gemini-2.5-flash')
response = model.generate_content(f"Analiza: {text}")
```

**Ahorro:** 94-98%

---

## 📋 Checklist de Optimización

Antes de usar Manus, verifica:

- [ ] ¿Puedo hacer esto con un script local?
- [ ] ¿Puedo usar cache de una ejecución anterior?
- [ ] ¿Puedo agrupar múltiples operaciones?
- [ ] ¿Puedo usar una API externa más barata?
- [ ] ¿Realmente necesito que Manus navegue o puedo usar requests?

Si respondiste **SÍ** a alguna pregunta, **NO uses Manus** para esa tarea.

---

## 🎯 Casos de Uso Específicos

### Caso 1: Primera Auditoría Completa

**Objetivo:** Extraer todos los expedientes de 2025

**Pasos:**

1. **Manus:** Guardar HTML de todas las páginas (10-20 créditos)
2. **Local:** Parsear HTML y extraer metadata (0 créditos)
3. **Manus:** Descargar PDFs (3-7 créditos × N documentos)
4. **Local:** Procesar PDFs y generar blockchain (0 créditos)

**Total:** ~500-1,000 créditos para 100 expedientes

### Caso 2: Actualización Incremental

**Objetivo:** Solo expedientes nuevos desde última ejecución

**Pasos:**

1. **Local:** Verificar última fecha en blockchain (0 créditos)
2. **Manus:** Guardar HTML solo de página 1 (5 créditos)
3. **Local:** Identificar expedientes nuevos (0 créditos)
4. **Manus:** Descargar solo PDFs nuevos (3-7 créditos × N nuevos)
5. **Local:** Procesar y actualizar blockchain (0 créditos)

**Total:** ~50-100 créditos para 10 expedientes nuevos

### Caso 3: Consulta de Expediente Existente

**Objetivo:** Buscar jurisprudencia específica

**Pasos:**

1. **Local:** Buscar en base de datos local (0 créditos)
2. **Local:** Verificar en blockchain (0 créditos)
3. **Local:** Generar informe (0 créditos)

**Total:** 0 créditos

---

## 🔧 Configuración Recomendada

### Variables de Entorno

```bash
# .env
MANUS_MODE=minimal              # Solo navegación esencial
CACHE_ENABLED=true              # Habilitar cache
CACHE_TTL=86400                 # 24 horas
LOCAL_PROCESSING=true           # Procesar localmente
GEMINI_API_KEY=tu_api_key       # Para análisis de texto
```

### Configuración de Manus

```json
{
  "optimization": {
    "cache_html": true,
    "batch_downloads": true,
    "local_processing": true,
    "max_parallel_requests": 3
  },
  "cost_limits": {
    "max_credits_per_task": 1000,
    "alert_threshold": 500
  }
}
```

---

## 📊 Comparación de Costos

### Escenario: 100 Expedientes, 300 PDFs

| Método | Navegación | Descarga | Procesamiento | **Total** |
|--------|-----------|----------|---------------|-----------|
| 100% Manus | 2,000 | 2,100 | 1,500 | **5,600** |
| Híbrido básico | 500 | 2,100 | 0 | **2,600** |
| **Híbrido optimizado** | **20** | **900** | **0** | **920** |
| **Ahorro vs 100% Manus** | **99%** | **57%** | **100%** | **84%** |

---

## 🎓 Mejores Prácticas

### DO ✅

1. **Guardar HTML completo** antes de procesar
2. **Usar cache** para consultas repetidas
3. **Agrupar descargas** en un solo script
4. **Procesar localmente** siempre que sea posible
5. **Verificar blockchain** antes de descargar duplicados

### DON'T ❌

1. **No pedir a Manus** que analice texto (usa Gemini API)
2. **No navegar** página por página (descarga HTML completo)
3. **No procesar** con Manus (usa Python local)
4. **No descargar** PDFs duplicados (verifica hash primero)
5. **No usar Manus** para operaciones que no requieren navegador

---

## 🆘 Solución de Problemas

### Problema: "Manus está consumiendo muchos créditos"

**Diagnóstico:**
```bash
# Ver log de operaciones
cat /var/log/manus_operations.log | grep "credits_used"
```

**Solución:**
1. Identificar operaciones costosas
2. Mover a procesamiento local
3. Habilitar cache
4. Usar batch processing

### Problema: "No puedo acceder a la SCJN"

**Solución:**
1. Usar HTML cacheado si existe
2. Verificar conectividad
3. Usar proxy si es necesario
4. Reintentar con backoff exponencial

### Problema: "Blockchain muy grande"

**Solución:**
1. Archivar bloques antiguos
2. Usar compresión
3. Implementar sharding
4. Exportar a almacenamiento externo

---

## 📞 Soporte

Si tienes dudas sobre optimización de costos:

1. Revisa esta guía completa
2. Consulta [ARQUITECTURA_SISTEMA.md](ARQUITECTURA_SISTEMA.md)
3. Abre un issue en GitHub
4. Contacta al equipo de desarrollo

---

## 🎉 Resumen

**Regla de Oro:**

> Manus solo para lo que **requiere navegador**.  
> Todo lo demás, **Python local**.

**Ahorro esperado:** 70-85% en créditos

**Costo típico:**
- Primera auditoría completa: 500-1,000 créditos
- Actualizaciones incrementales: 50-100 créditos
- Consultas: 0 créditos

---

**¡Feliz automatización con bajo costo!** 🚀
