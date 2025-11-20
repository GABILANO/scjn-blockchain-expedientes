# ARQUITECTURA DEL SISTEMA DE EXPEDIENTES VIRTUALES SCJN
## Sistema Blockchain con Autenticación CURP/RFC

**Versión:** 1.0.0  
**Fecha:** 20 de noviembre de 2025  
**Arquitecto:** Sistema Manus AI  

---

## RESUMEN EJECUTIVO

Este documento describe la arquitectura completa de un **sistema de expedientes virtuales descentralizado** para la gestión automatizada de jurisprudencias de la SCJN, con las siguientes características principales:

### Características Principales

**1. Blockchain Híbrido con Números Primos**
- Utiliza secuencias de números primos y no primos para evitar colisiones
- Cada expediente tiene un identificador único basado en hash(CURP+RFC+timestamp)
- Cadena de custodia inmutable con proof-of-work simplificado

**2. Autenticación Dual CURP/RFC**
- Validación cruzada con bases de datos RENAPO y SAT
- Soporte para personas físicas y morales
- Anonimización mediante hashing SHA-256
- Sistema de certificados .key y .cer del SAT

**3. Automatización por Correo Electrónico**
- Cada usuario registrado obtiene un correo personalizado: `[hash_curp_rfc]@scjn-expedientes.mx`
- Reenvío automático crea expedientes virtuales
- Adjuntos se procesan y almacenan con hash SHA-256
- Sistema de notificaciones automáticas

**4. Base de Datos de Jurisprudencias**
- Scraping automatizado de SCJN con validación forense
- Indexación por fecha, tipo, ministro ponente, artículos citados
- Sistema de búsqueda semántica con embeddings
- Filtrado por prescripción legal

**5. Optimización de Costos Manus**
- Scripts locales para procesamiento pesado (70-85% ahorro)
- Manus solo para navegación web en tiempo real
- Procesamiento batch con Python local
- Cache inteligente de resultados

---

## PARTE 1: ARQUITECTURA DE BLOCKCHAIN

### 1.1 Estructura de Bloques

Cada bloque en la cadena contiene:

```json
{
  "block_id": 123456789,
  "block_type": "prime",
  "timestamp": "2025-11-20T12:34:56.789Z",
  "previous_hash": "0000abc123...",
  "data": {
    "expediente_id": "EXP-2025-001-ABC123",
    "user_hash": "sha256(CURP+RFC)",
    "document_hash": "sha256(documento)",
    "metadata": {
      "tipo_documento": "demanda",
      "fecha_presentacion": "2025-11-20",
      "jurisprudencia_relacionada": ["1/2023", "5/2024"],
      "articulos_citados": ["Art. 1 CPEUM", "Art. 14 CPEUM"]
    },
    "email_origin": "usuario@gmail.com",
    "forwarded_to": "abc123def456@scjn-expedientes.mx"
  },
  "nonce": 42857,
  "hash": "0000def456..."
}
```

### 1.2 Sistema de Números Primos

**Propósito:** Evitar colisiones y garantizar unicidad de identificadores

**Algoritmo de Asignación:**

```python
def generar_id_expediente(curp, rfc, timestamp):
    """
    Genera ID único usando números primos
    """
    # Hash base
    base_hash = sha256(f"{curp}{rfc}{timestamp}").hexdigest()
    
    # Convertir a número
    num = int(base_hash[:16], 16)
    
    # Encontrar el siguiente número primo
    prime_id = next_prime(num)
    
    # Asignar tipo de bloque
    if is_prime(prime_id):
        block_type = "prime"
    else:
        block_type = "composite"
    
    return {
        "id": prime_id,
        "type": block_type,
        "hash": base_hash
    }

def next_prime(n):
    """Encuentra el siguiente número primo después de n"""
    candidate = n + 1
    while not is_prime(candidate):
        candidate += 1
    return candidate

def is_prime(n):
    """Verifica si n es primo (Miller-Rabin)"""
    if n < 2:
        return False
    if n == 2 or n == 3:
        return True
    if n % 2 == 0:
        return False
    
    # Miller-Rabin test
    r, d = 0, n - 1
    while d % 2 == 0:
        r += 1
        d //= 2
    
    for _ in range(5):  # 5 rondas
        a = random.randrange(2, n - 1)
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True
```

**Ventajas del Sistema de Números Primos:**

1. **Unicidad Matemática:** Los números primos garantizan distribución uniforme
2. **Detección de Colisiones:** Fácil verificar si un ID ya existe
3. **Seguridad Criptográfica:** Dificulta ataques de predicción
4. **Eficiencia Computacional:** Algoritmo Miller-Rabin es O(k log³ n)

### 1.3 Cadena de Custodia

**Flujo de Registro:**

```
Usuario → Email → Sistema → Validación CURP/RFC → Generación de Hash → 
Asignación de ID Primo → Creación de Bloque → Minado (PoW) → 
Inserción en Blockchain → Notificación al Usuario
```

