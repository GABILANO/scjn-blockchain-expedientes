#!/usr/bin/env python3
"""
Generador de Backend SCJN con Gemini API

Este script genera el backend completo de la base de datos de jurisprudencias
de la SCJN usando Gemini API, con ahorro del 98% vs Manus.

Uso:
    python generate_backend.py
    python generate_backend.py --module models
    python generate_backend.py --all-modules

Requisitos:
    pip install google-generativeai

Autor: Manus Credit Optimizer
Licencia: MIT
"""

import os
import sys
import time
import hashlib
from pathlib import Path
from typing import Optional, Dict, List
from datetime import datetime

try:
    import google.generativeai as genai
except ImportError:
    print("❌ Error: google-generativeai no está instalado")
    print()
    print("Instala con:")
    print("  pip install google-generativeai")
    print()
    sys.exit(1)


class GeminiBackendGenerator:
    """Generador de backend usando Gemini API"""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Inicializa el generador
        
        Args:
            api_key: API key de Gemini (si no se provee, se busca en env)
        """
        self.api_key = api_key or os.getenv('GEMINI_API_KEY')
        if not self.api_key:
            raise ValueError(
                "API key no encontrada.\n"
                "Configura GEMINI_API_KEY en variables de entorno:\n"
                "  export GEMINI_API_KEY=tu_api_key\n\n"
                "Obtén tu API key en:\n"
                "  https://makersuite.google.com/app/apikey"
            )
        
        # Configurar Gemini
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel('gemini-2.0-flash-exp')
        
        # Directorios
        self.base_dir = Path(__file__).parent
        self.prompts_dir = self.base_dir / 'prompts'
        self.backend_dir = self.base_dir / 'backend'
        self.cache_dir = self.base_dir / '.cache'
        
        # Crear directorios
        self.backend_dir.mkdir(exist_ok=True)
        self.cache_dir.mkdir(exist_ok=True)
    
    def generate_with_gemini(
        self,
        prompt: str,
        temperature: float = 0.3,
        max_tokens: int = 16384,
        use_cache: bool = True
    ) -> str:
        """
        Genera código usando Gemini API
        
        Args:
            prompt: Prompt para generar código
            temperature: Temperatura (0-1, menor = más determinista)
            max_tokens: Máximo de tokens a generar
            use_cache: Si usar cache para evitar regenerar
            
        Returns:
            Código generado
        """
        # Verificar cache
        if use_cache:
            prompt_hash = hashlib.md5(prompt.encode()).hexdigest()
            cache_file = self.cache_dir / f"{prompt_hash}.py"
            
            if cache_file.exists():
                print("✅ Usando código desde cache")
                return cache_file.read_text(encoding='utf-8')
        
        # Generar con Gemini
        try:
            response = self.model.generate_content(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    temperature=temperature,
                    max_output_tokens=max_tokens,
                )
            )
            
            code = response.text
            
            # Guardar en cache
            if use_cache:
                cache_file.write_text(code, encoding='utf-8')
            
            return code
        
        except Exception as e:
            raise RuntimeError(f"Error generando código con Gemini: {e}")
    
    def estimate_cost(self, prompt: str) -> Dict[str, float]:
        """
        Estima el costo de generar código
        
        Args:
            prompt: Prompt a usar
            
        Returns:
            Diccionario con estimaciones
        """
        # Estimación aproximada
        tokens_input = len(prompt) // 4
        tokens_output_est = 15000  # Estimado para backend completo
        
        # Precios Gemini 2.0 Flash
        cost_input = tokens_input * 0.000075 / 1000
        cost_output = tokens_output_est * 0.00030 / 1000
        cost_total = cost_input + cost_output
        
        # Equivalente en créditos Manus (1 crédito ≈ $0.001)
        credits_equivalent = int(cost_total * 1000)
        
        return {
            'tokens_input': tokens_input,
            'tokens_output_est': tokens_output_est,
            'cost_input': cost_input,
            'cost_output': cost_output,
            'cost_total': cost_total,
            'credits_equivalent': credits_equivalent,
            'savings_percent': int((1 - credits_equivalent / 2500) * 100)
        }
    
    def load_prompt(self, prompt_file: str = 'prompt_clean.txt') -> str:
        """
        Carga prompt desde archivo
        
        Args:
            prompt_file: Nombre del archivo de prompt
            
        Returns:
            Contenido del prompt
        """
        prompt_path = self.prompts_dir / prompt_file
        
        if not prompt_path.exists():
            raise FileNotFoundError(f"Prompt no encontrado: {prompt_path}")
        
        return prompt_path.read_text(encoding='utf-8')
    
    def generate_full_backend(
        self,
        output_file: str = 'api_scjn_generated.py',
        confirm: bool = True
    ) -> Path:
        """
        Genera el backend completo
        
        Args:
            output_file: Nombre del archivo de salida
            confirm: Si pedir confirmación antes de generar
            
        Returns:
            Path al archivo generado
        """
        print("=" * 60)
        print("🚀 Generador de Backend SCJN con Gemini API")
        print("=" * 60)
        print()
        
        # Cargar prompt
        print("📄 Cargando prompt...")
        prompt = self.load_prompt()
        print(f"✅ Prompt cargado: {len(prompt)} caracteres")
        print()
        
        # Estimar costo
        print("💰 Estimando costo...")
        cost = self.estimate_cost(prompt)
        
        print(f"   Input: ~{cost['tokens_input']} tokens (${cost['cost_input']:.4f})")
        print(f"   Output: ~{cost['tokens_output_est']} tokens (${cost['cost_output']:.4f})")
        print(f"   Total: ${cost['cost_total']:.4f} (~{cost['credits_equivalent']} créditos Manus)")
        print()
        print(f"   vs Manus directo: 2,000-3,000 créditos")
        print(f"   Ahorro estimado: {cost['savings_percent']}%")
        print()
        
        # Confirmar
        if confirm:
            response = input("¿Continuar con la generación? (s/n): ")
            if response.lower() != 's':
                print("❌ Cancelado")
                sys.exit(0)
            print()
        
        # Generar
        print("🤖 Generando código con Gemini API...")
        print("⏳ Esto puede tomar 30-60 segundos...")
        print()
        
        start_time = time.time()
        
        try:
            code = self.generate_with_gemini(prompt)
            
            elapsed = time.time() - start_time
            
            print(f"✅ Código generado en {elapsed:.1f} segundos")
            print(f"📊 Tamaño: {len(code)} caracteres")
            print()
            
            # Guardar
            output_path = self.backend_dir / output_file
            output_path.write_text(code, encoding='utf-8')
            
            print(f"💾 Código guardado en: {output_path}")
            print()
            
            # Estadísticas
            lines = code.count('\n')
            functions = code.count('def ')
            classes = code.count('class ')
            imports = code.count('import ')
            
            print("📊 Estadísticas del código generado:")
            print(f"   Líneas: {lines:,}")
            print(f"   Funciones: {functions}")
            print(f"   Clases: {classes}")
            print(f"   Imports: {imports}")
            print()
            
            # Resumen
            print("=" * 60)
            print("✨ ¡Generación completada exitosamente!")
            print("=" * 60)
            print()
            
            return output_path
        
        except Exception as e:
            print(f"❌ Error durante la generación: {e}")
            print()
            
            if "quota" in str(e).lower():
                print("💡 Sugerencias:")
                print("   1. Espera 15 minutos y reintenta")
                print("   2. Usa tu propia API key de Gemini")
                print("   3. Usa alternativas: GitHub Copilot, Cursor, Windsurf")
                print()
            
            sys.exit(1)
    
    def generate_module(
        self,
        module_name: str,
        output_file: Optional[str] = None
    ) -> Path:
        """
        Genera un módulo específico
        
        Args:
            module_name: Nombre del módulo (models, schemas, auth, etc.)
            output_file: Nombre del archivo de salida (opcional)
            
        Returns:
            Path al archivo generado
        """
        # Prompts por módulo
        module_prompts = {
            'models': """
