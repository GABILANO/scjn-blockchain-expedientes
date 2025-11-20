# Prompt Estratégico: Backend SCJN Jurisprudencias

**Para usar con Gemini API - Optimizado para máxima calidad y mínimo costo**

---

## 🎯 Instrucciones de Uso

```bash
# Método 1: Con gemini_code_generator.py
python /path/to/gemini_code_generator.py \
  --custom "$(cat prompts/gemini_backend_scjn.md)" \
  --output backend/api_scjn.py

# Método 2: Con API directa
# Copiar el prompt completo de abajo y usar con Gemini API
```

**Costo estimado:** $0.02-0.05 (~20-50 créditos Manus)  
**vs Manus directo:** 2,000-3,000 créditos  
**Ahorro:** 98%

---

## 📋 PROMPT COMPLETO PARA GEMINI API

```
Crea una API REST completa en Python con FastAPI para un sistema de gestión de jurisprudencias de la Suprema Corte de Justicia de la Nación (SCJN) de México.

=== CONTEXTO DEL PROYECTO ===

Este sistema debe permitir:
1. Almacenar y consultar jurisprudencias de la SCJN
2. Autenticar usuarios mediante CURP y RFC (personas físicas y morales)
3. Crear expedientes virtuales personales tipo blockchain
4. Automatizar recepción de correos electrónicos para crear expedientes
5. Generar hashes únicos usando CURP/RFC
6. Usar números primos para identificadores únicos
7. Integrar con datos de RENAPO y SAT
8. Proporcionar fe pública digital de forma anónima

=== ARQUITECTURA TÉCNICA ===

Framework: FastAPI (Python 3.11+)
Base de datos: PostgreSQL con extensión pgcrypto
ORM: SQLAlchemy 2.0
Autenticación: JWT con validación CURP/RFC
Blockchain: Implementación custom con SHA-256
Cache: Redis
Queue: Celery con Redis
Email: IMAP/SMTP con imaplib
Validación: Pydantic v2

=== MODELOS DE BASE DE DATOS ===

1. Usuario (User)
   - id: UUID (primary key)
   - curp: String(18) UNIQUE NOT NULL
   - rfc: String(13) UNIQUE NOT NULL
   - curp_hash: String(64) - SHA-256 del CURP
   - rfc_hash: String(64) - SHA-256 del RFC
   - tipo_persona: Enum('fisica', 'moral')
   - email: String UNIQUE NOT NULL
   - email_personalizado: String UNIQUE - formato: {curp_hash[:8]}@expedientes.scjn.local
   - activo: Boolean DEFAULT True
   - verificado: Boolean DEFAULT False
   - fecha_registro: DateTime
   - ultimo_acceso: DateTime

2. Jurisprudencia (Jurisprudence)
   - id: BigInteger (primary key, número primo)
   - numero_registro: String UNIQUE NOT NULL
   - epoca: String NOT NULL
   - instancia: String NOT NULL
   - tipo: String NOT NULL
   - fuente: String NOT NULL
   - tesis: Text NOT NULL
   - subtesis: Text
   - materia: String NOT NULL
   - fecha_publicacion: Date NOT NULL
   - fecha_resolucion: Date
   - precedente: String
   - prescripcion_vigente: Boolean - calculado según fecha
   - contenido_completo: Text NOT NULL
   - hash_contenido: String(64) - SHA-256 del contenido
   - url_original: String
   - archivos_adjuntos: JSONB
   - metadata: JSONB
   - fecha_scraping: DateTime
   - fecha_actualizacion: DateTime

3. ExpedienteVirtual (VirtualFile)
   - id: BigInteger (primary key, número primo)
   - usuario_id: UUID FK(User.id)
   - numero_expediente: String UNIQUE NOT NULL - formato: EXP-{año}-{primo}
   - tipo_documento: Enum('email', 'adjunto', 'jurisprudencia', 'nota')
   - asunto: String NOT NULL
   - contenido: Text
   - hash_documento: String(64) - SHA-256 del contenido
   - hash_previo: String(64) - Hash del documento anterior (blockchain)
   - timestamp: DateTime NOT NULL
   - firma_digital: String - Firma del hash
   - archivos_adjuntos: JSONB
   - metadata: JSONB
   - validado: Boolean DEFAULT False
   - cadena_custodia: JSONB - Registro de modificaciones

4. BloqueExpediente (FileBlock)
   - id: BigInteger (primary key, número primo)
   - expediente_id: BigInteger FK(VirtualFile.id)
   - numero_bloque: Integer NOT NULL
   - hash_bloque: String(64) NOT NULL
   - hash_anterior: String(64)
   - timestamp: DateTime NOT NULL
   - datos: JSONB NOT NULL
   - nonce: BigInteger - Número primo usado para mining
   - dificultad: Integer DEFAULT 4
   - valido: Boolean DEFAULT True

5. JurisprudenciaExpediente (FileJurisprudence)
   - id: UUID (primary key)
   - expediente_id: BigInteger FK(VirtualFile.id)
   - jurisprudencia_id: BigInteger FK(Jurisprudence.id)
   - relevancia: Float - Score de relevancia
   - notas: Text
   - fecha_vinculacion: DateTime

6. EmailRecibido (ReceivedEmail)
   - id: UUID (primary key)
   - usuario_id: UUID FK(User.id)
   - email_origen: String NOT NULL
   - email_destino: String NOT NULL - email personalizado del usuario
   - asunto: String
   - cuerpo: Text
   - adjuntos: JSONB
   - hash_email: String(64)
   - fecha_recepcion: DateTime
   - procesado: Boolean DEFAULT False
   - expediente_creado_id: BigInteger FK(VirtualFile.id)

7. TokenSAT (SATToken)
   - id: UUID (primary key)
   - usuario_id: UUID FK(User.id)
   - archivo_key: LargeBinary - .key del SAT
   - archivo_cer: LargeBinary - .cer del SAT
   - password: String ENCRYPTED
   - fecha_vencimiento: Date
   - activo: Boolean
   - fecha_carga: DateTime

=== ENDPOINTS REQUERIDOS ===

AUTENTICACIÓN:
POST   /api/auth/register          - Registro con CURP/RFC
POST   /api/auth/login             - Login con CURP/RFC
POST   /api/auth/verify-curp       - Verificar CURP con RENAPO
POST   /api/auth/verify-rfc        - Verificar RFC con SAT
POST   /api/auth/upload-sat-certs  - Subir certificados SAT (.key/.cer)
GET    /api/auth/me                - Datos del usuario actual
POST   /api/auth/refresh           - Refresh token

JURISPRUDENCIAS:
GET    /api/jurisprudencias                    - Listar (paginado, filtros)
GET    /api/jurisprudencias/{id}               - Detalle
GET    /api/jurisprudencias/search             - Búsqueda avanzada
GET    /api/jurisprudencias/vigentes           - Solo vigentes (no prescritas)
GET    /api/jurisprudencias/por-materia/{mat}  - Filtrar por materia
POST   /api/jurisprudencias/bulk-import        - Importar desde scraper
GET    /api/jurisprudencias/stats              - Estadísticas

EXPEDIENTES VIRTUALES:
GET    /api/expedientes                        - Listar expedientes del usuario
POST   /api/expedientes                        - Crear expediente manual
GET    /api/expedientes/{id}                   - Detalle con blockchain
PUT    /api/expedientes/{id}                   - Actualizar (crea nuevo bloque)
DELETE /api/expedientes/{id}                   - Marcar como eliminado (no borra)
GET    /api/expedientes/{id}/blockchain        - Ver cadena completa
GET    /api/expedientes/{id}/validar           - Validar integridad blockchain
POST   /api/expedientes/{id}/vincular-juris    - Vincular jurisprudencia
GET    /api/expedientes/{id}/export-pdf        - Exportar con cadena de custodia

EMAIL AUTOMATION:
POST   /api/email/configure                    - Configurar cuenta IMAP
GET    /api/email/status                       - Estado del procesamiento
POST   /api/email/process-now                  - Forzar procesamiento
GET    /api/email/received                     - Listar emails recibidos
POST   /api/email/create-expediente-from-email - Crear expediente desde email

BLOCKCHAIN:
GET    /api/blockchain/validate-all            - Validar toda la cadena
GET    /api/blockchain/stats                   - Estadísticas blockchain
GET    /api/blockchain/generate-prime          - Generar siguiente número primo
POST   /api/blockchain/mine-block              - Minar nuevo bloque

ADMIN:
GET    /api/admin/users                        - Listar usuarios
GET    /api/admin/stats                        - Estadísticas del sistema
POST   /api/admin/sync-renapo                  - Sincronizar con RENAPO
POST   /api/admin/sync-sat                     - Sincronizar con SAT

=== FUNCIONALIDADES ESPECÍFICAS ===

1. VALIDACIÓN CURP/RFC:
   - Validar formato según estándares oficiales
   - Calcular dígito verificador
   - Verificar coincidencia CURP/RFC para misma persona
   - Validar que CURP corresponda a persona física
   - Validar que RFC de 12 caracteres sea persona moral

2. GENERACIÓN DE NÚMEROS PRIMOS:
   - Usar algoritmo Miller-Rabin para verificar primalidad
   - Generar secuencia de primos para IDs
   - Cache de primos ya generados
   - Función: get_next_prime_id(table_name)

3. BLOCKCHAIN:
   - Cada expediente es una cadena blockchain
   - Hash actual = SHA-256(hash_anterior + contenido + timestamp + nonce)
   - Proof of Work con dificultad ajustable
   - Validación de integridad de toda la cadena
   - Detección de modificaciones

4. PROCESAMIENTO DE EMAILS:
   - Tarea Celery que corre cada 5 minutos
   - Conectar a IMAP del usuario
   - Buscar emails a dirección personalizada
   - Extraer adjuntos
   - Crear expediente automáticamente
   - Vincular jurisprudencias mencionadas
   - Marcar email como procesado

5. HASHING Y SEGURIDAD:
   - CURP/RFC hasheados con SHA-256 + salt
   - Contraseñas con bcrypt
   - Tokens JWT con RS256
   - Certificados SAT encriptados con Fernet
   - Firma digital de documentos con RSA

6. PRESCRIPCIÓN:
   - Calcular automáticamente si jurisprudencia está vigente
   - Reglas: 5 años para civil, 10 para penal, etc.
   - Campo calculado: prescripcion_vigente
   - Endpoint para actualizar prescripciones

7. FE PÚBLICA DIGITAL:
   - Generar certificado de autenticidad
   - Timestamp con servidor NTP
   - Firma con clave privada del sistema
   - QR code con hash para verificación
   - API pública para verificar: /api/public/verify/{hash}

=== REQUISITOS NO FUNCIONALES ===

1. SEGURIDAD:
   - Rate limiting: 100 req/min por IP
   - CORS configurado
   - Headers de seguridad (HSTS, CSP, etc.)
   - Sanitización de inputs
   - Prepared statements (SQLAlchemy ORM)
   - Logs de auditoría

2. PERFORMANCE:
   - Cache con Redis (TTL 1 hora para jurisprudencias)
   - Índices en campos de búsqueda
   - Paginación obligatoria (max 100 items)
   - Lazy loading de relaciones
   - Compresión gzip

3. LOGGING:
   - Formato JSON estructurado
   - Niveles: DEBUG, INFO, WARNING, ERROR
   - Rotación diaria
   - Logs de: autenticación, blockchain, emails, errores

4. DOCUMENTACIÓN:
   - OpenAPI/Swagger automático
   - Ejemplos de requests/responses
   - Descripción de cada endpoint
   - Modelos Pydantic documentados

5. TESTING:
   - Fixtures para datos de prueba
   - Tests de endpoints principales
   - Tests de validación CURP/RFC
   - Tests de blockchain
   - Coverage > 80%

=== ESTRUCTURA DEL CÓDIGO ===

```
backend/
├── main.py                 # Entry point FastAPI
├── config.py               # Configuración y variables de entorno
├── database.py             # Conexión DB y sesiones
├── models/
│   ├── __init__.py
│   ├── user.py            # Modelo Usuario
│   ├── jurisprudence.py   # Modelo Jurisprudencia
│   ├── file.py            # Modelo Expediente
│   ├── blockchain.py      # Modelo Blockchain
│   └── email.py           # Modelo Email
├── schemas/
│   ├── __init__.py
│   ├── user.py            # Pydantic schemas User
│   ├── jurisprudence.py   # Pydantic schemas Jurisprudence
│   ├── file.py            # Pydantic schemas File
│   └── auth.py            # Pydantic schemas Auth
├── api/
│   ├── __init__.py
│   ├── deps.py            # Dependencias (get_db, get_current_user)
│   ├── auth.py            # Endpoints autenticación
│   ├── jurisprudencias.py # Endpoints jurisprudencias
│   ├── expedientes.py     # Endpoints expedientes
│   ├── email.py           # Endpoints email
│   ├── blockchain.py      # Endpoints blockchain
│   └── admin.py           # Endpoints admin
├── core/
│   ├── __init__.py
│   ├── security.py        # JWT, hashing, encryption
│   ├── validators.py      # Validación CURP/RFC
│   ├── primes.py          # Generación números primos
│   ├── blockchain.py      # Lógica blockchain
│   └── email_processor.py # Procesamiento emails
├── tasks/
│   ├── __init__.py
│   ├── celery_app.py      # Configuración Celery
│   └── email_tasks.py     # Tareas asíncronas email
├── utils/
│   ├── __init__.py
│   ├── logging.py         # Configuración logging
│   └── helpers.py         # Funciones auxiliares
└── tests/
    ├── __init__.py
    ├── conftest.py        # Fixtures pytest
    ├── test_auth.py
    ├── test_jurisprudencias.py
    ├── test_expedientes.py
    ├── test_blockchain.py
    └── test_validators.py