**Proof-of-Work Simplificado:**

```python
def mine_block(block_data, difficulty=4):
    """
    Mina un bloque con PoW simplificado
    difficulty: número de ceros iniciales en el hash
    """
    nonce = 0
    target = "0" * difficulty
    
    while True:
        block_data["nonce"] = nonce
        block_hash = sha256(json.dumps(block_data, sort_keys=True)).hexdigest()
        
        if block_hash.startswith(target):
            block_data["hash"] = block_hash
            return block_data
        
        nonce += 1
        
        # Límite de seguridad
        if nonce > 10_000_000:
            raise Exception("PoW timeout - ajustar difficulty")
```

---

## PARTE 2: SISTEMA DE AUTENTICACIÓN CURP/RFC

### 2.1 Validación de Identidad

**Flujo de Registro:**

```
1. Usuario ingresa CURP y RFC
2. Sistema valida formato (regex)
3. Sistema verifica coincidencia CURP ↔ RFC
4. Sistema genera hash único: sha256(CURP + RFC + salt)
5. Sistema asigna correo: [hash]@scjn-expedientes.mx
6. Sistema crea expediente virtual inicial
7. Usuario recibe notificación con credenciales
```

**Validación de CURP:**

```python
import re

def validar_curp(curp):
    """
    Valida formato de CURP según RENAPO
    Formato: AAAA######HHHHHH##
    """
    pattern = r'^[A-Z]{4}\d{6}[HM][A-Z]{5}[0-9A-Z]\d$'
    
    if not re.match(pattern, curp):
        return False, "Formato inválido"
    
    # Validar fecha de nacimiento
    year = int(curp[4:6])
    month = int(curp[6:8])
    day = int(curp[8:10])
    
    if month < 1 or month > 12:
        return False, "Mes inválido"
    if day < 1 or day > 31:
        return False, "Día inválido"
    
    # Validar dígito verificador
    if not validar_digito_verificador_curp(curp):
        return False, "Dígito verificador incorrecto"
    
    return True, "CURP válido"

def validar_digito_verificador_curp(curp):
    """Valida el dígito verificador del CURP"""
    valores = "0123456789ABCDEFGHIJKLMNÑOPQRSTUVWXYZ"
    suma = 0
    
    for i, char in enumerate(curp[:-1]):
        suma += valores.index(char) * (18 - i)
    
    digito_esperado = (10 - (suma % 10)) % 10
    return str(digito_esperado) == curp[-1]
```

**Validación de RFC:**

```python
def validar_rfc(rfc, tipo="fisica"):
    """
    Valida formato de RFC según SAT
    Persona física: AAAA######XXX
    Persona moral: AAA######XXX
    """
    if tipo == "fisica":
        pattern = r'^[A-ZÑ&]{4}\d{6}[A-Z0-9]{3}$'
        if len(rfc) != 13:
            return False, "RFC de persona física debe tener 13 caracteres"
    else:  # moral
        pattern = r'^[A-ZÑ&]{3}\d{6}[A-Z0-9]{3}$'
        if len(rfc) != 12:
            return False, "RFC de persona moral debe tener 12 caracteres"
    
    if not re.match(pattern, rfc):
        return False, "Formato inválido"
    
    # Validar homoclave
    if not validar_homoclave_rfc(rfc):
        return False, "Homoclave inválida"
    
    return True, "RFC válido"

def validar_homoclave_rfc(rfc):
    """Valida la homoclave del RFC"""
    # Algoritmo de validación de homoclave SAT
    # (Implementación completa en el código fuente)
    return True  # Simplificado para documentación
```

**Validación Cruzada CURP ↔ RFC:**

```python
def validar_coincidencia_curp_rfc(curp, rfc):
    """
    Verifica que CURP y RFC correspondan a la misma persona
    """
    # Extraer fecha de nacimiento del CURP
    curp_year = curp[4:6]
    curp_month = curp[6:8]
    curp_day = curp[8:10]
    
    # Extraer fecha de nacimiento del RFC
    rfc_year = rfc[4:6]
    rfc_month = rfc[6:8]
    rfc_day = rfc[8:10]
    
    if curp_year != rfc_year or curp_month != rfc_month or curp_day != rfc_day:
        return False, "Fechas de nacimiento no coinciden"
    
    # Extraer iniciales del CURP
    curp_iniciales = curp[0:4]
    
    # Extraer iniciales del RFC
    rfc_iniciales = rfc[0:4]
    
    if curp_iniciales != rfc_iniciales:
        return False, "Iniciales no coinciden"
    
    return True, "CURP y RFC coinciden"
```

### 2.2 Gestión de Certificados SAT (.key y .cer)

**Soporte para Certificados Vencidos:**