Genera solo los modelos SQLAlchemy para el backend SCJN.

Incluye:
- User (con CURP/RFC y hashes)
- Jurisprudence (con prescripción)
- VirtualFile (expedientes blockchain)
- FileBlock (bloques de la cadena)
- FileJurisprudence (relaciones)
- ReceivedEmail (emails procesados)
- SATToken (certificados SAT)

Usa SQLAlchemy 2.0, type hints, y docstrings completos.
            """,
            
            'schemas': """
Genera solo los schemas Pydantic para el backend SCJN.

Incluye schemas para:
- User (Create, Update, Response)
- Jurisprudence (Create, Update, Response, Search)
- VirtualFile (Create, Update, Response)
- Auth (Login, Register, Token)

Con validación de CURP/RFC y todos los campos necesarios.
            """,
            
            'auth': """
Genera solo los endpoints de autenticación para el backend SCJN.

Incluye:
- POST /auth/register (con validación CURP/RFC)
- POST /auth/login
- POST /auth/verify-curp
- POST /auth/verify-rfc
- POST /auth/upload-sat-certs
- GET /auth/me
- POST /auth/refresh

Con JWT, validación completa, y manejo de errores.
            """,
            
            'jurisprudencias': """
Genera solo los endpoints de jurisprudencias para el backend SCJN.

Incluye:
- GET /jurisprudencias (con paginación y filtros)
- GET /jurisprudencias/{id}
- GET /jurisprudencias/search
- GET /jurisprudencias/vigentes
- GET /jurisprudencias/por-materia/{materia}
- POST /jurisprudencias/bulk-import
- GET /jurisprudencias/stats

Con validación, caché, y documentación completa.
            """,
            
            'expedientes': """
Genera solo los endpoints de expedientes virtuales para el backend SCJN.

Incluye:
- GET /expedientes
- POST /expedientes (con blockchain)
- GET /expedientes/{id}
- PUT /expedientes/{id} (crea nuevo bloque)
- GET /expedientes/{id}/blockchain
- GET /expedientes/{id}/validar
- POST /expedientes/{id}/vincular-juris
- GET /expedientes/{id}/export-pdf