```

=== DEPENDENCIAS (requirements.txt) ===

fastapi==0.109.0
uvicorn[standard]==0.27.0
sqlalchemy==2.0.25
psycopg2-binary==2.9.9
alembic==1.13.1
pydantic==2.5.3
pydantic-settings==2.1.0
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
python-multipart==0.0.6
redis==5.0.1
celery==5.3.6
cryptography==42.0.0
python-dateutil==2.8.2
httpx==0.26.0

=== VARIABLES DE ENTORNO (.env) ===

# Database
DATABASE_URL=postgresql://user:pass@localhost:5432/scjn_db

# Redis
REDIS_URL=redis://localhost:6379/0

# JWT
SECRET_KEY=tu_secret_key_super_segura_aqui
ALGORITHM=RS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Email
IMAP_SERVER=imap.gmail.com
IMAP_PORT=993
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587

# Blockchain
BLOCKCHAIN_DIFFICULTY=4
MINING_REWARD=0

# API Keys (opcional)
RENAPO_API_KEY=
SAT_API_KEY=

=== INSTRUCCIONES ADICIONALES ===

1. Usa type hints en todas las funciones
2. Docstrings en formato Google
3. Manejo de errores con HTTPException
4. Validación de datos con Pydantic
5. Transacciones DB con context managers
6. Logs en todas las operaciones críticas
7. Comentarios explicativos en lógica compleja
8. Código limpio y PEP 8
9. Funciones pequeñas y reutilizables
10. Tests con pytest y coverage

=== PRIORIDADES ===

1. CRÍTICO: Autenticación CURP/RFC
2. CRÍTICO: CRUD Jurisprudencias
3. CRÍTICO: Blockchain expedientes
4. IMPORTANTE: Procesamiento emails
5. IMPORTANTE: Validación integridad
6. NORMAL: Admin endpoints
7. NORMAL: Exportación PDF

=== OUTPUT ESPERADO ===

Genera el código completo y funcional de:
1. main.py con configuración FastAPI
2. Todos los modelos SQLAlchemy
3. Todos los schemas Pydantic
4. Todos los endpoints de la API
5. Lógica de blockchain
6. Validadores CURP/RFC
7. Generador de números primos
8. Procesador de emails con Celery
9. Sistema de seguridad completo
10. Tests básicos

El código debe ser production-ready, bien documentado, y seguir mejores prácticas.
```