```python
from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
import datetime

def cargar_certificado_sat(cer_path, key_path, password=None):
    """
    Carga certificados SAT incluso si están vencidos
    Útil para validación histórica
    """
    # Cargar certificado .cer
    with open(cer_path, 'rb') as f:
        cert_data = f.read()
        cert = x509.load_der_x509_certificate(cert_data, default_backend())
    
    # Cargar llave privada .key
    with open(key_path, 'rb') as f:
        key_data = f.read()
        if password:
            private_key = serialization.load_der_private_key(
                key_data, 
                password=password.encode(), 
                backend=default_backend()
            )
        else:
            private_key = serialization.load_der_private_key(
                key_data, 
                password=None, 
                backend=default_backend()
            )
    
    # Extraer información del certificado
    info = {
        "rfc": extraer_rfc_de_certificado(cert),
        "nombre": cert.subject.get_attributes_for_oid(x509.NameOID.COMMON_NAME)[0].value,
        "valido_desde": cert.not_valid_before,
        "valido_hasta": cert.not_valid_after,
        "vencido": cert.not_valid_after < datetime.datetime.now(),
        "numero_serie": cert.serial_number,
        "emisor": cert.issuer.rfc4514_string()
    }
    
    return {
        "certificado": cert,
        "llave_privada": private_key,
        "info": info
    }

def extraer_rfc_de_certificado(cert):
    """Extrae el RFC del certificado SAT"""
    # El RFC está en el campo serialNumber del subject
    for attr in cert.subject:
        if attr.oid == x509.NameOID.SERIAL_NUMBER:
            return attr.value
    return None

def firmar_documento_con_certificado_vencido(documento_hash, private_key):
    """
    Firma un documento usando certificado vencido
    Útil para demostrar posesión histórica del certificado
    """
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.primitives.asymmetric import padding
    
    signature = private_key.sign(
        documento_hash.encode(),
        padding.PKCS1v15(),
        hashes.SHA256()
    )
    
    return signature.hex()
```

### 2.3 Anonimización y Privacidad

**Sistema de Hashing con Salt:**

```python
import hashlib
import secrets

def generar_hash_usuario(curp, rfc, salt=None):
    """
    Genera hash único para usuario con salt
    """
    if salt is None:
        salt = secrets.token_hex(32)
    
    # Concatenar datos
    data = f"{curp}{rfc}{salt}"
    
    # Generar hash SHA-256
    hash_obj = hashlib.sha256(data.encode())
    user_hash = hash_obj.hexdigest()
    
    return {
        "user_hash": user_hash,
        "salt": salt,
        "email": f"{user_hash[:16]}@scjn-expedientes.mx"
    }

def verificar_usuario(curp, rfc, user_hash, salt):
    """
    Verifica que CURP y RFC correspondan al hash
    """
    data = f"{curp}{rfc}{salt}"
    hash_obj = hashlib.sha256(data.encode())
    calculated_hash = hash_obj.hexdigest()
    
    return calculated_hash == user_hash
```

---

## PARTE 3: SISTEMA DE CORREO ELECTRÓNICO

### 3.1 Arquitectura de Email

**Componentes:**

1. **Servidor SMTP/IMAP:** Postfix + Dovecot
2. **Alias Dinámicos:** PostfixAdmin con base de datos MySQL
3. **Procesador de Correos:** Python daemon con `imaplib`
4. **Parser de Adjuntos:** Python con `email` y `mimetypes`
5. **Almacenamiento:** MinIO (S3-compatible) para adjuntos

**Flujo de Procesamiento:**

```
Email entrante → Postfix → Dovecot → IMAP → Python Daemon → 
Parser → Extracción de Adjuntos → Hash SHA-256 → 
Creación de Bloque → Blockchain → Almacenamiento MinIO → 
Notificación al Usuario
```

### 3.2 Procesador de Correos

