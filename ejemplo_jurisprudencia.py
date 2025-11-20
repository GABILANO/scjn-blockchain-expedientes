#!/usr/bin/env python3
"""
Script de Ejemplo: Expediente Virtual con Jurisprudencia SCJN

Demuestra el uso completo del módulo ExpedienteBlockchain para:
1. Crear un expediente virtual
2. Agregar jurisprudencias de la SCJN
3. Vincular documentos legales
4. Exportar para validez legal

Caso de uso: Demanda de Amparo con jurisprudencias vinculadas

Autor: Manus Credit Optimizer
Licencia: MIT
"""

import sys
import json
from pathlib import Path
from datetime import datetime

# Importar módulo blockchain
sys.path.insert(0, str(Path(__file__).parent / 'backend'))
from blockchain_complete import ExpedienteBlockchain


def print_separator(title: str = ""):
    """Imprime separador visual"""
    if title:
        print(f"\n{'=' * 60}")
        print(f"  {title}")
        print(f"{'=' * 60}\n")
    else:
        print(f"{'=' * 60}\n")


def crear_expediente_amparo():
    """
    Crea un expediente virtual completo de amparo con jurisprudencias
    
    Caso: Demanda de Amparo Indirecto por violación al debido proceso
    """
    
    print_separator("SISTEMA DE EXPEDIENTES VIRTUALES SCJN")
    print("Creando expediente de amparo con jurisprudencias vinculadas...")
    print()
    
    # =========================================================================
    # PASO 1: Crear expediente virtual
    # =========================================================================
    
    print("📁 PASO 1: Creando expediente virtual")
    print("-" * 60)
    
    # Crear blockchain con dificultad moderada
    blockchain = ExpedienteBlockchain(difficulty=3)
    
    print(f"✅ Expediente creado exitosamente")
    print(f"   ID del expediente: {blockchain.expediente_id} (número primo)")
    print(f"   Dificultad PoW: {blockchain.difficulty}")
    print(f"   Bloques iniciales: {len(blockchain.chain)}")
    print()
    
    # =========================================================================
    # PASO 2: Agregar demanda inicial
    # =========================================================================
    
    print("📄 PASO 2: Agregando demanda inicial")
    print("-" * 60)
    
    demanda_data = {
        "tipo": "documento_legal",
        "categoria": "demanda",
        "titulo": "Demanda de Amparo Indirecto",
        "numero_expediente": "A.I. 234/2025",
        "quejoso": {
            "nombre": "Juan Pérez García",
            "curp": "PEGJ850427HDFRNN09",
            "domicilio": "Ciudad de México"
        },
        "autoridad_responsable": "Juez Tercero de Distrito en Materia Civil",
        "acto_reclamado": "Sentencia definitiva que viola el debido proceso",
        "derechos_violados": [
            "Derecho al debido proceso",
            "Derecho de audiencia",
            "Garantía de legalidad"
        ],
        "fecha_presentacion": "2025-11-20",
        "abogado": {
            "nombre": "Lic. María González López",
            "cedula": "1234567",
            "domicilio_profesional": "Av. Reforma 123, CDMX"
        },
        "timestamp": datetime.utcnow().isoformat()
    }
    
    bloque_demanda = blockchain.add_block(demanda_data)
    
    print(f"✅ Demanda agregada al expediente")
    print(f"   Block ID: {bloque_demanda.block_id} (primo)")
    print(f"   Hash: {bloque_demanda.hash[:32]}...")
    print(f"   Nonce: {bloque_demanda.nonce} (no primo)")
    print()
    
    # =========================================================================
    # PASO 3: Vincular jurisprudencia 1 - Debido Proceso
    # =========================================================================
    
    print("⚖️  PASO 3: Vinculando jurisprudencia sobre debido proceso")
    print("-" * 60)
    
    jurisprudencia_1 = {
        "tipo": "jurisprudencia",
        "numero_registro": "2023456",
        "epoca": "Décima Época",
        "instancia": "Primera Sala",
        "tipo_tesis": "Jurisprudencia",
        "fuente": "Semanario Judicial de la Federación",
        "tomo": "Libro XXV, Octubre de 2023",
        "pagina": "1234",
        "tesis": "DEBIDO PROCESO. ALCANCE Y CONTENIDO DEL DERECHO FUNDAMENTAL",
        "subtesis": (
            "El derecho al debido proceso comprende el conjunto de requisitos "
            "que deben observarse en las instancias procesales, a fin de que "
            "las personas estén en condiciones de defender adecuadamente sus "
            "derechos ante cualquier acto del Estado que pueda afectarlos."
        ),
        "texto_completo": (
            "El derecho fundamental al debido proceso legal comprende una serie "
            "de elementos que deben observarse en todo procedimiento jurisdiccional, "
            "entre los que destacan: 1) Notificación del inicio del procedimiento; "
            "2) Oportunidad de ofrecer y desahogar pruebas; 3) Oportunidad de alegar; "
            "4) Dictado de una resolución que dirima las cuestiones debatidas; "
            "5) Posibilidad de impugnar la resolución."
        ),
        "precedentes": [
            "Amparo directo 28/2022",
            "Amparo directo 45/2023"
        ],
        "votos": {
            "unanimidad": True,
            "ministros": 5
        },
        "relevancia_caso": 0.98,
        "aplicabilidad": "Directa al acto reclamado",
        "vinculado_por": "Sistema automático de IA",
        "fecha_vinculacion": datetime.utcnow().isoformat(),
        "url_scjn": "https://sjf.scjn.gob.mx/SJFSem/Paginas/DetalleGeneralV2.aspx?ID=2023456",
        "timestamp": datetime.utcnow().isoformat()
    }
    
    bloque_juris_1 = blockchain.add_block(jurisprudencia_1)
    
    print(f"✅ Jurisprudencia vinculada al expediente")
    print(f"   Registro: {jurisprudencia_1['numero_registro']}")
    print(f"   Tesis: {jurisprudencia_1['tesis']}")
    print(f"   Relevancia: {jurisprudencia_1['relevancia_caso']*100}%")
    print(f"   Block ID: {bloque_juris_1.block_id} (primo)")
    print(f"   Hash: {bloque_juris_1.hash[:32]}...")
    print()
    
    # =========================================================================
    # PASO 4: Vincular jurisprudencia 2 - Derecho de Audiencia
    # =========================================================================
    
    print("⚖️  PASO 4: Vinculando jurisprudencia sobre derecho de audiencia")
    print("-" * 60)
    
    jurisprudencia_2 = {
        "tipo": "jurisprudencia",
        "numero_registro": "2023789",
        "epoca": "Décima Época",
        "instancia": "Pleno",
        "tipo_tesis": "Jurisprudencia",
        "fuente": "Semanario Judicial de la Federación",
        "tomo": "Libro XXIV, Septiembre de 2023",
        "pagina": "567",
        "tesis": "DERECHO DE AUDIENCIA. SU CONTENIDO Y ALCANCES",
        "subtesis": (
            "El derecho de audiencia previsto en el artículo 14 constitucional "
            "consiste en otorgar al gobernado la oportunidad de defensa previamente "
            "al acto privativo de la vida, libertad, propiedad, posesiones o derechos."
        ),
        "texto_completo": (
            "El derecho de audiencia garantiza que nadie puede ser privado de sus "
            "derechos sin que previamente sea oído y vencido en juicio. Este derecho "
            "fundamental implica: 1) Conocimiento del procedimiento; 2) Oportunidad "
            "de ofrecer pruebas; 3) Oportunidad de formular alegatos; 4) Dictado de "
            "resolución fundada y motivada."
        ),
        "precedentes": [
            "Amparo en revisión 123/2022",
            "Contradicción de tesis 56/2023"
        ],
        "votos": {
            "unanimidad": False,
            "ministros": 11,
            "mayoria": 9,
            "minoria": 2
        },
        "relevancia_caso": 0.95,
        "aplicabilidad": "Directa - Violación al derecho de audiencia",
        "vinculado_por": "Sistema automático de IA",
        "fecha_vinculacion": datetime.utcnow().isoformat(),
        "url_scjn": "https://sjf.scjn.gob.mx/SJFSem/Paginas/DetalleGeneralV2.aspx?ID=2023789",
        "timestamp": datetime.utcnow().isoformat()
    }
    
    bloque_juris_2 = blockchain.add_block(jurisprudencia_2)
    
    print(f"✅ Jurisprudencia vinculada al expediente")
    print(f"   Registro: {jurisprudencia_2['numero_registro']}")
    print(f"   Tesis: {jurisprudencia_2['tesis']}")
    print(f"   Relevancia: {jurisprudencia_2['relevancia_caso']*100}%")
    print(f"   Block ID: {bloque_juris_2.block_id} (primo)")
    print(f"   Hash: {bloque_juris_2.hash[:32]}...")
    print()
    
    # =========================================================================
    # PASO 5: Agregar pruebas documentales
    # =========================================================================
    
    print("📎 PASO 5: Agregando pruebas documentales")
    print("-" * 60)
    
    pruebas_data = {
        "tipo": "pruebas",
        "categoria": "documentales",
        "pruebas": [
            {
                "numero": 1,
                "descripcion": "Copia certificada de la sentencia reclamada",
                "fecha_emision": "2025-10-15",
                "autoridad_emisora": "Juez Tercero de Distrito",
                "hash_documento": "a1b2c3d4e5f6...",
                "formato": "PDF",
                "paginas": 25
            },
            {
                "numero": 2,
                "descripcion": "Constancia de notificación de la sentencia",
                "fecha_emision": "2025-10-20",
                "autoridad_emisora": "Actuario Judicial",
                "hash_documento": "f6e5d4c3b2a1...",
                "formato": "PDF",
                "paginas": 3
            },
            {
                "numero": 3,
                "descripcion": "Escrito de alegatos presentado en primera instancia",
                "fecha_emision": "2025-09-10",
                "autoridad_emisora": "Quejoso",
                "hash_documento": "1a2b3c4d5e6f...",
                "formato": "PDF",
                "paginas": 15
            }
        ],
        "total_pruebas": 3,
        "ofrecidas_por": "Quejoso",
        "fecha_ofrecimiento": "2025-11-20",
        "timestamp": datetime.utcnow().isoformat()
    }
    
    bloque_pruebas = blockchain.add_block(pruebas_data)
    
    print(f"✅ Pruebas agregadas al expediente")
    print(f"   Total de pruebas: {pruebas_data['total_pruebas']}")
    print(f"   Block ID: {bloque_pruebas.block_id} (primo)")
    print(f"   Hash: {bloque_pruebas.hash[:32]}...")
    print()
    
    # =========================================================================
    # PASO 6: Agregar resolución (simulada)
    # =========================================================================
    
    print("📋 PASO 6: Agregando resolución del amparo")
    print("-" * 60)
    
    resolucion_data = {
        "tipo": "resolucion",
        "categoria": "sentencia_amparo",
        "numero_expediente": "A.I. 234/2025",
        "sentido": "SE CONCEDE EL AMPARO",
        "sintesis": (
            "Se concede el amparo solicitado para el efecto de que la autoridad "
            "responsable deje insubsistente la sentencia reclamada y dicte una nueva "
            "en la que respete el derecho al debido proceso y derecho de audiencia "
            "del quejoso, conforme a las jurisprudencias aplicables."
        ),
        "consideraciones": [
            "El acto reclamado viola el derecho al debido proceso",
            "No se respetó el derecho de audiencia del quejoso",
            "Las jurisprudencias 2023456 y 2023789 son aplicables al caso",
            "Procede conceder el amparo para efectos"
        ],
        "efectos": (
            "La autoridad responsable deberá dictar nueva sentencia en la que "
            "otorgue al quejoso la oportunidad de ofrecer pruebas y formular "
            "alegatos, respetando plenamente su derecho de audiencia."
        ),
        "magistrado_ponente": "Mtro. Carlos Ramírez Sánchez",
        "fecha_resolucion": "2025-12-15",
        "fecha_notificacion": "2025-12-20",
        "definitiva": True,
        "ejecutoriada": False,
        "timestamp": datetime.utcnow().isoformat()
    }
    
    bloque_resolucion = blockchain.add_block(resolucion_data)
    
    print(f"✅ Resolución agregada al expediente")
    print(f"   Sentido: {resolucion_data['sentido']}")
    print(f"   Magistrado ponente: {resolucion_data['magistrado_ponente']}")
    print(f"   Block ID: {bloque_resolucion.block_id} (primo)")
    print(f"   Hash: {bloque_resolucion.hash[:32]}...")
    print()
    
    # =========================================================================
    # PASO 7: Validar integridad de la cadena
    # =========================================================================
    
    print_separator("VALIDACIÓN DE INTEGRIDAD")
    
    print("🔍 Validando integridad de la blockchain...")
    print()
    
    is_valid, errors = blockchain.validate_chain()
    
    if is_valid:
        print("✅ BLOCKCHAIN VÁLIDA")
        print("   Todos los bloques tienen integridad verificada")
        print("   Todos los enlaces son correctos")
        print("   Todos los block IDs son números primos")
        print("   Todos los nonces son números no primos")
        print("   Proof of Work válido en todos los bloques")
    else:
        print("❌ BLOCKCHAIN INVÁLIDA")
        print("   Errores encontrados:")
        for error in errors:
            print(f"   - {error}")
    
    print()
    
    # =========================================================================
    # PASO 8: Mostrar resumen del expediente
    # =========================================================================
    
    print_separator("RESUMEN DEL EXPEDIENTE")
    
    summary = blockchain.get_chain_summary()
    
    print(f"📊 Estadísticas del expediente:")
    print(f"   Expediente ID: {summary['expediente_id']} (primo: {summary['expediente_id_is_prime']})")
    print(f"   Total de bloques: {summary['total_blocks']}")
    print(f"   Dificultad PoW: {summary['difficulty']}")
    print(f"   Blockchain válida: {summary['is_valid']}")
    print()
    
    print(f"📋 Secuencia de bloques (IDs primos):")
    for i, block_id in enumerate(summary['block_ids']):
        block = blockchain.get_block(block_id)
        tipo = block.data.get('tipo', 'desconocido')
        print(f"   {i+1}. Block ID: {block_id:>3} (primo) - Tipo: {tipo}")
    print()
    
    print(f"🔢 Nonces utilizados (no primos):")
    for i, nonce in enumerate(summary['nonces_used'], 1):
        print(f"   {i}. Nonce: {nonce:>5} (no primo)")
    print()
    
    print(f"🔐 Hashes de la cadena:")
    print(f"   Primer bloque: {summary['first_block_hash'][:32]}...")
    print(f"   Último bloque: {summary['last_block_hash'][:32]}...")
    print()
    
    # =========================================================================
    # PASO 9: Exportar para validez legal
    # =========================================================================
    
    print_separator("EXPORTACIÓN PARA VALIDEZ LEGAL")
    
    print("⚖️  Generando exportación con validez legal...")
    print()
    
    legal_export = blockchain.export_for_legal_proof()
    
    print(f"✅ Exportación generada exitosamente")
    print()
    print(f"📄 Información legal:")
    print(f"   Tipo de documento: {legal_export['tipo_documento']}")
    print(f"   Normas aplicables:")
    for norma in legal_export['normas_aplicables']:
        print(f"      - {norma}")
    print(f"   Cadena válida: {legal_export['cadena_valida']}")
    print(f"   Total de bloques: {legal_export['total_bloques']}")
    print(f"   Fecha de creación: {legal_export['fecha_creacion']}")
    print(f"   Última actualización: {legal_export['fecha_ultimo_bloque']}")
    print(f"   Firma digital: {legal_export['firma_digital'][:32]}...")
    print()
    
    # =========================================================================
    # PASO 10: Guardar exportaciones
    # =========================================================================
    
    print_separator("GUARDANDO ARCHIVOS")
    
    # Crear directorio de salida
    output_dir = Path(__file__).parent / 'output'
    output_dir.mkdir(exist_ok=True)
    
    # Guardar exportación legal (JSON)
    legal_file = output_dir / f'expediente_{blockchain.expediente_id}_legal.json'
    with open(legal_file, 'w', encoding='utf-8') as f:
        json.dump(legal_export, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Exportación legal guardada:")
    print(f"   {legal_file}")
    print()
    
    # Guardar blockchain completa (JSON)
    blockchain_file = output_dir / f'expediente_{blockchain.expediente_id}_blockchain.json'
    with open(blockchain_file, 'w', encoding='utf-8') as f:
        f.write(blockchain.export_to_json())
    
    print(f"✅ Blockchain completa guardada:")
    print(f"   {blockchain_file}")
    print()
    
    # Guardar resumen (texto)
    resumen_file = output_dir / f'expediente_{blockchain.expediente_id}_resumen.txt'
    with open(resumen_file, 'w', encoding='utf-8') as f:
        f.write("=" * 60 + "\n")
        f.write("RESUMEN DEL EXPEDIENTE VIRTUAL\n")
        f.write("=" * 60 + "\n\n")
        f.write(f"Expediente ID: {blockchain.expediente_id}\n")
        f.write(f"Total de bloques: {len(blockchain.chain)}\n")
        f.write(f"Blockchain válida: {is_valid}\n\n")
        f.write("BLOQUES:\n")
        f.write("-" * 60 + "\n")
        for i, block in enumerate(blockchain.chain):
            f.write(f"\nBloque {i+1}:\n")
            f.write(f"  Block ID: {block.block_id} (primo)\n")
            f.write(f"  Tipo: {block.data.get('tipo', 'N/A')}\n")
            f.write(f"  Hash: {block.hash}\n")
            f.write(f"  Nonce: {block.nonce} (no primo)\n")
            if 'tesis' in block.data:
                f.write(f"  Tesis: {block.data['tesis']}\n")
            if 'titulo' in block.data:
                f.write(f"  Título: {block.data['titulo']}\n")
    
    print(f"✅ Resumen guardado:")
    print(f"   {resumen_file}")
    print()
    
    # =========================================================================
    # FINALIZACIÓN
    # =========================================================================
    
    print_separator("PROCESO COMPLETADO")
    
    print("✨ Expediente virtual creado exitosamente")
    print()
    print("📁 Archivos generados:")
    print(f"   1. {legal_file.name}")
    print(f"   2. {blockchain_file.name}")
    print(f"   3. {resumen_file.name}")
    print()
    print("⚖️  El expediente tiene validez legal según:")
    print("   - NOM-151-SCFI-2016 (Preservación de mensajes de datos)")
    print("   - CNPP Art. 227 (Cadena de custodia digital)")
    print("   - CFPC Art. 210-A (Validez probatoria)")
    print()
    print("🔐 Características de seguridad:")
    print("   ✅ IDs únicos con números primos")
    print("   ✅ Mining eficiente con números no primos")
    print("   ✅ Cadena de custodia verificable")
    print("   ✅ Inmutabilidad garantizada")
    print("   ✅ Trazabilidad completa")
    print()
    
    return blockchain, legal_export


def main():
    """Función principal"""
    try:
        blockchain, legal_export = crear_expediente_amparo()
        
        print("=" * 60)
        print("Para verificar el expediente:")
        print("=" * 60)
        print()
        print("# Ver archivos generados:")
        print("ls -lh output/")
        print()
        print("# Ver exportación legal:")
        print(f"cat output/expediente_{blockchain.expediente_id}_legal.json")
        print()
        print("# Ver blockchain completa:")
        print(f"cat output/expediente_{blockchain.expediente_id}_blockchain.json")
        print()
        print("# Ver resumen:")
        print(f"cat output/expediente_{blockchain.expediente_id}_resumen.txt")
        print()
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