---

## 📊 Análisis de Costo

**Este prompt generará aproximadamente:**
- 15,000-20,000 tokens de output
- Costo: $0.02-0.05
- Equivalente: 20-50 créditos Manus

**Si se hiciera con Manus directamente:**
- Múltiples iteraciones
- 2,000-3,000 créditos
- **Ahorro: 98%**

---

## 🚀 Cómo Usar Este Prompt

### Opción 1: Con gemini_code_generator.py

```bash
cd /path/to/manus-credit-optimizer

python scripts/gemini_code_generator.py \
  --custom "$(cat /path/to/scjn-blockchain-system/prompts/gemini_backend_scjn.md | sed -n '/^```$/,/^```$/p' | sed '1d;$d')" \
  --output /path/to/scjn-blockchain-system/backend/api_scjn_complete.py \
  --temperature 0.3
```

### Opción 2: Con API Directa

```python
import google.generativeai as genai
from pathlib import Path

genai.configure(api_key="tu_api_key")
model = genai.GenerativeModel('gemini-2.0-flash-exp')

# Leer prompt
prompt = Path("prompts/gemini_backend_scjn.md").read_text()
prompt = prompt.split("```")[1]  # Extraer solo el prompt

# Generar código
response = model.generate_content(
    prompt,
    generation_config=genai.types.GenerationConfig(
        temperature=0.3,  # Más determinista
        max_output_tokens=16384,
    )
)