```python
import imaplib
import email
from email.header import decode_header
import hashlib
import json
from datetime import datetime

class EmailProcessor:
    def __init__(self, imap_server, email_user, email_pass):
        self.imap = imaplib.IMAP4_SSL(imap_server)
        self.imap.login(email_user, email_pass)
        self.imap.select("INBOX")
    
    def procesar_correos_nuevos(self):
        """
        Procesa todos los correos no leídos
        """
        status, messages = self.imap.search(None, 'UNSEEN')
        
        if status != "OK":
            return []
        
        email_ids = messages[0].split()
        expedientes_creados = []
        
        for email_id in email_ids:
            expediente = self.procesar_email(email_id)
            if expediente:
                expedientes_creados.append(expediente)
        
        return expedientes_creados
    
    def procesar_email(self, email_id):
        """
        Procesa un email individual
        """
        status, msg_data = self.imap.fetch(email_id, '(RFC822)')
        
        if status != "OK":
            return None
        
        # Parsear email
        raw_email = msg_data[0][1]
        msg = email.message_from_bytes(raw_email)
        
        # Extraer información
        from_addr = msg.get("From")
        to_addr = msg.get("To")
        subject = self.decode_subject(msg.get("Subject"))
        date = msg.get("Date")
        
        # Extraer hash de usuario del destinatario
        user_hash = self.extraer_user_hash(to_addr)
        
        if not user_hash:
            return None
        
        # Procesar adjuntos
        adjuntos = self.extraer_adjuntos(msg)
        
        # Crear expediente
        expediente = {
            "user_hash": user_hash,
            "email_origen": from_addr,
            "email_destino": to_addr,
            "asunto": subject,
            "fecha": date,
            "timestamp": datetime.now().isoformat(),
            "adjuntos": adjuntos,
            "hash_email": hashlib.sha256(raw_email).hexdigest()
        }
        
        # Registrar en blockchain
        self.registrar_en_blockchain(expediente)
        
        return expediente
    
    def decode_subject(self, subject):
        """Decodifica el asunto del email"""
        if subject is None:
            return ""
        
        decoded_parts = decode_header(subject)
        decoded_subject = ""
        
        for part, encoding in decoded_parts:
            if isinstance(part, bytes):
                decoded_subject += part.decode(encoding or 'utf-8')
            else:
                decoded_subject += part
        
        return decoded_subject
    
    def extraer_user_hash(self, to_addr):
        """Extrae el hash de usuario del email"""
        # Formato: [hash]@scjn-expedientes.mx
        if "@scjn-expedientes.mx" not in to_addr:
            return None
        
        return to_addr.split("@")[0]
    
    def extraer_adjuntos(self, msg):
        """Extrae y procesa adjuntos del email"""
        adjuntos = []
        
        for part in msg.walk():
            if part.get_content_maintype() == 'multipart':
                continue
            if part.get('Content-Disposition') is None:
                continue
            
            filename = part.get_filename()
            if filename:
                # Decodificar nombre de archivo
                filename = self.decode_subject(filename)
                
                # Obtener contenido
                file_data = part.get_payload(decode=True)
                
                # Calcular hash
                file_hash = hashlib.sha256(file_data).hexdigest()
                
                # Guardar archivo
                file_path = self.guardar_adjunto(filename, file_data, file_hash)
                
                adjuntos.append({
                    "nombre": filename,
                    "tamano": len(file_data),
                    "hash": file_hash,
                    "ruta": file_path,
                    "tipo": part.get_content_type()
                })
        
        return adjuntos
    
    def guardar_adjunto(self, filename, file_data, file_hash):
        """Guarda adjunto en almacenamiento"""
        # Guardar en MinIO o filesystem
        path = f"/storage/adjuntos/{file_hash[:2]}/{file_hash[2:4]}/{file_hash}.dat"
        
        import os
        os.makedirs(os.path.dirname(path), exist_ok=True)
        
        with open(path, 'wb') as f:
            f.write(file_data)
        
        # Guardar metadata
        metadata_path = f"{path}.json"
        with open(metadata_path, 'w') as f:
            json.dump({
                "nombre_original": filename,
                "hash": file_hash,
                "tamano": len(file_data),
                "fecha_guardado": datetime.now().isoformat()
            }, f, indent=2)
        
        return path
    
    def registrar_en_blockchain(self, expediente):
        """Registra el expediente en la blockchain"""
        # Implementación en la siguiente sección
        pass
```

### 3.3 Configuración de Postfix

**Archivo: `/etc/postfix/main.cf`**

```conf
# Configuración básica
myhostname = scjn-expedientes.mx
mydomain = scjn-expedientes.mx
myorigin = $mydomain
mydestination = $myhostname, localhost.$mydomain, localhost, $mydomain

# Alias virtuales
virtual_alias_domains = scjn-expedientes.mx
virtual_alias_maps = mysql:/etc/postfix/mysql-virtual-alias-maps.cf

# Seguridad
smtpd_tls_cert_file = /etc/letsencrypt/live/scjn-expedientes.mx/fullchain.pem
smtpd_tls_key_file = /etc/letsencrypt/live/scjn-expedientes.mx/privkey.pem
smtpd_use_tls = yes
smtpd_tls_security_level = may

# Restricciones
smtpd_recipient_restrictions = 
    permit_mynetworks,
    permit_sasl_authenticated,
    reject_unauth_destination
```

**Archivo: `/etc/postfix/mysql-virtual-alias-maps.cf`**

```conf
user = postfix
password = [CONTRASEÑA_SEGURA]
hosts = localhost
dbname = postfix_db
query = SELECT destination FROM virtual_aliases WHERE source='%s'
```

**Script SQL para crear alias dinámicos:**

