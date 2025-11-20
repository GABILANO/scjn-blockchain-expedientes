#!/usr/bin/env python3
"""
Sistema de Blockchain con Números Primos
Implementación optimizada para expedientes virtuales
"""

import hashlib
import json
import random
from datetime import datetime
from typing import Dict, List, Optional, Tuple
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class PrimeNumberGenerator:
    """
    Generador de números primos usando Miller-Rabin
    """
    
    @staticmethod
    def is_prime(n: int, k: int = 5) -> bool:
        """
        Test de primalidad de Miller-Rabin
        k: número de rondas (mayor = más preciso)
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
        
        # Test de Miller-Rabin
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
    
    @staticmethod
    def next_prime(n: int) -> int:
        """Encuentra el siguiente número primo después de n"""
        if n < 2:
            return 2
        
        candidate = n + 1
        
        # Saltar números pares
        if candidate % 2 == 0:
            candidate += 1
        
        while not PrimeNumberGenerator.is_prime(candidate):
            candidate += 2
        
        return candidate
    
    @staticmethod
    def generate_prime_from_hash(hash_str: str) -> int:
        """Genera un número primo a partir de un hash"""
        # Tomar primeros 16 caracteres del hash
        hash_part = hash_str[:16]
        
        # Convertir a número
        num = int(hash_part, 16)
        
        # Encontrar siguiente primo
        return PrimeNumberGenerator.next_prime(num)


class Block:
    """
    Bloque individual en la blockchain
    """
    
    def __init__(
        self,
        block_id: int,
        block_type: str,
        timestamp: str,
        previous_hash: str,
        data: Dict,
        nonce: int = 0,
        hash_value: str = None
    ):
        self.block_id = block_id
        self.block_type = block_type  # "prime" o "composite"
        self.timestamp = timestamp
        self.previous_hash = previous_hash
        self.data = data
        self.nonce = nonce
        self.hash = hash_value or self.calculate_hash()
    
    def calculate_hash(self) -> str:
        """Calcula el hash del bloque"""
        block_string = json.dumps({
            'block_id': self.block_id,
            'block_type': self.block_type,
            'timestamp': self.timestamp,
            'previous_hash': self.previous_hash,
            'data': self.data,
            'nonce': self.nonce
        }, sort_keys=True)
        
        return hashlib.sha256(block_string.encode()).hexdigest()
    
    def mine_block(self, difficulty: int = 4) -> None:
        """
        Mina el bloque con Proof-of-Work
        difficulty: número de ceros iniciales requeridos
        """
        target = "0" * difficulty
        
        logger.info(f"Minando bloque {self.block_id} (dificultad: {difficulty})...")
        
        while not self.hash.startswith(target):
            self.nonce += 1
            self.hash = self.calculate_hash()
            
            # Límite de seguridad
            if self.nonce > 10_000_000:
                raise Exception("PoW timeout - ajustar dificultad")
        
        logger.info(f"✓ Bloque minado: {self.hash} (nonce: {self.nonce})")
    
    def to_dict(self) -> Dict:
        """Convierte el bloque a diccionario"""
        return {
            'block_id': self.block_id,
            'block_type': self.block_type,
            'timestamp': self.timestamp,
            'previous_hash': self.previous_hash,
            'data': self.data,
            'nonce': self.nonce,
            'hash': self.hash
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Block':
        """Crea un bloque desde un diccionario"""
        return cls(
            block_id=data['block_id'],
            block_type=data['block_type'],
            timestamp=data['timestamp'],
            previous_hash=data['previous_hash'],
            data=data['data'],
            nonce=data['nonce'],
            hash_value=data['hash']
        )


class Blockchain:
    """
    Blockchain con sistema de números primos
    """
    
    def __init__(self, difficulty: int = 4):
        self.chain: List[Block] = []
        self.difficulty = difficulty
        self.prime_generator = PrimeNumberGenerator()
        
        # Crear bloque génesis
        self.create_genesis_block()
    
    def create_genesis_block(self) -> None:
        """Crea el bloque génesis"""
        genesis_data = {
            'tipo': 'genesis',
            'mensaje': 'Bloque Génesis - Sistema de Expedientes Virtuales SCJN',
            'version': '1.0.0',
            'fecha': datetime.now().isoformat()
        }
        
        genesis_block = Block(
            block_id=2,  # Primer número primo
            block_type='prime',
            timestamp=datetime.now().isoformat(),
            previous_hash='0',
            data=genesis_data
        )
        
        genesis_block.mine_block(self.difficulty)
        self.chain.append(genesis_block)
        
        logger.info("✓ Bloque génesis creado")
    
    def get_latest_block(self) -> Block:
        """Obtiene el último bloque de la cadena"""
        return self.chain[-1]
    
    def generate_block_id(self, user_hash: str, document_hash: str) -> Tuple[int, str]:
        """
        Genera ID de bloque usando números primos
        """
        # Combinar hashes
        combined = f"{user_hash}{document_hash}{datetime.now().isoformat()}"
        combined_hash = hashlib.sha256(combined.encode()).hexdigest()
        
        # Generar número primo
        block_id = self.prime_generator.generate_prime_from_hash(combined_hash)
        
        # Determinar tipo
        block_type = "prime" if self.prime_generator.is_prime(block_id) else "composite"
        
        return block_id, block_type
    
    def add_block(self, data: Dict, user_hash: str = None, document_hash: str = None) -> Block:
        """
        Añade un nuevo bloque a la cadena
        """
        previous_block = self.get_latest_block()
        
        # Generar ID de bloque
        if user_hash and document_hash:
            block_id, block_type = self.generate_block_id(user_hash, document_hash)
        else:
            # Usar siguiente primo del último bloque
            block_id = self.prime_generator.next_prime(previous_block.block_id)
            block_type = "prime"
        
        # Crear nuevo bloque
        new_block = Block(
            block_id=block_id,
            block_type=block_type,
            timestamp=datetime.now().isoformat(),
            previous_hash=previous_block.hash,
            data=data
        )
        
        # Minar bloque
        new_block.mine_block(self.difficulty)
        
        # Añadir a la cadena
        self.chain.append(new_block)
        
        logger.info(f"✓ Bloque añadido: #{block_id} ({block_type})")
        
        return new_block
    
    def is_valid(self) -> Tuple[bool, str]:
        """
        Valida la integridad de la blockchain
        """
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]
            
            # Verificar hash del bloque
            if current_block.hash != current_block.calculate_hash():
                return False, f"Hash inválido en bloque {current_block.block_id}"
            
            # Verificar enlace con bloque anterior
            if current_block.previous_hash != previous_block.hash:
                return False, f"Cadena rota en bloque {current_block.block_id}"
            
            # Verificar proof-of-work
            target = "0" * self.difficulty
            if not current_block.hash.startswith(target):
                return False, f"PoW inválido en bloque {current_block.block_id}"
        
        return True, "Blockchain válida"
    
    def get_block_by_id(self, block_id: int) -> Optional[Block]:
        """Busca un bloque por su ID"""
        for block in self.chain:
            if block.block_id == block_id:
                return block
        return None
    
    def get_blocks_by_user(self, user_hash: str) -> List[Block]:
        """Obtiene todos los bloques de un usuario"""
        blocks = []
        for block in self.chain:
            if block.data.get('user_hash') == user_hash:
                blocks.append(block)
        return blocks
    
    def export_to_json(self, filepath: str) -> None:
        """Exporta la blockchain a JSON"""
        data = {
            'version': '1.0.0',
            'difficulty': self.difficulty,
            'chain_length': len(self.chain),
            'created_at': self.chain[0].timestamp,
            'last_updated': datetime.now().isoformat(),
            'blocks': [block.to_dict() for block in self.chain]
        }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        logger.info(f"✓ Blockchain exportada a {filepath}")
    
    def import_from_json(self, filepath: str) -> None:
        """Importa blockchain desde JSON"""
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        self.difficulty = data['difficulty']
        self.chain = [Block.from_dict(block_data) for block_data in data['blocks']]
        
        logger.info(f"✓ Blockchain importada desde {filepath}")
        
        # Validar integridad
        valida, mensaje = self.is_valid()
        if valida:
            logger.info("✓ Blockchain válida")
        else:
            logger.error(f"✗ Blockchain inválida: {mensaje}")
    
    def get_stats(self) -> Dict:
        """Obtiene estadísticas de la blockchain"""
        prime_blocks = sum(1 for block in self.chain if block.block_type == 'prime')
        composite_blocks = len(self.chain) - prime_blocks
        
        return {
            'total_blocks': len(self.chain),
            'prime_blocks': prime_blocks,
            'composite_blocks': composite_blocks,
            'difficulty': self.difficulty,
            'genesis_timestamp': self.chain[0].timestamp,
            'latest_timestamp': self.chain[-1].timestamp,
            'is_valid': self.is_valid()[0]
        }


class ExpedienteBlockchain:
    """
    Blockchain especializada para expedientes virtuales
    """
    
    def __init__(self, difficulty: int = 4):
        self.blockchain = Blockchain(difficulty)
    
    def registrar_expediente(
        self,
        user_hash: str,
        curp_hash: str,
        rfc_hash: str,
        email_personalizado: str
    ) -> Block:
        """Registra un nuevo expediente virtual"""
        data = {
            'tipo': 'registro_expediente',
            'user_hash': user_hash,
            'curp_hash': curp_hash,
            'rfc_hash': rfc_hash,
            'email_personalizado': email_personalizado,
            'fecha_registro': datetime.now().isoformat()
        }
        
        return self.blockchain.add_block(data, user_hash, curp_hash)
    
    def registrar_documento(
        self,
        user_hash: str,
        documento_hash: str,
        nombre_documento: str,
        origen_email: str,
        asunto_email: str,
        tamano_bytes: int
    ) -> Block:
        """Registra un documento en el expediente"""
        data = {
            'tipo': 'documento',
            'user_hash': user_hash,
            'documento_hash': documento_hash,
            'nombre_documento': nombre_documento,
            'origen_email': origen_email,
            'asunto_email': asunto_email,
            'tamano_bytes': tamano_bytes,
            'fecha_recepcion': datetime.now().isoformat()
        }
        
        return self.blockchain.add_block(data, user_hash, documento_hash)
    
    def registrar_jurisprudencia(
        self,
        numero_expediente: str,
        año: int,
        tipo_asunto: str,
        documento_hash: str,
        url_scjn: str
    ) -> Block:
        """Registra una jurisprudencia de la SCJN"""
        data = {
            'tipo': 'jurisprudencia',
            'numero_expediente': numero_expediente,
            'año': año,
            'tipo_asunto': tipo_asunto,
            'documento_hash': documento_hash,
            'url_scjn': url_scjn,
            'fecha_registro': datetime.now().isoformat()
        }
        
        return self.blockchain.add_block(data, numero_expediente, documento_hash)
    
    def verificar_documento(self, documento_hash: str) -> Tuple[bool, Optional[Block]]:
        """Verifica si un documento está registrado en la blockchain"""
        for block in self.blockchain.chain:
            if block.data.get('documento_hash') == documento_hash:
                return True, block
        
        return False, None
    
    def obtener_expediente_usuario(self, user_hash: str) -> List[Block]:
        """Obtiene todos los bloques de un usuario"""
        return self.blockchain.get_blocks_by_user(user_hash)
    
    def generar_cadena_custodia(self, user_hash: str) -> Dict:
        """Genera cadena de custodia para un usuario"""
        bloques = self.obtener_expediente_usuario(user_hash)
        
        cadena = {
            'user_hash': user_hash,
            'total_documentos': len(bloques),
            'fecha_generacion': datetime.now().isoformat(),
            'blockchain_valida': self.blockchain.is_valid()[0],
            'documentos': []
        }
        
        for block in bloques:
            if block.data.get('tipo') == 'documento':
                cadena['documentos'].append({
                    'block_id': block.block_id,
                    'documento_hash': block.data['documento_hash'],
                    'nombre': block.data['nombre_documento'],
                    'fecha': block.data['fecha_recepcion'],
                    'block_hash': block.hash
                })
        
        return cadena


def main():
    """Función de prueba"""
    print("═══════════════════════════════════════════════════")
    print("SISTEMA DE BLOCKCHAIN CON NÚMEROS PRIMOS")
    print("═══════════════════════════════════════════════════\n")
    
    # Crear blockchain
    exp_blockchain = ExpedienteBlockchain(difficulty=3)
    
    # Registrar expediente
    print("Registrando expediente virtual...")
    block1 = exp_blockchain.registrar_expediente(
        user_hash="abc123def456",
        curp_hash="hash_curp_123",
        rfc_hash="hash_rfc_456",
        email_personalizado="abc123def456@scjn-expedientes.mx"
    )
    print(f"✓ Expediente registrado en bloque #{block1.block_id}\n")
    
    # Registrar documento
    print("Registrando documento...")
    block2 = exp_blockchain.registrar_documento(
        user_hash="abc123def456",
        documento_hash="doc_hash_789",
        nombre_documento="demanda.pdf",
        origen_email="usuario@gmail.com",
        asunto_email="Demanda de amparo",
        tamano_bytes=1024000
    )
    print(f"✓ Documento registrado en bloque #{block2.block_id}\n")
    
    # Verificar blockchain
    print("Verificando integridad de la blockchain...")
    valida, mensaje = exp_blockchain.blockchain.is_valid()
    print(f"Resultado: {mensaje}\n")
    
    # Estadísticas
    print("Estadísticas de la blockchain:")
    stats = exp_blockchain.blockchain.get_stats()
    for key, value in stats.items():
        print(f"  {key}: {value}")
    
    # Generar cadena de custodia
    print("\nGenerando cadena de custodia...")
    cadena = exp_blockchain.generar_cadena_custodia("abc123def456")
    print(json.dumps(cadena, indent=2, ensure_ascii=False))
    
    print("\n═══════════════════════════════════════════════════")


if __name__ == '__main__':
    main()