# Guardar
Path("backend/api_scjn_complete.py").write_text(response.text)
print("✅ Backend generado exitosamente")
```

### Opción 3: Por Partes (Para Proyectos Grandes)

```python
# Generar en múltiples llamadas para mejor calidad

prompts = {
    "models.py": "Genera solo los modelos SQLAlchemy del prompt...",
    "schemas.py": "Genera solo los schemas Pydantic del prompt...",
    "auth.py": "Genera solo los endpoints de autenticación...",
    "jurisprudencias.py": "Genera solo los endpoints de jurisprudencias...",
    # etc.
}

for filename, specific_prompt in prompts.items():
    code = model.generate_content(specific_prompt).text
    Path(f"backend/{filename}").write_text(code)
```

---

## 💡 Tips para Optimizar

1. **Usa temperatura baja (0.2-0.4)** para código más consistente
2. **Genera por módulos** si el proyecto es muy grande
3. **Valida con linters** después de generar (flake8, mypy)
4. **Itera si es necesario** con prompts de refinamiento
5. **Usa cache** para evitar regenerar código idéntico

---

## 🎯 Resultado Esperado

Después de ejecutar este prompt, tendrás:

✅ API REST completa con FastAPI  
✅ 7 modelos de base de datos  
✅ 30+ endpoints documentados  
✅ Sistema de autenticación CURP/RFC  
✅ Blockchain funcional  
✅ Procesamiento de emails  
✅ Generador de números primos  
✅ Sistema de seguridad completo  
✅ Tests básicos  
✅ Documentación OpenAPI  

**Todo en un solo archivo o dividido en módulos según prefieras.**

---

## 📞 Siguiente Paso

Una vez generado el código:

1. Revisar y ajustar según necesidades específicas
2. Ejecutar tests
3. Configurar base de datos
4. Desplegar

**Costo total:** $0.02-0.05  
**vs Manus:** 2,000-3,000 créditos  
**Ahorro:** 98%

---

**¡Prompt listo para generar el backend completo!** 🚀