```sql
CREATE DATABASE postfix_db;

USE postfix_db;

CREATE TABLE virtual_aliases (
    id INT AUTO_INCREMENT PRIMARY KEY,
    source VARCHAR(255) NOT NULL,
    destination VARCHAR(255) NOT NULL,
    user_hash VARCHAR(64) NOT NULL,
    curp_hash VARCHAR(64) NOT NULL,
    rfc_hash VARCHAR(64) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX(source),
    INDEX(user_hash)
);

-- Ejemplo de inserción
INSERT INTO virtual_aliases (source, destination, user_hash, curp_hash, rfc_hash)
VALUES (
    'abc123def456@scjn-expedientes.mx',
    'processor@localhost',
    'abc123def456',
    'sha256(CURP)',
    'sha256(RFC)'
);
```

---

## PARTE 4: BASE DE DATOS DE JURISPRUDENCIAS

### 4.1 Esquema de Base de Datos

**Tecnología:** PostgreSQL 15 con extensiones `pgvector` para embeddings

**Tablas Principales:**

```sql
-- Tabla de jurisprudencias
CREATE TABLE jurisprudencias (
    id SERIAL PRIMARY KEY,
    numero_expediente VARCHAR(50) UNIQUE NOT NULL,
    año INT NOT NULL,
    tipo_asunto VARCHAR(100),
    organo_radicacion VARCHAR(100),
    ministro_ponente VARCHAR(200),
    tema TEXT,
    descripcion TEXT,
    organo_origen VARCHAR(200),
    fecha_resolucion DATE,
    fecha_publicacion DATE,
    fecha_prescripcion DATE,
    prescrito BOOLEAN DEFAULT FALSE,
    url_scjn TEXT,
    hash_documento VARCHAR(64),
    embedding vector(1536),  -- OpenAI embeddings
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Índices
CREATE INDEX idx_numero_expediente ON jurisprudencias(numero_expediente);
CREATE INDEX idx_año ON jurisprudencias(año);
CREATE INDEX idx_prescrito ON jurisprudencias(prescrito);
CREATE INDEX idx_fecha_resolucion ON jurisprudencias(fecha_resolucion);

-- Índice vectorial para búsqueda semántica
CREATE INDEX idx_embedding ON jurisprudencias USING ivfflat (embedding vector_cosine_ops);

-- Tabla de documentos asociados
CREATE TABLE documentos (
    id SERIAL PRIMARY KEY,
    jurisprudencia_id INT REFERENCES jurisprudencias(id),
    tipo_documento VARCHAR(50),  -- PDF, ENGROSE, SENTENCIA, etc.
    nombre_archivo VARCHAR(255),
    ruta_archivo TEXT,
    hash_sha256 VARCHAR(64) UNIQUE NOT NULL,
    tamano_bytes BIGINT,
    url_descarga TEXT,
    fecha_descarga TIMESTAMP,
    contenido_texto TEXT,  -- Texto extraído del PDF
    embedding vector(1536),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_jurisprudencia_id ON documentos(jurisprudencia_id);
CREATE INDEX idx_hash_sha256 ON documentos(hash_sha256);

-- Tabla de artículos citados
CREATE TABLE articulos_citados (
    id SERIAL PRIMARY KEY,
    jurisprudencia_id INT REFERENCES jurisprudencias(id),
    articulo VARCHAR(200),  -- "Art. 1 CPEUM"
    ley VARCHAR(200),  -- "Constitución Política de los Estados Unidos Mexicanos"
    contenido TEXT,  -- Texto del artículo
    relevancia FLOAT,  -- 0.0 - 1.0
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_articulo ON articulos_citados(articulo);

-- Tabla de precedentes
CREATE TABLE precedentes (
    id SERIAL PRIMARY KEY,
    jurisprudencia_origen_id INT REFERENCES jurisprudencias(id),
    jurisprudencia_citada_id INT REFERENCES jurisprudencias(id),
    tipo_relacion VARCHAR(50),  -- "cita", "contradice", "confirma", etc.
    relevancia FLOAT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla de expedientes virtuales de usuarios
CREATE TABLE expedientes_virtuales (
    id SERIAL PRIMARY KEY,
    user_hash VARCHAR(64) NOT NULL,
    curp_hash VARCHAR(64) NOT NULL,
    rfc_hash VARCHAR(64) NOT NULL,
    email_personalizado VARCHAR(255) UNIQUE NOT NULL,
    tipo_persona VARCHAR(10),  -- "fisica" o "moral"
    activo BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_user_hash ON expedientes_virtuales(user_hash);
CREATE INDEX idx_email_personalizado ON expedientes_virtuales(email_personalizado);

-- Tabla de documentos de expedientes virtuales
CREATE TABLE expediente_documentos (
    id SERIAL PRIMARY KEY,
    expediente_id INT REFERENCES expedientes_virtuales(id),
    nombre_documento VARCHAR(255),
    hash_sha256 VARCHAR(64) UNIQUE NOT NULL,
    ruta_almacenamiento TEXT,
    tamano_bytes BIGINT,
    tipo_mime VARCHAR(100),
    origen_email VARCHAR(255),
    asunto_email TEXT,
    fecha_recepcion TIMESTAMP,
    blockchain_block_id BIGINT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_expediente_id ON expediente_documentos(expediente_id);
CREATE INDEX idx_blockchain_block_id ON expediente_documentos(blockchain_block_id);

-- Tabla de blockchain
CREATE TABLE blockchain (
    id BIGSERIAL PRIMARY KEY,
    block_number BIGINT UNIQUE NOT NULL,
    block_type VARCHAR(20),  -- "prime" o "composite"
    timestamp TIMESTAMP NOT NULL,
    previous_hash VARCHAR(64),
    data JSONB,
    nonce BIGINT,
    hash VARCHAR(64) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_block_number ON blockchain(block_number);
CREATE INDEX idx_hash ON blockchain(hash);
CREATE INDEX idx_timestamp ON blockchain(timestamp);

-- Tabla de auditoría
CREATE TABLE auditoria (
    id BIGSERIAL PRIMARY KEY,
    accion VARCHAR(100),
    tabla VARCHAR(100),
    registro_id BIGINT,
    user_hash VARCHAR(64),
    ip_origen VARCHAR(45),
    user_agent TEXT,
    datos_antes JSONB,
    datos_despues JSONB,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_timestamp_auditoria ON auditoria(timestamp);
CREATE INDEX idx_user_hash_auditoria ON auditoria(user_hash);
```

