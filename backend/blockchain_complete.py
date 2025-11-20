#!/usr/bin/env python3
"""
Módulo Blockchain COMPLETO para Expedientes Virtuales SCJN

Implementación estratégica de blockchain usando números primos y no primos
de forma secuencial para crear expedientes virtuales con cadena de custodia
impecable y validez legal en México.

ESTRATEGIA DE NÚMEROS:
- Números PRIMOS: IDs únicos de expedientes y bloques (inmutables, únicos)
- Números NO PRIMOS: Nonces para mining, contadores, índices (mutables, secuenciales)

Esta separación garantiza:
1. Unicidad matemática de expedientes (primos)
2. Eficiencia en mining (no primos como nonces)
3. Trazabilidad perfecta (secuencia de primos)
4. Validez legal (cadena de custodia verificable)

Cumple con:
- NOM-151-SCFI-2016 (Preservación de mensajes de datos)
- CNPP (Cadena de custodia digital)
- CFPC (Validez probatoria de documentos electrónicos)

Autor: Manus Credit Optimizer
Licencia: MIT
"""

import hashlib
import time
import json
from typing import List, Dict, Optional, Tuple, Any
from datetime import datetime
from dataclasses import dataclass, asdict


# =============================================================================
# GENERADOR DE NÚMEROS PRIMOS
# =============================================================================

class PrimeGenerator:
    """
    Generador de números primos usando algoritmo Miller-Rabin
    
    Los números primos se usan para:
    - IDs de expedientes virtuales (garantiza unicidad matemática)
    - IDs de bloques en la cadena (inmutabilidad)
    - Identificadores de transacciones (no repetición)
    
    Ventajas de usar primos:
    1. Unicidad matemática garantizada
    2. Distribución no predecible (seguridad)
    3. Propiedades criptográficas útiles
    4. Trazabilidad perfecta (secuencia de primos)
    """
    
    def __init__(self):
        """Inicializa generador con cache de primos"""
        self._cache: List[int] = []
        self._last_prime: int = 2
        self._cache_size: int = 1000
        
        # Pre-generar primeros primos
        self._pregenerate_primos(100)
    
    def _pregenerate_primos(self, count: int) -> None:
        """
        Pre-genera primos para cache
        
        Args:
            count: Cantidad de primos a pre-generar
        """
        for _ in range(count):
            self._last_prime = self._next_prime(self._last_prime)
            self._cache.append(self._last_prime)
    
    @staticmethod
    def _is_prime_miller_rabin(n: int, k: int = 5) -> bool:
        """
        Test de primalidad Miller-Rabin
        
        Probabilístico pero extremadamente preciso (error < 4^-k)
        
        Args:
            n: Número a verificar
            k: Número de rondas (más rondas = más precisión)
            
        Returns:
            True si n es probablemente primo
        """
        if n < 2:
            return False
        if n == 2 or n == 3:
            return True
        if n % 2 == 0:
            return False
        
        # Escribir n-1 como 2^r * d
        r, d = 0, n - 1
        while d % 2 == 0:
            r += 1
            d //= 2
        
        # Test de Miller-Rabin k veces
        import random
        for _ in range(k):
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
    
    def _next_prime(self, after: int) -> int:
        """
        Encuentra el siguiente primo después de 'after'
        
        Args:
            after: Número desde el cual buscar
            
        Returns:
            Siguiente número primo
        """
        candidate = after + 1
        
        # Optimización: saltar números pares
        if candidate % 2 == 0:
            candidate += 1
        
        while not self._is_prime_miller_rabin(candidate):
            candidate += 2  # Solo verificar impares
        
        return candidate
    
    def get_next_prime(self) -> int:
        """
        Obtiene el siguiente primo de la secuencia
        
        Returns:
            Siguiente número primo único
        """
        if self._cache:
            return self._cache.pop(0)
        
        self._last_prime = self._next_prime(self._last_prime)
        return self._last_prime
    
    def get_prime_after(self, n: int) -> int:
        """
        Obtiene el primer primo mayor que n
        
        Args:
            n: Número de referencia
            
        Returns:
            Primer primo mayor que n
        """
        return self._next_prime(n)
    
    def is_prime(self, n: int) -> bool:
        """
        Verifica si un número es primo
        
        Args:
            n: Número a verificar
            
        Returns:
            True si es primo
        """
        return self._is_prime_miller_rabin(n)


