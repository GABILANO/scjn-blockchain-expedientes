# Prompts Estratégicos para GitHub Copilot

**Sistema de Expedientes Virtuales SCJN**  
**Optimización: Ahorro de créditos Manus mediante GitHub Copilot**

---

## 🎯 Estrategia de Ejecución

### Principio Fundamental

> **Usa GitHub Copilot para generar código. Usa Manus solo para validar y ejecutar.**

### Flujo de Trabajo Optimizado

```
1. Abrir repositorio en GitHub
2. Activar GitHub Copilot
3. Copiar prompt estratégico
4. Esperar a que Copilot genere el código
5. Revisar y hacer commit
6. DETENER y notificar a Manus
7. Manus ejecuta y valida (mínimo consumo)
8. Repetir con siguiente prompt
```

**Ahorro estimado:** 90-95% en créditos Manus

---

## 📋 Lista de Prompts Estratégicos

### PROMPT 1: Procesador de Correos Electrónicos

**Archivo:** `backend/email_processor.py`

**Prompt para Copilot:**

```python
"""
Crea un procesador de correos electrónicos para el sistema de expedientes virtuales SCJN.

Requisitos:
1. Conectar a servidor IMAP
2. Procesar correos no leídos
3. Extraer adjuntos (PDFs, documentos)
4. Calcular hash SHA-256 de cada adjunto
5. Extraer user_hash del email destino (formato: [hash]@scjn-expedientes.mx)
6. Guardar adjuntos en almacenamiento con estructura: /storage/adjuntos/{hash[:2]}/{hash[2:4]}/{hash}.dat
7. Generar metadata JSON para cada adjunto
8. Integrar con blockchain (importar desde blockchain.py)
9. Registrar cada documento en blockchain
10. Enviar notificación al usuario

Tecnologías:
- imaplib para IMAP
- email para parsing
- hashlib para SHA-256
- json para metadata
- pathlib para rutas

Clase principal: EmailProcessor
Métodos:
- __init__(imap_server, email_user, email_pass)
- procesar_correos_nuevos() -> List[Dict]
- procesar_email(email_id) -> Dict
- extraer_adjuntos(msg) -> List[Dict]
- guardar_adjunto(filename, file_data, file_hash) -> str
- registrar_en_blockchain(expediente) -> None

Incluir:
- Manejo de errores robusto
- Logging detallado
- Validación de formatos
- Decodificación de caracteres especiales
- Soporte para múltiples tipos MIME

Estilo: PEP 8, type hints, docstrings completos
"""

# GitHub Copilot generará el código aquí
```

**Instrucciones para el usuario:**

1. Abre GitHub en: https://github.com/GABILANO/scjn-blockchain-expedientes
2. Navega a `backend/`
3. Crea nuevo archivo: `email_processor.py`
4. Pega el prompt completo
5. Presiona Tab para que Copilot genere el código
6. Revisa y ajusta si es necesario
7. Haz commit: "Add email processor with IMAP integration"
8. **DETÉN AQUÍ** y notifica a Manus para validación

**Consumo Manus:** 0 créditos (Copilot genera, Manus solo valida)

---

### PROMPT 2: Gestión de Base de Datos

**Archivo:** `backend/database.py`

**Prompt para Copilot:**

```python
"""
Crea el módulo de gestión de base de datos PostgreSQL para el sistema SCJN.

Requisitos:
1. Conexión a PostgreSQL con psycopg2
2. Operaciones CRUD para todas las tablas:
   - jurisprudencias
   - documentos
   - articulos_citados
   - precedentes
   - expedientes_virtuales
   - expediente_documentos
   - blockchain
   - auditoria

3. Funciones de búsqueda:
   - Buscar jurisprudencias por año, tipo, ministro
   - Buscar por artículos citados
   - Buscar por prescripción (vigentes/prescritas)
   - Búsqueda full-text en contenido

4. Funciones de estadísticas:
   - Total de expedientes por año
   - Distribución por tipo de asunto
   - Top ministros ponentes
   - Jurisprudencias prescritas vs vigentes

5. Integración con blockchain:
   - Guardar bloques en tabla blockchain
   - Verificar integridad
   - Exportar/importar blockchain

Tecnologías:
- psycopg2 para PostgreSQL
- sqlalchemy para ORM (opcional)
- contextlib para context managers
- typing para type hints

Clase principal: DatabaseManager
Métodos:
- __init__(connection_string)
- connect() -> connection
- disconnect() -> None
- insert_jurisprudencia(data: Dict) -> int
- get_jurisprudencia(numero_expediente: str) -> Dict
- search_jurisprudencias(filters: Dict) -> List[Dict]
- insert_documento(data: Dict) -> int
- insert_blockchain_block(block: Dict) -> int
- get_blockchain() -> List[Dict]
- verify_blockchain_integrity() -> Tuple[bool, str]
- get_statistics() -> Dict

Incluir:
- Connection pooling
- Transacciones
- Manejo de errores
- Logging
- Validación de datos
- SQL injection prevention

Estilo: PEP 8, type hints, docstrings completos
"""

# GitHub Copilot generará el código aquí
```