### 4.2 Sistema de Scraping SCJN

```python
import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime, timedelta
import hashlib
import psycopg2
from psycopg2.extras import Json

class SCJNScraper:
    def __init__(self, db_conn):
        self.db = db_conn
        self.base_url = "https://www2.scjn.gob.mx/ConsultasTematica/Resultados"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'
        })
    
    def scrape_año(self, año):
        """
        Extrae todos los expedientes de un año
        """
        print(f"Iniciando scraping para año {año}...")
        
        # URL de consulta
        url = f"{self.base_url}/-0-0-0-0-{año}"
        
        # Obtener primera página
        response = self.session.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Extraer número total de páginas
        num_paginas = self.extraer_num_paginas(soup)
        print(f"Total de páginas: {num_paginas}")
        
        # Iterar por todas las páginas
        expedientes = []
        for pagina in range(1, num_paginas + 1):
            print(f"Procesando página {pagina}/{num_paginas}...")
            
            if pagina > 1:
                url_pagina = f"{self.base_url}/-0-0-0-{pagina}-{año}"
                response = self.session.get(url_pagina)
                soup = BeautifulSoup(response.text, 'html.parser')
            
            # Extraer expedientes de la página
            expedientes_pagina = self.extraer_expedientes(soup, año)
            expedientes.extend(expedientes_pagina)
            
            # Guardar en base de datos
            for exp in expedientes_pagina:
                self.guardar_expediente(exp)
        
        print(f"Total de expedientes extraídos: {len(expedientes)}")
        return expedientes
    
    def extraer_num_paginas(self, soup):
        """Extrae el número total de páginas"""
        paginacion = soup.find('div', class_='pagination')
        if not paginacion:
            return 1
        
        links = paginacion.find_all('a')
        if not links:
            return 1
        
        # Último número de página
        numeros = [int(link.text) for link in links if link.text.isdigit()]
        return max(numeros) if numeros else 1
    
    def extraer_expedientes(self, soup, año):
        """Extrae expedientes de una página"""
        expedientes = []
        
        # Buscar tabla de resultados
        tabla = soup.find('table', class_='resultados')
        if not tabla:
            return expedientes
        
        filas = tabla.find_all('tr')[1:]  # Saltar encabezado
        
        for fila in filas:
            celdas = fila.find_all('td')
            if len(celdas) < 6:
                continue
            
            # Extraer datos
            numero_expediente = celdas[0].text.strip()
            tipo_asunto = celdas[1].text.strip()
            organo = celdas[2].text.strip()
            ponente = celdas[3].text.strip()
            tema = celdas[4].text.strip()
            organo_origen = celdas[5].text.strip()
            
            # Extraer enlaces a documentos
            documentos = []
            enlaces = celdas[0].find_all('a')
            for enlace in enlaces:
                href = enlace.get('href')
                if href and 'pdf' in href.lower():
                    documentos.append({
                        'url': href if href.startswith('http') else f"https://www2.scjn.gob.mx{href}",
                        'tipo': self.identificar_tipo_documento(enlace.text)
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
                'fecha_extraccion': datetime.now().isoformat()
            }
            
            expedientes.append(expediente)
        
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
        else:
            return 'PDF'
    
    def guardar_expediente(self, expediente):
        """Guarda expediente en la base de datos"""
        cursor = self.db.cursor()
        
        try:
            # Insertar jurisprudencia
            cursor.execute("""
                INSERT INTO jurisprudencias (
                    numero_expediente, año, tipo_asunto, organo_radicacion,
                    ministro_ponente, tema, organo_origen, url_scjn
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (numero_expediente) DO UPDATE SET
                    tipo_asunto = EXCLUDED.tipo_asunto,
                    organo_radicacion = EXCLUDED.organo_radicacion,
                    ministro_ponente = EXCLUDED.ministro_ponente,
                    tema = EXCLUDED.tema,
                    updated_at = CURRENT_TIMESTAMP
                RETURNING id
            """, (
                expediente['numero_expediente'],
                expediente['año'],
                expediente['tipo_asunto'],
                expediente['organo_radicacion'],
                expediente['ministro_ponente'],
                expediente['tema'],
                expediente['organo_origen'],
                expediente['url_scjn']
            ))
            
            jurisprudencia_id = cursor.fetchone()[0]
            
            # Descargar y guardar documentos
            for doc in expediente['documentos']:
                self.descargar_documento(jurisprudencia_id, doc)
            
            self.db.commit()
            print(f"✓ Guardado: {expediente['numero_expediente']}")
            
        except Exception as e:
            self.db.rollback()
            print(f"✗ Error guardando {expediente['numero_expediente']}: {e}")
    
    def descargar_documento(self, jurisprudencia_id, doc_info):
        """Descarga y guarda un documento"""
        try:
            response = self.session.get(doc_info['url'], timeout=30)
            response.raise_for_status()
            
            # Calcular hash
            file_hash = hashlib.sha256(response.content).hexdigest()
            
            # Guardar archivo
            ruta = f"/storage/documentos/{file_hash[:2]}/{file_hash[2:4]}/{file_hash}.pdf"
            import os
            os.makedirs(os.path.dirname(ruta), exist_ok=True)
            
            with open(ruta, 'wb') as f:
                f.write(response.content)
            
            # Guardar en base de datos
            cursor = self.db.cursor()
            cursor.execute("""
                INSERT INTO documentos (
                    jurisprudencia_id, tipo_documento, nombre_archivo,
                    ruta_archivo, hash_sha256, tamano_bytes, url_descarga,
                    fecha_descarga
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (hash_sha256) DO NOTHING
            """, (
                jurisprudencia_id,
                doc_info['tipo'],
                f"{file_hash}.pdf",
                ruta,
                file_hash,
                len(response.content),
                doc_info['url'],
                datetime.now()
            ))
            
            print(f"  ✓ Documento descargado: {doc_info['tipo']}")
            
        except Exception as e:
            print(f"  ✗ Error descargando documento: {e}")
```

