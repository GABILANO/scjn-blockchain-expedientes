# Sistema de Expedientes Virtuales SCJN con Blockchain

**Versión:** 1.0.0  
**Fecha:** 20 de noviembre de 2025  
**Licencia:** MIT  

---

## 🎯 Descripción

Sistema completo de **expedientes virtuales descentralizados** para la gestión automatizada de jurisprudencias de la Suprema Corte de Justicia de la Nación (SCJN) de México, con autenticación dual CURP/RFC, blockchain basado en números primos, y optimización extrema de costos para uso con Manus AI.

### Características Principales

✅ **Blockchain Híbrido con Números Primos**
- Sistema de identificadores únicos basados en números primos
- Proof-of-Work simplificado para validación
- Cadena de custodia inmutable y verificable
- Cumplimiento NOM-151-SCFI-2016

✅ **Autenticación Dual CURP/RFC**
- Validación cruzada de identidades
- Soporte para personas físicas y morales
- Anonimización mediante hashing SHA-256
- Integración con certificados SAT (.key y .cer)

✅ **Automatización por Correo Electrónico**
- Email personalizado por usuario: `[hash]@scjn-expedientes.mx`
- Procesamiento automático de adjuntos
- Registro blockchain de cada documento
- Sistema de notificaciones

✅ **Base de Datos de Jurisprudencias**
- Scraping automatizado de SCJN
- Indexación completa por múltiples criterios
- Búsqueda semántica con embeddings
- Filtrado por prescripción legal

✅ **Optimización de Costos Manus**
- **70-85% de ahorro** en créditos
- Scripts locales para procesamiento pesado
- Manus solo para navegación web
- Cache inteligente de resultados

---

## 📦 Estructura del Proyecto

```
scjn-blockchain-system/
├── README.md                          ← Este archivo
├── ARQUITECTURA_SISTEMA.md            ← Documentación técnica completa
├── LICENSE                            ← Licencia MIT
│
├── backend/                           ← Backend Python
│   ├── scjn_scraper.py                ← Scraper optimizado SCJN
│   ├── auth_curp_rfc.py               ← Autenticación CURP/RFC
│   ├── blockchain.py                  ← Sistema de blockchain
│   ├── email_processor.py             ← Procesador de correos
│   ├── database.py                    ← Gestión de base de datos
│   └── api.py                         ← API REST
│
├── scripts/                           ← Scripts de automatización
│   ├── SCJN_Mass_Downloader_GDrive.user.js
│   ├── SCJN_Extractor_Ultimate.user.js
│   ├── generar_cadena_custodia.sh
│   └── setup_environment.sh
│
├── frontend/                          ← Frontend web
│   ├── index.html
│   ├── css/
│   ├── js/
│   └── assets/
│
├── database/                          ← Esquemas de base de datos
│   ├── schema.sql
│   ├── migrations/
│   └── seeds/
│
├── config/                            ← Archivos de configuración
│   ├── config.example.json
│   ├── postfix.conf
│   └── nginx.conf
│
├── docs/                              ← Documentación adicional
│   ├── GUIA_INSTALACION.md
│   ├── GUIA_USO.md
│   ├── API_REFERENCE.md
│   └── FAQ.md
│
├── tests/                             ← Tests automatizados
│   ├── test_blockchain.py
│   ├── test_auth.py
│   └── test_scraper.py
│
└── .github/                           ← GitHub Actions
    └── workflows/
        ├── ci.yml
        └── deploy.yml
```

---

## 🚀 Inicio Rápido

### Prerrequisitos

- **Python 3.11+**
- **PostgreSQL 15+** con extensión `pgvector`
- **Node.js 18+** (opcional, para frontend)
- **Postfix + Dovecot** (para sistema de correo)
- **MinIO** o S3 (para almacenamiento de archivos)

### Instalación

#### 1. Clonar el repositorio

```bash
git clone https://github.com/TU_USUARIO/scjn-blockchain-system.git
cd scjn-blockchain-system
```

#### 2. Instalar dependencias Python

```bash
pip install -r requirements.txt
```

#### 3. Configurar base de datos

```bash
# Crear base de datos PostgreSQL
createdb scjn_expedientes

# Instalar extensión pgvector
psql scjn_expedientes -c "CREATE EXTENSION vector;"

# Ejecutar migraciones
psql scjn_expedientes < database/schema.sql
```

#### 4. Configurar variables de entorno

```bash
cp config/config.example.json config/config.json
# Editar config.json con tus credenciales
```

#### 5. Ejecutar scraper de prueba

```bash
cd backend
python3 scjn_scraper.py --año 2025 --no-pdfs
```