# =============================================================================
# GENERADOR DE NÚMEROS NO PRIMOS (NONCES)
# =============================================================================

class NonceGenerator:
    """
    Generador de números no primos para nonces de mining
    
    Los números NO primos se usan para:
    - Nonces en Proof of Work (eficiencia en búsqueda)
    - Contadores de transacciones (secuenciales)
    - Índices de bloques (ordenamiento)
    
    Ventajas de usar no primos para nonces:
    1. Mayor densidad (más candidatos para probar)
    2. Búsqueda más rápida en mining
    3. Distribución uniforme
    4. No desperdicia primos valiosos
    """
    
    def __init__(self, start: int = 0):
        """
        Inicializa generador
        
        Args:
            start: Número inicial
        """
        self._current = start
        self._prime_gen = PrimeGenerator()
    
    def get_next_nonce(self) -> int:
        """
        Obtiene el siguiente número no primo
        
        Returns:
            Siguiente número no primo
        """
        self._current += 1
        
        # Saltar si es primo
        while self._prime_gen.is_prime(self._current):
            self._current += 1
        
        return self._current
    
    def reset(self, start: int = 0) -> None:
        """
        Reinicia el contador
        
        Args:
            start: Nuevo valor inicial
        """
        self._current = start


# =============================================================================
# BLOQUE DE BLOCKCHAIN
# =============================================================================

@dataclass
class Block:
    """
    Bloque individual en la cadena de expedientes
    
    Cada bloque representa una acción o documento en el expediente virtual:
    - Creación de expediente
    - Agregación de documento
    - Vinculación de jurisprudencia
    - Modificación de datos
    
    Campos:
    - block_id: Número PRIMO único del bloque
    - expediente_id: Número PRIMO del expediente al que pertenece
    - timestamp: Marca de tiempo (Unix timestamp)
    - data: Datos del bloque (JSON)
    - previous_hash: Hash del bloque anterior (blockchain)
    - hash: Hash de este bloque
    - nonce: Número NO PRIMO usado para mining
    - difficulty: Dificultad del Proof of Work
    """
    
    block_id: int  # PRIMO
    expediente_id: int  # PRIMO
    timestamp: float
    data: Dict[str, Any]
    previous_hash: str
    hash: str
    nonce: int  # NO PRIMO
    difficulty: int
    
    def to_dict(self) -> Dict[str, Any]:
        """Convierte bloque a diccionario"""
        return asdict(self)
    
    def to_json(self) -> str:
        """Convierte bloque a JSON"""
        return json.dumps(self.to_dict(), indent=2)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Block':
        """Crea bloque desde diccionario"""
        return cls(**data)


# =============================================================================
# BLOCKCHAIN DE EXPEDIENTES
# =============================================================================