**Instrucciones para el usuario:**

1. Crea archivo: `backend/database.py`
2. Pega el prompt
3. Deja que Copilot genere
4. Commit: "Add database manager with PostgreSQL integration"
5. **DETÉN AQUÍ** y notifica a Manus

**Consumo Manus:** 0 créditos

---

### PROMPT 3: API REST con FastAPI

**Archivo:** `backend/api.py`

**Prompt para Copilot:**

```python
"""
Crea una API REST completa con FastAPI para el sistema de expedientes virtuales SCJN.

Requisitos:

Endpoints de Autenticación:
POST /api/auth/register - Registrar usuario con CURP/RFC
POST /api/auth/verify - Verificar identidad
GET /api/auth/user/{user_hash} - Obtener info de usuario

Endpoints de Expedientes:
GET /api/expedientes/{user_hash} - Obtener expedientes de usuario
POST /api/expedientes - Crear expediente
GET /api/expedientes/{id}/documentos - Listar documentos
POST /api/expedientes/{id}/documentos - Subir documento

Endpoints de Jurisprudencias:
GET /api/jurisprudencias - Listar jurisprudencias (con filtros)
GET /api/jurisprudencias/{numero} - Obtener jurisprudencia específica
GET /api/jurisprudencias/search - Búsqueda avanzada
GET /api/jurisprudencias/stats - Estadísticas

Endpoints de Blockchain:
GET /api/blockchain - Obtener blockchain completa
GET /api/blockchain/{block_id} - Obtener bloque específico
GET /api/blockchain/verify - Verificar integridad
POST /api/blockchain/export - Exportar blockchain

Endpoints de Utilidades:
GET /api/health - Health check
GET /api/stats - Estadísticas generales
POST /api/scraper/run - Ejecutar scraper (admin)

Tecnologías:
- FastAPI para API REST
- Pydantic para validación
- uvicorn para servidor
- python-multipart para uploads
- python-jose para JWT (opcional)

Incluir:
- Modelos Pydantic para request/response
- Validación de datos
- Manejo de errores HTTP
- CORS middleware
- Documentación automática (Swagger)
- Rate limiting
- Autenticación básica
- Logging de requests

Integrar con:
- auth_curp_rfc.py
- blockchain.py
- database.py
- scjn_scraper.py

Estilo: PEP 8, type hints, docstrings, async/await
"""

# GitHub Copilot generará el código aquí
```

**Instrucciones para el usuario:**

1. Crea archivo: `backend/api.py`
2. Pega el prompt
3. Deja que Copilot genere
4. Commit: "Add FastAPI REST API with all endpoints"
5. **DETÉN AQUÍ** y notifica a Manus

**Consumo Manus:** 0 créditos

---

### PROMPT 4: Esquema de Base de Datos SQL

**Archivo:** `database/schema.sql`

**Prompt para Copilot:**

```sql
-- Crea el esquema completo de base de datos PostgreSQL para el sistema SCJN
-- 
-- Requisitos:
-- 1. Tabla jurisprudencias con todos los campos mencionados en ARQUITECTURA_SISTEMA.md
-- 2. Tabla documentos con relación a jurisprudencias
-- 3. Tabla articulos_citados con relación a jurisprudencias
-- 4. Tabla precedentes con relaciones entre jurisprudencias
-- 5. Tabla expedientes_virtuales para usuarios
-- 6. Tabla expediente_documentos para documentos de usuarios
-- 7. Tabla blockchain para bloques
-- 8. Tabla auditoria para logs
-- 
-- Incluir:
-- - Índices apropiados para búsquedas rápidas
-- - Foreign keys con ON DELETE CASCADE
-- - Constraints de validación
-- - Triggers para updated_at
-- - Extensión pgvector para embeddings
-- - Comentarios en cada tabla y campo
-- 
-- Usar tipos de datos apropiados:
-- - VARCHAR para textos cortos
-- - TEXT para textos largos
-- - TIMESTAMP para fechas
-- - BOOLEAN para flags
-- - BIGINT para IDs grandes
-- - vector(1536) para embeddings

-- GitHub Copilot generará el código aquí
```

**Instrucciones para el usuario:**

1. Crea archivo: `database/schema.sql`
2. Pega el prompt
3. Deja que Copilot genere
4. Commit: "Add complete PostgreSQL schema with indexes"
5. **DETÉN AQUÍ** y notifica a Manus