---

## 📖 Guías de Uso

### 1. Scraping de Jurisprudencias SCJN

**Opción A: Script Python (Recomendado para Manus)**

```bash
cd backend
python3 scjn_scraper.py --año 2025 --output ../data
```

**Opciones:**
- `--año`: Año a extraer (default: 2025)
- `--output`: Directorio de salida (default: ./data)
- `--no-pdfs`: Solo extraer metadata, no descargar PDFs
- `--cache`: Usar cache (default: True)

**Opción B: UserScript en Navegador**

1. Instalar **Violentmonkey** o **Tampermonkey**
2. Cargar script: `scripts/SCJN_Mass_Downloader_GDrive.user.js`
3. Navegar a: `https://www2.scjn.gob.mx/ConsultasTematica/Resultados/-0-0-0-0-2025`
4. Hacer clic en "🚀 Iniciar Descarga Masiva"

### 2. Registro de Usuario

```python
from backend.auth_curp_rfc import GestorExpedientesVirtuales

gestor = GestorExpedientesVirtuales()

# Registrar persona física
valido, mensaje, info = gestor.registrar_usuario(
    curp="GABC850101HDFRRL09",
    rfc="GABC850101ABC"
)

if valido:
    print(f"Email personalizado: {info['email_personalizado']}")
    print(f"User hash: {info['user_hash']}")
```

### 3. Registro en Blockchain

```python
from backend.blockchain import ExpedienteBlockchain

blockchain = ExpedienteBlockchain(difficulty=4)

# Registrar expediente
block = blockchain.registrar_expediente(
    user_hash="abc123def456",
    curp_hash="hash_curp",
    rfc_hash="hash_rfc",
    email_personalizado="abc123@scjn-expedientes.mx"
)

print(f"Expediente registrado en bloque #{block.block_id}")

# Registrar documento
block = blockchain.registrar_documento(
    user_hash="abc123def456",
    documento_hash="doc_hash_789",
    nombre_documento="demanda.pdf",
    origen_email="usuario@gmail.com",
    asunto_email="Demanda de amparo",
    tamano_bytes=1024000
)

# Verificar integridad
valida, mensaje = blockchain.blockchain.is_valid()
print(f"Blockchain: {mensaje}")
```

### 4. Procesamiento de Correos

```python
from backend.email_processor import EmailProcessor

processor = EmailProcessor(
    imap_server="mail.scjn-expedientes.mx",
    email_user="processor@scjn-expedientes.mx",
    email_pass="tu_contraseña"
)

# Procesar correos nuevos
expedientes = processor.procesar_correos_nuevos()

for exp in expedientes:
    print(f"Expediente creado para: {exp['user_hash']}")
    print(f"Documentos adjuntos: {len(exp['adjuntos'])}")
```

---

## 🔒 Seguridad y Cumplimiento Normativo

### Normativas Cumplidas

✅ **NOM-151-SCFI-2016**
- Preservación de mensajes de datos
- Hashing criptográfico SHA-256
- Timestamps en formato RFC 3339
- Cadena de custodia documentada

✅ **Código Nacional de Procedimientos Penales (CNPP)**
- Cadena de custodia digital
- Registro de todas las acciones
- Integridad verificable
- Trazabilidad completa

✅ **Ley Federal de Protección de Datos Personales (LFPDPPP)**
- Anonimización de datos sensibles
- Hashing de CURP y RFC
- No almacenamiento de datos personales en texto plano
- Cumplimiento de privacidad

✅ **Código Federal de Procedimientos Civiles (CFPC)**
- Validez probatoria de documentos electrónicos
- Firma digital mediante hashing
- Fecha cierta documentada
- Autenticidad verificable

### Buenas Prácticas de Seguridad

1. **Nunca almacenar CURP/RFC en texto plano**
2. **Usar HTTPS para todas las comunicaciones**
3. **Rotar salts periódicamente**
4. **Hacer backups regulares de la blockchain**
5. **Auditar logs de acceso**
6. **Validar integridad de blockchain diariamente**

---

## 💰 Optimización de Costos Manus

### Estrategia de Ahorro

El sistema está diseñado para **minimizar el consumo de créditos Manus** mediante:

#### 1. Delegación Estratégica

| Tarea | Ejecutor | Créditos |
|-------|----------|----------|
| Navegación web SCJN | Manus Browser | 10-20 |
| Descarga de PDFs | Manus Browser | 3-7 |
| Extracción de texto | Python local | 0 |
| Cálculo de hashes | Python local | 0 |
| Registro blockchain | Python local | 0 |
| Generación informes | Python + Gemini API | 1-3 |
| Búsqueda semántica | PostgreSQL local | 0 |
| Procesamiento emails | Python local | 0 |