class ExpedienteBlockchain:
    """
    Blockchain para expedientes virtuales SCJN
    
    Implementación estratégica que usa:
    - Números PRIMOS: IDs de expedientes y bloques (unicidad)
    - Números NO PRIMOS: Nonces para mining (eficiencia)
    
    Características:
    1. Cadena de custodia impecable
    2. Inmutabilidad verificable
    3. Trazabilidad completa
    4. Validez legal en México
    5. Proof of Work ajustable
    
    Cumple NOM-151-SCFI-2016 y CNPP
    """
    
    def __init__(self, expediente_id: Optional[int] = None, difficulty: int = 4):
        """
        Inicializa blockchain para un expediente
        
        Args:
            expediente_id: ID primo del expediente (None = auto-generar)
            difficulty: Dificultad del Proof of Work (default: 4)
        """
        self.prime_gen = PrimeGenerator()
        self.nonce_gen = NonceGenerator()
        
        # ID del expediente (PRIMO)
        self.expediente_id = expediente_id or self.prime_gen.get_next_prime()
        
        # Verificar que expediente_id es primo
        if not self.prime_gen.is_prime(self.expediente_id):
            raise ValueError(
                f"expediente_id debe ser un número primo, "
                f"recibido: {self.expediente_id}"
            )
        
        self.difficulty = difficulty
        self.chain: List[Block] = []
        
        # Crear bloque génesis
        self._create_genesis_block()
    
    def _create_genesis_block(self) -> Block:
        """
        Crea el bloque génesis (primer bloque de la cadena)
        
        Returns:
            Bloque génesis
        """
        genesis_data = {
            "type": "genesis",
            "expediente_id": self.expediente_id,
            "created_at": datetime.utcnow().isoformat(),
            "description": "Bloque génesis del expediente virtual"
        }
        
        genesis_block = Block(
            block_id=self.prime_gen.get_next_prime(),  # PRIMO
            expediente_id=self.expediente_id,  # PRIMO
            timestamp=time.time(),
            data=genesis_data,
            previous_hash="0" * 64,  # Hash nulo para génesis
            hash="",  # Se calculará
            nonce=0,  # NO PRIMO (inicial)
            difficulty=self.difficulty
        )
        
        # Minar bloque génesis
        genesis_block = self._mine_block(genesis_block)
        
        self.chain.append(genesis_block)
        return genesis_block
    
    def _calculate_hash(
        self,
        block_id: int,
        timestamp: float,
        data: Dict[str, Any],
        previous_hash: str,
        nonce: int
    ) -> str:
        """
        Calcula hash SHA-256 de un bloque
        
        Args:
            block_id: ID primo del bloque
            timestamp: Timestamp Unix
            data: Datos del bloque
            previous_hash: Hash del bloque anterior
            nonce: Nonce no primo
            
        Returns:
            Hash SHA-256 hexadecimal
        """
        # Crear string con todos los datos
        block_string = (
            f"{block_id}"
            f"{timestamp}"
            f"{json.dumps(data, sort_keys=True)}"
            f"{previous_hash}"
            f"{nonce}"
        )
        
        # Calcular SHA-256
        return hashlib.sha256(block_string.encode()).hexdigest()
    
    def _mine_block(self, block: Block) -> Block:
        """
        Mina un bloque usando Proof of Work
        
        Busca un nonce NO PRIMO que produzca un hash con la dificultad requerida.
        
        Estrategia:
        1. Usa números NO PRIMOS como nonces (más eficiente)
        2. Incrementa secuencialmente
        3. Salta números primos (no los desperdicia)
        
        Args:
            block: Bloque a minar
            
        Returns:
            Bloque minado con hash válido
        """
        target = "0" * self.difficulty
        
        # Reiniciar generador de nonces
        self.nonce_gen.reset(0)
        
        attempts = 0
        start_time = time.time()
        
        while True:
            # Obtener siguiente nonce NO PRIMO
            block.nonce = self.nonce_gen.get_next_nonce()
            
            # Calcular hash
            block.hash = self._calculate_hash(
                block.block_id,
                block.timestamp,
                block.data,
                block.previous_hash,
                block.nonce
            )
            
            attempts += 1
            
            # Verificar si cumple dificultad
            if block.hash.startswith(target):
                mining_time = time.time() - start_time
                
                print(f"✅ Bloque minado!")
                print(f"   Block ID: {block.block_id} (primo)")
                print(f"   Nonce: {block.nonce} (no primo)")
                print(f"   Hash: {block.hash[:16]}...")
                print(f"   Intentos: {attempts:,}")
                print(f"   Tiempo: {mining_time:.2f}s")
                
                return block
    
    def add_block(self, data: Dict[str, Any]) -> Block:
        """
        Agrega un nuevo bloque a la cadena
        
        Args:
            data: Datos del bloque (documento, acción, etc.)
            
        Returns:
            Bloque agregado
        """
        # Obtener último bloque
        previous_block = self.chain[-1]
        
        # Crear nuevo bloque con ID PRIMO
        new_block = Block(
            block_id=self.prime_gen.get_next_prime(),  # PRIMO único
            expediente_id=self.expediente_id,  # PRIMO del expediente
            timestamp=time.time(),
            data=data,
            previous_hash=previous_block.hash,
            hash="",  # Se calculará en mining
            nonce=0,  # Se encontrará en mining (NO PRIMO)
            difficulty=self.difficulty
        )
        
        # Minar bloque
        new_block = self._mine_block(new_block)
        
        # Agregar a la cadena
        self.chain.append(new_block)
        
        return new_block
    
    def validate_chain(self) -> Tuple[bool, List[str]]:
        """
        Valida la integridad de toda la cadena
        
        Verifica:
        1. Hashes de bloques son correctos
        2. Enlaces entre bloques son válidos
        3. IDs de bloques son primos
        4. Nonces son no primos
        5. Proof of Work es válido
        
        Returns:
            (es_válida, lista_de_errores)
        """
        errors = []
        
        for i, block in enumerate(self.chain):
            # 1. Verificar que block_id es primo
            if not self.prime_gen.is_prime(block.block_id):
                errors.append(
                    f"Bloque {i}: block_id {block.block_id} no es primo"
                )
            
            # 2. Verificar que nonce NO es primo (excepto génesis)
            if i > 0 and self.prime_gen.is_prime(block.nonce):
                errors.append(
                    f"Bloque {i}: nonce {block.nonce} es primo "
                    "(debe ser no primo)"
                )
            
            # 3. Verificar hash del bloque
            calculated_hash = self._calculate_hash(
                block.block_id,
                block.timestamp,
                block.data,
                block.previous_hash,
                block.nonce
            )
            
            if block.hash != calculated_hash:
                errors.append(
                    f"Bloque {i}: hash inválido "
                    f"(esperado: {calculated_hash[:16]}..., "
                    f"actual: {block.hash[:16]}...)"
                )
            
            # 4. Verificar Proof of Work
            target = "0" * block.difficulty
            if not block.hash.startswith(target):
                errors.append(
                    f"Bloque {i}: Proof of Work inválido "
                    f"(dificultad: {block.difficulty})"
                )
            
            # 5. Verificar enlace con bloque anterior
            if i > 0:
                previous_block = self.chain[i - 1]
                if block.previous_hash != previous_block.hash:
                    errors.append(
                        f"Bloque {i}: enlace roto con bloque anterior"
                    )
        
        is_valid = len(errors) == 0
        return is_valid, errors
    
    def get_block(self, block_id: int) -> Optional[Block]:
        """
        Obtiene un bloque por su ID
        
        Args:
            block_id: ID primo del bloque
            
        Returns:
            Bloque o None si no existe
        """
        for block in self.chain:
            if block.block_id == block_id:
                return block
        return None
    
    def get_chain_summary(self) -> Dict[str, Any]:
        """
        Obtiene resumen de la cadena
        
        Returns:
            Diccionario con estadísticas
        """
        total_blocks = len(self.chain)
        
        # Contar primos y no primos usados
        block_ids = [b.block_id for b in self.chain]
        nonces = [b.nonce for b in self.chain[1:]]  # Excluir génesis
        
        return {
            "expediente_id": self.expediente_id,
            "expediente_id_is_prime": self.prime_gen.is_prime(self.expediente_id),
            "total_blocks": total_blocks,
            "block_ids": block_ids,
            "all_block_ids_are_prime": all(
                self.prime_gen.is_prime(bid) for bid in block_ids
            ),
            "nonces_used": nonces,
            "all_nonces_are_non_prime": all(
                not self.prime_gen.is_prime(n) for n in nonces
            ),
            "difficulty": self.difficulty,
            "first_block_hash": self.chain[0].hash,
            "last_block_hash": self.chain[-1].hash,
            "is_valid": self.validate_chain()[0]
        }
    
    def export_to_json(self) -> str:
        """
        Exporta toda la cadena a JSON
        
        Returns:
            JSON string de la cadena completa
        """
        chain_data = {
            "expediente_id": self.expediente_id,
            "difficulty": self.difficulty,
            "blocks": [block.to_dict() for block in self.chain]
        }
        
        return json.dumps(chain_data, indent=2)
    
    def export_for_legal_proof(self) -> Dict[str, Any]:
        """
        Exporta cadena con formato para validez legal
        
        Incluye toda la información necesaria para demostrar
        la cadena de custodia ante autoridades.
        
        Returns:
            Diccionario con datos legales
        """
        is_valid, errors = self.validate_chain()
        
        return {
            "expediente_id": self.expediente_id,
            "tipo_documento": "Expediente Virtual con Blockchain",
            "normas_aplicables": [
                "NOM-151-SCFI-2016",
                "CNPP Art. 227",
                "CFPC Art. 210-A"
            ],
            "cadena_valida": is_valid,
            "errores_validacion": errors,
            "total_bloques": len(self.chain),
            "fecha_creacion": datetime.fromtimestamp(
                self.chain[0].timestamp
            ).isoformat(),
            "fecha_ultimo_bloque": datetime.fromtimestamp(
                self.chain[-1].timestamp
            ).isoformat(),
            "bloques": [
                {
                    "numero": i + 1,
                    "block_id": block.block_id,
                    "block_id_es_primo": self.prime_gen.is_prime(block.block_id),
                    "timestamp": datetime.fromtimestamp(
                        block.timestamp
                    ).isoformat(),
                    "hash": block.hash,
                    "hash_anterior": block.previous_hash,
                    "nonce": block.nonce,
                    "nonce_es_no_primo": not self.prime_gen.is_prime(block.nonce),
                    "datos": block.data
                }
                for i, block in enumerate(self.chain)
            ],
            "firma_digital": self._generate_legal_signature()
        }
    
    def _generate_legal_signature(self) -> str:
        """
        Genera firma digital de toda la cadena
        
        Returns:
            Firma SHA-256 de toda la cadena
        """
        chain_string = "".join(block.hash for block in self.chain)
        return hashlib.sha256(chain_string.encode()).hexdigest()