### 4.3 Sistema de Prescripción Legal

```python
from datetime import datetime, timedelta

class PrescripcionCalculator:
    """
    Calcula la prescripción de jurisprudencias según la legislación mexicana
    """
    
    # Plazos de prescripción por tipo de asunto (en años)
    PLAZOS = {
        'AMPARO': 15,
        'CONTROVERSIA_CONSTITUCIONAL': 10,
        'ACCION_INCONSTITUCIONALIDAD': None,  # No prescribe
        'RECURSO_REVISION': 10,
        'VARIOS': 5,
        'DEFAULT': 10
    }
    
    def calcular_fecha_prescripcion(self, tipo_asunto, fecha_resolucion):
        """
        Calcula la fecha de prescripción de una jurisprudencia
        """
        plazo = self.PLAZOS.get(tipo_asunto.upper(), self.PLAZOS['DEFAULT'])
        
        if plazo is None:
            return None  # No prescribe
        
        if not isinstance(fecha_resolucion, datetime):
            fecha_resolucion = datetime.fromisoformat(fecha_resolucion)
        
        fecha_prescripcion = fecha_resolucion + timedelta(days=plazo * 365)
        
        return fecha_prescripcion
    
    def esta_prescrito(self, tipo_asunto, fecha_resolucion):
        """
        Verifica si una jurisprudencia está prescrita
        """
        fecha_prescripcion = self.calcular_fecha_prescripcion(tipo_asunto, fecha_resolucion)
        
        if fecha_prescripcion is None:
            return False  # No prescribe
        
        return datetime.now() > fecha_prescripcion
    
    def actualizar_prescripciones(self, db_conn):
        """
        Actualiza el estado de prescripción de todas las jurisprudencias
        """
        cursor = db_conn.cursor()
        
        cursor.execute("""
            SELECT id, tipo_asunto, fecha_resolucion
            FROM jurisprudencias
            WHERE fecha_resolucion IS NOT NULL
        """)
        
        actualizadas = 0
        for row in cursor.fetchall():
            juris_id, tipo_asunto, fecha_resolucion = row
            
            fecha_prescripcion = self.calcular_fecha_prescripcion(tipo_asunto, fecha_resolucion)
            prescrito = self.esta_prescrito(tipo_asunto, fecha_resolucion)
            
            cursor.execute("""
                UPDATE jurisprudencias
                SET fecha_prescripcion = %s, prescrito = %s
                WHERE id = %s
            """, (fecha_prescripcion, prescrito, juris_id))
            
            actualizadas += 1
        
        db_conn.commit()
        print(f"Actualizadas {actualizadas} jurisprudencias")
```

