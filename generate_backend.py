#!/usr/bin/env python3
"""
Script para generar el backend completo de SCJN usando Gemini API

Uso:
    python generate_backend.py

Requiere:
    - GEMINI_API_KEY en variables de entorno
    - pip install google-generativeai
"""

import os
import sys
from pathlib import Path
import google.generativeai as genai


def main():
    # Verificar API key
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key:
        print("❌ Error: GEMINI_API_KEY no configurada")
        print()
        print("Configura tu API key:")
        print("  export GEMINI_API_KEY=tu_api_key")
        print()
        print("Obtén tu API key en:")
        print("  https://makersuite.google.com/app/apikey")
        sys.exit(1)
    
    print("=" * 60)
    print("🚀 Generador de Backend SCJN con Gemini API")
    print("=" * 60)
    print()
    
    # Configurar Gemini
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-2.0-flash-exp')
    
    # Leer prompt
    prompt_file = Path(__file__).parent / 'prompts' / 'prompt_clean.txt'
    
    if not prompt_file.exists():
        print(f"❌ Error: {prompt_file} no encontrado")
        sys.exit(1)
    
    print(f"📄 Leyendo prompt desde: {prompt_file}")
    prompt = prompt_file.read_text(encoding='utf-8')
    
    print(f"📊 Tamaño del prompt: {len(prompt)} caracteres")
    print()
    
    # Estimar costo
    tokens_input = len(prompt) // 4  # Aproximación
    tokens_output_est = 15000  # Estimado
    cost_input = tokens_input * 0.000075 / 1000
    cost_output = tokens_output_est * 0.00030 / 1000
    cost_total = cost_input + cost_output
    
    print(f"💰 Costo estimado:")
    print(f"   Input: ~{tokens_input} tokens (${cost_input:.4f})")
    print(f"   Output: ~{tokens_output_est} tokens (${cost_output:.4f})")
    print(f"   Total: ${cost_total:.4f} (~{int(cost_total * 1000)} créditos Manus)")
    print()
    
    # Confirmar
    response = input("¿Continuar con la generación? (s/n): ")
    if response.lower() != 's':
        print("❌ Cancelado")
        sys.exit(0)
    
    print()
    print("🤖 Generando código con Gemini API...")
    print("⏳ Esto puede tomar 30-60 segundos...")
    print()
    
    try:
        # Generar código
        response = model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(
                temperature=0.3,  # Más determinista para código
                max_output_tokens=16384,
            )
        )
        
        code = response.text
        
        print("✅ Código generado exitosamente")
        print(f"📊 Tamaño: {len(code)} caracteres")
        print()
        
        # Guardar código
        output_file = Path(__file__).parent / 'backend' / 'api_scjn_generated.py'
        output_file.parent.mkdir(parents=True, exist_ok=True)
        output_file.write_text(code, encoding='utf-8')
        
        print(f"💾 Código guardado en: {output_file}")
        print()
        
        # Estadísticas
        lines = code.count('\n')
        functions = code.count('def ')
        classes = code.count('class ')
        
        print("📊 Estadísticas del código generado:")
        print(f"   Líneas: {lines}")
        print(f"   Funciones: {functions}")
        print(f"   Clases: {classes}")
        print()
        
        # Costo real
        try:
            tokens_used = response.usage_metadata.total_token_count
            cost_real = (tokens_used * 0.000075) / 1000
            print(f"💰 Costo real: ${cost_real:.4f} (~{int(cost_real * 1000)} créditos Manus)")
            print(f"   vs Manus directo: 2,000-3,000 créditos")
            print(f"   Ahorro: ~{int((1 - cost_real * 1000 / 2500) * 100)}%")
        except:
            pass
        
        print()
        print("=" * 60)
        print("✨ ¡Generación completada exitosamente!")
        print("=" * 60)
        print()
        print("📝 Próximos pasos:")
        print("   1. Revisar el código generado")
        print("   2. Dividir en módulos si es necesario")
        print("   3. Ejecutar tests")
        print("   4. Configurar base de datos")
        print("   5. Desplegar")
        print()
        
    except Exception as e:
        print(f"❌ Error durante la generación: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