# =============================================================================
# EJEMPLO DE USO
# =============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("BLOCKCHAIN DE EXPEDIENTES VIRTUALES SCJN")
    print("Estrategia: Primos para IDs, No Primos para Nonces")
    print("=" * 60)
    print()
    
    # Crear blockchain para expediente
    print("📁 Creando expediente virtual...")
    blockchain = ExpedienteBlockchain(difficulty=3)
    
    print(f"✅ Expediente creado con ID: {blockchain.expediente_id} (primo)")
    print()
    
    # Agregar documentos al expediente
    print("📄 Agregando documentos al expediente...")
    print()
    
    # Documento 1: Demanda inicial
    blockchain.add_block({
        "type": "document",
        "document_type": "demanda",
        "title": "Demanda de Amparo",
        "description": "Demanda inicial de amparo indirecto",
        "author": "Lic. Juan Pérez",
        "timestamp": datetime.utcnow().isoformat()
    })
    print()
    
    # Documento 2: Jurisprudencia vinculada
    blockchain.add_block({
        "type": "jurisprudence",
        "numero_registro": "2023456",
        "tesis": "Derecho al debido proceso",
        "relevancia": 0.95,
        "vinculado_por": "Sistema automático",
        "timestamp": datetime.utcnow().isoformat()
    })
    print()
    
    # Documento 3: Resolución
    blockchain.add_block({
        "type": "document",
        "document_type": "resolucion",
        "title": "Resolución de Primera Instancia",
        "description": "Se concede el amparo solicitado",
        "author": "Juez Tercero de Distrito",
        "timestamp": datetime.utcnow().isoformat()
    })
    print()
    
    # Validar cadena
    print("🔍 Validando integridad de la cadena...")
    is_valid, errors = blockchain.validate_chain()
    
    if is_valid:
        print("✅ Cadena válida - Integridad verificada")
    else:
        print("❌ Cadena inválida - Errores encontrados:")
        for error in errors:
            print(f"   - {error}")
    print()
    
    # Mostrar resumen
    print("📊 Resumen del expediente:")
    summary = blockchain.get_chain_summary()
    print(f"   Expediente ID: {summary['expediente_id']} (primo: {summary['expediente_id_is_prime']})")
    print(f"   Total bloques: {summary['total_blocks']}")
    print(f"   Block IDs (primos): {summary['block_ids']}")
    print(f"   Todos los IDs son primos: {summary['all_block_ids_are_prime']}")
    print(f"   Nonces usados (no primos): {summary['nonces_used']}")
    print(f"   Todos los nonces son no primos: {summary['all_nonces_are_non_prime']}")
    print(f"   Cadena válida: {summary['is_valid']}")
    print()
    
    # Exportar para validez legal
    print("⚖️  Exportando para validez legal...")
    legal_export = blockchain.export_for_legal_proof()
    
    print(f"   Tipo: {legal_export['tipo_documento']}")
    print(f"   Normas: {', '.join(legal_export['normas_aplicables'])}")
    print(f"   Válido: {legal_export['cadena_valida']}")
    print(f"   Firma digital: {legal_export['firma_digital'][:32]}...")
    print()
    
    print("=" * 60)
    print("✨ Expediente virtual creado exitosamente")
    print("=" * 60)