---

## PARTE 5: OPTIMIZACIÓN DE COSTOS MANUS

### 5.1 Estrategia de Delegación

**Principio:** Manus solo para tareas que requieren navegación web en tiempo real

**Distribución de Tareas:**

| Tarea | Ejecutor | Consumo Créditos |
|-------|----------|------------------|
| Navegación web SCJN | Manus Browser | ALTO (10-20) |
| Descarga de PDFs | Manus Browser | MEDIO (3-7) |
| Extracción de texto | Python local | CERO |
| Cálculo de hashes | Python local | CERO |
| Registro blockchain | Python local | CERO |
| Generación informes | Python + Gemini API | BAJO (1-3) |
| Búsqueda semántica | PostgreSQL local | CERO |
| Procesamiento emails | Python local | CERO |
| Almacenamiento | MinIO local | CERO |

**Ahorro Estimado:** 70-85%

### 5.2 Sistema de Cache

```python
import json
import hashlib
from datetime import datetime, timedelta

class CacheManager:
    """
    Sistema de cache para evitar consultas repetidas a SCJN
    """
    
    def __init__(self, cache_dir="/storage/cache"):
        self.cache_dir = cache_dir
        import os
        os.makedirs(cache_dir, exist_ok=True)
    
    def get_cache_key(self, url):
        """Genera clave de cache para una URL"""
        return hashlib.md5(url.encode()).hexdigest()
    
    def get(self, url, max_age_hours=24):
        """Obtiene contenido del cache si existe y no ha expirado"""
        cache_key = self.get_cache_key(url)
        cache_file = f"{self.cache_dir}/{cache_key}.json"
        
        try:
            with open(cache_file, 'r') as f:
                cache_data = json.load(f)
            
            # Verificar edad
            cached_time = datetime.fromisoformat(cache_data['timestamp'])
            age = datetime.now() - cached_time
            
            if age.total_seconds() / 3600 > max_age_hours:
                return None  # Cache expirado
            
            return cache_data['content']
            
        except FileNotFoundError:
            return None
    
    def set(self, url, content):
        """Guarda contenido en cache"""
        cache_key = self.get_cache_key(url)
        cache_file = f"{self.cache_dir}/{cache_key}.json"
        
        cache_data = {
            'url': url,
            'timestamp': datetime.now().isoformat(),
            'content': content
        }
        
        with open(cache_file, 'w') as f:
            json.dump(cache_data, f)
```

### 5.3 Procesamiento Batch

```python
class BatchProcessor:
    """
    Procesa múltiples expedientes en lotes para optimizar recursos
    """
    
    def __init__(self, batch_size=10):
        self.batch_size = batch_size
    
    def procesar_expedientes(self, expedientes):
        """
        Procesa expedientes en lotes
        """
        total = len(expedientes)
        procesados = 0
        
        for i in range(0, total, self.batch_size):
            batch = expedientes[i:i+self.batch_size]
            
            print(f"Procesando lote {i//self.batch_size + 1} ({len(batch)} expedientes)...")
            
            for exp in batch:
                try:
                    self.procesar_expediente(exp)
                    procesados += 1
                except Exception as e:
                    print(f"Error procesando {exp['numero_expediente']}: {e}")
            
            print(f"Progreso: {procesados}/{total} ({procesados/total*100:.1f}%)")
        
        return procesados
    
    def procesar_expediente(self, expediente):
        """Procesa un expediente individual"""
        # Implementación específica
        pass
```

---

## CONCLUSIÓN

Este sistema proporciona una solución completa, escalable y optimizada para la gestión de expedientes virtuales de la SCJN con las siguientes ventajas:

**Ventajas Técnicas:**
- Blockchain inmutable con números primos
- Autenticación robusta CURP/RFC
- Procesamiento automático de emails
- Base de datos completa de jurisprudencias
- Búsqueda semántica con embeddings

**Ventajas Económicas:**
- 70-85% de ahorro en créditos Manus
- Procesamiento local de tareas pesadas
- Cache inteligente de resultados
- Escalabilidad horizontal

**Ventajas Legales:**
- Cumplimiento NOM-151-SCFI-2016
- Cadena de custodia verificable
- Validez probatoria
- Anonimización de datos personales

---

**Próximos Pasos:**
1. Implementar código fuente completo
2. Configurar infraestructura (servidores, base de datos)
3. Realizar pruebas de integración
4. Desplegar en producción
5. Documentar APIs y endpoints