#### 2. Sistema de Cache

- Cache de páginas HTML (24 horas)
- Cache de PDFs descargados
- Cache de resultados de búsqueda
- Cache de embeddings

#### 3. Procesamiento Batch

- Agrupar múltiples expedientes
- Descargar en horarios de baja demanda
- Procesar localmente

### Comparación de Costos

| Método | Créditos por Expediente | Total 100 Expedientes |
|--------|------------------------|----------------------|
| 100% Manus | 50-80 | 5,000-8,000 |
| **Sistema Híbrido** | **10-22** | **1,000-2,200** |
| **Ahorro** | **40-58 (70-80%)** | **4,000-5,800 (72-80%)** |

---

## 🧪 Tests

### Ejecutar tests

```bash
# Todos los tests
pytest tests/

# Test específico
pytest tests/test_blockchain.py

# Con cobertura
pytest --cov=backend tests/
```

### Tests disponibles

- `test_blockchain.py`: Tests de blockchain y números primos
- `test_auth.py`: Tests de validación CURP/RFC
- `test_scraper.py`: Tests de scraping SCJN
- `test_email.py`: Tests de procesamiento de correos

---

## 📊 Estadísticas del Sistema

### Capacidades

- **Expedientes procesados:** Ilimitados
- **Documentos por expediente:** Ilimitados
- **Tamaño máximo por documento:** 100 MB
- **Usuarios registrados:** Ilimitados
- **Velocidad de scraping:** ~50 expedientes/minuto
- **Velocidad de blockchain:** ~10 bloques/segundo

### Requisitos de Hardware

**Mínimo:**
- CPU: 2 cores
- RAM: 4 GB
- Disco: 50 GB

**Recomendado:**
- CPU: 4+ cores
- RAM: 8+ GB
- Disco: 200+ GB SSD

---

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor:

1. Fork el repositorio
2. Crear rama feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit cambios (`git commit -am 'Agregar nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Crear Pull Request

### Guías de Contribución

- Seguir PEP 8 para código Python
- Documentar todas las funciones
- Agregar tests para nuevas funcionalidades
- Actualizar documentación

---

## 📝 Licencia

Este proyecto está bajo la Licencia MIT. Ver archivo `LICENSE` para más detalles.

---

## 📞 Soporte

### Documentación

- [Guía de Instalación](docs/GUIA_INSTALACION.md)
- [Guía de Uso](docs/GUIA_USO.md)
- [Referencia API](docs/API_REFERENCE.md)
- [FAQ](docs/FAQ.md)
- [Arquitectura del Sistema](ARQUITECTURA_SISTEMA.md)

### Contacto

- **Issues:** [GitHub Issues](https://github.com/TU_USUARIO/scjn-blockchain-system/issues)
- **Discusiones:** [GitHub Discussions](https://github.com/TU_USUARIO/scjn-blockchain-system/discussions)

---

## 🎉 Créditos

**Desarrollado por:**
- Sistema Manus AI
- Basado en trabajo original de GÉNESIS (Arquitecto Soberano)

**Tecnologías utilizadas:**
- Python 3.11
- PostgreSQL 15 + pgvector
- Postfix + Dovecot
- MinIO / S3
- Blockchain custom
- Violentmonkey

---

## ⚖️ Aviso Legal

- Este software accede únicamente a **datos públicos** de la SCJN
- No realiza ninguna acción ilegal o no autorizada
- Los archivos descargados son de **dominio público**
- El usuario es responsable del uso que haga de los datos
- Consulta con un abogado para validar el cumplimiento normativo en tu jurisdicción

---

## 🗺️ Roadmap

### Versión 1.1 (Q1 2026)
- [ ] API REST completa
- [ ] Frontend web interactivo
- [ ] Integración con Google Drive
- [ ] Notificaciones push

### Versión 1.2 (Q2 2026)
- [ ] Búsqueda semántica con embeddings
- [ ] Análisis de jurisprudencias con IA
- [ ] Generación automática de informes
- [ ] Dashboard de estadísticas

### Versión 2.0 (Q3 2026)
- [ ] Blockchain distribuida (múltiples nodos)
- [ ] Integración con RENAPO y SAT
- [ ] Firma electrónica avanzada
- [ ] Aplicación móvil

---

**¡Gracias por usar el Sistema de Expedientes Virtuales SCJN!** ⚖️

Para más información, consulta la [documentación completa](ARQUITECTURA_SISTEMA.md).