Con blockchain, validación de integridad, y firma digital.
            """,
            
            'blockchain': """
Genera la lógica completa de blockchain para expedientes SCJN.

Incluye:
- Funciones de hashing SHA-256
- Proof of Work con números primos
- Mining de bloques
- Validación de cadena
- Detección de modificaciones
- Generación de números primos (Miller-Rabin)

Con documentación completa y tests.
            """,
            
            'validators': """
Genera validadores para CURP y RFC mexicanos.

Incluye:
- validate_curp() con dígito verificador
- validate_rfc() con dígito verificador
- validate_curp_rfc_match() para verificar coincidencia
- Regex oficiales
- Validación de fecha de nacimiento
- Validación de entidad federativa

Con tests completos.
            """,
        }
        
        if module_name not in module_prompts:
            raise ValueError(
                f"Módulo '{module_name}' no reconocido.\n"
                f"Módulos disponibles: {', '.join(module_prompts.keys())}"
            )
        
        print(f"🔧 Generando módulo: {module_name}")
        print()
        
        prompt = module_prompts[module_name]
        code = self.generate_with_gemini(prompt, max_tokens=8192)
        
        # Nombre de archivo
        if not output_file:
            output_file = f"{module_name}.py"
        
        output_path = self.backend_dir / output_file
        output_path.write_text(code, encoding='utf-8')
        
        print(f"✅ Módulo '{module_name}' generado: {output_path}")
        print()
        
        return output_path
    
    def generate_all_modules(self) -> List[Path]:
        """
        Genera todos los módulos por separado
        
        Returns:
            Lista de paths a archivos generados
        """
        modules = [
            'models',
            'schemas',
            'validators',
            'blockchain',
            'auth',
            'jurisprudencias',
            'expedientes',
        ]
        
        print("=" * 60)
        print("🚀 Generando todos los módulos por separado")
        print("=" * 60)
        print()
        
        generated_files = []
        
        for i, module in enumerate(modules, 1):
            print(f"[{i}/{len(modules)}] {module}")
            output_path = self.generate_module(module)
            generated_files.append(output_path)
            time.sleep(1)  # Evitar rate limiting
        
        print("=" * 60)
        print("✨ ¡Todos los módulos generados!")
        print("=" * 60)
        print()
        
        return generated_files
    
    def show_next_steps(self, output_path: Path):
        """Muestra próximos pasos después de generar"""
        print("📝 Próximos pasos:")
        print()
        print("1. Revisar el código generado:")
        print(f"   cat {output_path}")
        print()
        print("2. Validar sintaxis:")
        print(f"   python -m py_compile {output_path}")
        print()
        print("3. Dividir en módulos (opcional):")
        print("   python generate_backend.py --all-modules")
        print()
        print("4. Instalar dependencias:")
        print("   pip install -r requirements.txt")
        print()
        print("5. Configurar base de datos:")
        print("   # Editar .env con DATABASE_URL")
        print("   alembic upgrade head")
        print()
        print("6. Ejecutar tests:")
        print("   pytest backend/tests/")
        print()
        print("7. Ejecutar servidor:")
        print("   uvicorn backend.main:app --reload")
        print()


def main():
    """Función principal"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Generador de Backend SCJN con Gemini API',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos de uso:

  # Generar backend completo
  python generate_backend.py

  # Generar módulo específico
  python generate_backend.py --module models
  python generate_backend.py --module auth

  # Generar todos los módulos por separado
  python generate_backend.py --all-modules

  # Sin confirmación (para scripts)
  python generate_backend.py --no-confirm

Configuración:
  export GEMINI_API_KEY=tu_api_key

Obtén tu API key en:
  https://makersuite.google.com/app/apikey
        """
    )
    
    parser.add_argument(
        '--module',
        type=str,
        help='Generar solo un módulo específico'
    )
    
    parser.add_argument(
        '--all-modules',
        action='store_true',
        help='Generar todos los módulos por separado'
    )
    
    parser.add_argument(
        '--output',
        type=str,
        help='Nombre del archivo de salida'
    )
    
    parser.add_argument(
        '--no-confirm',
        action='store_true',
        help='No pedir confirmación'
    )
    
    parser.add_argument(
        '--no-cache',
        action='store_true',
        help='No usar cache'
    )
    
    args = parser.parse_args()
    
    try:
        # Crear generador
        generator = GeminiBackendGenerator()
        
        # Generar todos los módulos
        if args.all_modules:
            generator.generate_all_modules()
            return
        
        # Generar módulo específico
        if args.module:
            output_path = generator.generate_module(
                args.module,
                args.output
            )
            generator.show_next_steps(output_path)
            return
        
        # Generar backend completo
        output_file = args.output or 'api_scjn_generated.py'
        output_path = generator.generate_full_backend(
            output_file,
            confirm=not args.no_confirm
        )
        
        generator.show_next_steps(output_path)
    
    except ValueError as e:
        print(f"❌ Error de configuración: {e}")
        sys.exit(1)
    
    except FileNotFoundError as e:
        print(f"❌ Archivo no encontrado: {e}")
        sys.exit(1)
    
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