**Consumo Manus:** 0 créditos

---

### PROMPT 5: Tests Automatizados

**Archivo:** `tests/test_blockchain.py`

**Prompt para Copilot:**

```python
"""
Crea tests completos para el módulo blockchain.py usando pytest.

Requisitos:
1. Test de creación de bloque génesis
2. Test de generación de números primos
3. Test de validación de números primos (Miller-Rabin)
4. Test de adición de bloques
5. Test de proof-of-work
6. Test de validación de blockchain
7. Test de detección de bloques modificados
8. Test de exportación/importación JSON
9. Test de registro de expedientes
10. Test de registro de documentos
11. Test de verificación de documentos
12. Test de cadena de custodia
13. Test de estadísticas

Usar:
- pytest para framework
- pytest fixtures para setup/teardown
- parametrize para múltiples casos
- monkeypatch para mocking
- tmp_path para archivos temporales

Incluir:
- Tests unitarios para cada función
- Tests de integración
- Tests de edge cases
- Tests de rendimiento (opcional)
- Asserts detallados
- Docstrings explicativos

Cobertura objetivo: 90%+

Estilo: PEP 8, nombres descriptivos
"""

# GitHub Copilot generará el código aquí
```

**Instrucciones para el usuario:**

1. Crea archivo: `tests/test_blockchain.py`
2. Pega el prompt
3. Deja que Copilot genere
4. Crea también: `tests/test_auth.py`, `tests/test_scraper.py` con prompts similares
5. Commit: "Add comprehensive test suite with pytest"
6. **DETÉN AQUÍ** y notifica a Manus

**Consumo Manus:** 0 créditos

---

### PROMPT 6: Frontend Web Básico

**Archivo:** `frontend/index.html`

**Prompt para Copilot:**

```html
<!-- 
Crea una interfaz web completa para el sistema de expedientes virtuales SCJN

Requisitos:

Página Principal:
1. Header con logo y navegación
2. Hero section explicando el sistema
3. Sección de características principales
4. Formulario de registro (CURP/RFC)
5. Sección de búsqueda de jurisprudencias
6. Footer con enlaces

Funcionalidades JavaScript:
1. Validación de CURP/RFC en tiempo real
2. Llamadas a API REST (fetch)
3. Mostrar resultados de búsqueda
4. Visualización de blockchain
5. Subida de documentos con drag & drop
6. Notificaciones toast
7. Responsive design (mobile-first)

Estilo:
1. CSS moderno (Flexbox/Grid)
2. Colores: tema legal (azul oscuro, dorado)
3. Tipografía: profesional
4. Animaciones sutiles
5. Dark mode toggle

Tecnologías:
- HTML5 semántico
- CSS3 moderno (sin frameworks)
- JavaScript vanilla (ES6+)
- Fetch API para AJAX
- LocalStorage para cache

Incluir:
- Accesibilidad (ARIA labels)
- SEO básico (meta tags)
- Performance (lazy loading)
- Validación de formularios
- Manejo de errores
- Loading states

Estructura:
- index.html (página principal)
- css/styles.css (estilos)
- js/app.js (lógica)
- js/api.js (cliente API)
- js/validators.js (validaciones)
-->

<!-- GitHub Copilot generará el código aquí -->
```

**Instrucciones para el usuario:**

1. Crea archivo: `frontend/index.html`
2. Pega el prompt
3. Deja que Copilot genere
4. Crea también los archivos CSS y JS mencionados
5. Commit: "Add complete frontend with responsive design"
6. **DETÉN AQUÍ** y notifica a Manus

**Consumo Manus:** 0 créditos

---

### PROMPT 7: Configuración de Docker

**Archivo:** `docker-compose.yml`

**Prompt para Copilot:**

```yaml
# Crea una configuración completa de Docker Compose para el sistema SCJN
#
# Servicios requeridos:
# 1. app - Aplicación Python (FastAPI)
# 2. postgres - PostgreSQL 15 con pgvector
# 3. postfix - Servidor SMTP
# 4. dovecot - Servidor IMAP
# 5. minio - Almacenamiento S3-compatible
# 6. nginx - Reverse proxy y servidor web
#
# Requisitos:
# - Volúmenes persistentes para datos
# - Red interna para comunicación entre servicios
# - Variables de entorno desde .env
# - Health checks para todos los servicios
# - Restart policy: unless-stopped
# - Logs con rotación
#
# Puertos expuestos:
# - 80 (nginx HTTP)
# - 443 (nginx HTTPS)
# - 8000 (API FastAPI)
# - 5432 (PostgreSQL)
# - 9000 (MinIO)
#
# Incluir:
# - Dockerfile para app Python
# - Configuración de nginx
# - Scripts de inicialización
# - Backups automáticos

# GitHub Copilot generará el código aquí
```

**Instrucciones para el usuario:**

1. Crea archivo: `docker-compose.yml`
2. Pega el prompt
3. Deja que Copilot genere
4. Crea también: `Dockerfile`, `nginx.conf`
5. Commit: "Add Docker configuration for deployment"
6. **DETÉN AQUÍ** y notifica a Manus

**Consumo Manus:** 0 créditos

---

### PROMPT 8: GitHub Actions CI/CD

**Archivo:** `.github/workflows/ci.yml`

**Prompt para Copilot:**

```yaml
# Crea un workflow de GitHub Actions para CI/CD del sistema SCJN
#
# Jobs requeridos:
# 1. test - Ejecutar tests con pytest
# 2. lint - Verificar código con flake8 y black
# 3. security - Escanear vulnerabilidades con bandit
# 4. build - Construir imagen Docker
# 5. deploy - Desplegar a producción (manual)
#
# Triggers:
# - Push a main/master
# - Pull requests
# - Manual workflow_dispatch
#
# Requisitos:
# - Usar Python 3.11
# - Cache de dependencias pip
# - Matriz de tests (Python 3.11, 3.12)
# - Cobertura de tests con codecov
# - Notificaciones en Slack (opcional)
#
# Secrets necesarios:
# - DOCKER_USERNAME
# - DOCKER_PASSWORD
# - DEPLOY_SSH_KEY
#
# Incluir:
# - Badges en README
# - Artifacts de tests
# - Reportes de cobertura

# GitHub Copilot generará el código aquí
```

**Instrucciones para el usuario:**

1. Crea archivo: `.github/workflows/ci.yml`
2. Pega el prompt
3. Deja que Copilot genere
4. Commit: "Add GitHub Actions CI/CD pipeline"
5. **DETÉN AQUÍ** y notifica a Manus

**Consumo Manus:** 0 créditos

---

## 📊 Resumen de Ahorro

### Comparación de Costos

| Tarea | Con Manus | Con Copilot | Ahorro |
|-------|-----------|-------------|--------|
| Email processor | 200-300 créditos | 0 | 100% |
| Database manager | 250-350 créditos | 0 | 100% |
| API REST | 300-400 créditos | 0 | 100% |
| SQL schema | 100-150 créditos | 0 | 100% |
| Tests | 200-300 créditos | 0 | 100% |
| Frontend | 400-500 créditos | 0 | 100% |
| Docker config | 100-150 créditos | 0 | 100% |
| CI/CD | 100-150 créditos | 0 | 100% |
| **TOTAL** | **1,650-2,300** | **0** | **100%** |

**Manus solo valida:** 50-100 créditos (una sola vez al final)

**Ahorro total:** 1,550-2,200 créditos (95-98%)

---

## 🎯 Flujo de Trabajo Recomendado

### Día 1: Backend Core
1. PROMPT 1: Email processor (Copilot)
2. PROMPT 2: Database manager (Copilot)
3. Validación con Manus (50 créditos)

### Día 2: API y Tests
4. PROMPT 3: API REST (Copilot)
5. PROMPT 4: SQL schema (Copilot)
6. PROMPT 5: Tests (Copilot)
7. Validación con Manus (30 créditos)

### Día 3: Frontend y Deploy
8. PROMPT 6: Frontend (Copilot)
9. PROMPT 7: Docker (Copilot)
10. PROMPT 8: CI/CD (Copilot)
11. Validación final con Manus (20 créditos)

**Total:** 100 créditos vs 2,000+ con método tradicional

---

## 💡 Consejos Adicionales

### Para Maximizar Eficiencia de Copilot

1. **Prompts detallados:** Más contexto = mejor código
2. **Ejemplos:** Incluir ejemplos de uso esperado
3. **Estilo:** Especificar convenciones de código
4. **Integración:** Mencionar otros módulos a importar
5. **Tests:** Pedir tests junto con código

### Para Minimizar Uso de Manus

1. **Validar en batch:** No validar cada archivo individualmente
2. **Tests automáticos:** Dejar que pytest valide
3. **Linting:** Usar black/flake8 antes de Manus
4. **Documentación:** Copilot puede generar docs también

### Cuando SÍ Usar Manus

1. **Navegación web:** Scraping de SCJN
2. **Validación final:** Ejecutar tests completos
3. **Debugging:** Errores que Copilot no puede resolver
4. **Despliegue:** Configuración de servidores

---

## 📞 Soporte

Si tienes dudas sobre los prompts:

1. Revisa ejemplos en el código existente
2. Consulta documentación de cada tecnología
3. Ajusta el prompt según necesidades
4. Itera con Copilot hasta obtener resultado deseado

---

**¡Ahorra hasta 95% en créditos usando esta estrategia!** 🚀
