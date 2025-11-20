#!/usr/bin/env python3
"""
Tests para el módulo blockchain

Verifica la implementación estratégica de números primos y no primos
"""

import pytest
from blockchain_complete import (
    PrimeGenerator,
    NonceGenerator,
    Block,
    ExpedienteBlockchain
)


class TestPrimeGenerator:
    """Tests para generador de números primos"""
    
    def test_is_prime(self):
        """Test verificación de primalidad"""
        gen = PrimeGenerator()
        
        # Primos conocidos
        assert gen.is_prime(2) == True
        assert gen.is_prime(3) == True
        assert gen.is_prime(5) == True
        assert gen.is_prime(7) == True
        assert gen.is_prime(11) == True
        assert gen.is_prime(97) == True
        
        # No primos
        assert gen.is_prime(1) == False
        assert gen.is_prime(4) == False
        assert gen.is_prime(6) == False
        assert gen.is_prime(8) == False
        assert gen.is_prime(9) == False
        assert gen.is_prime(100) == False
    
    def test_get_next_prime(self):
        """Test generación secuencial de primos"""
        gen = PrimeGenerator()
        
        # Primeros primos: 2, 3, 5, 7, 11, 13, 17, 19, 23, 29
        expected_primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
        
        for expected in expected_primes[:5]:  # Verificar primeros 5
            prime = gen.get_next_prime()
            assert gen.is_prime(prime)
    
    def test_get_prime_after(self):
        """Test obtener primo después de n"""
        gen = PrimeGenerator()
        
        assert gen.get_prime_after(10) == 11
        assert gen.get_prime_after(20) == 23
        assert gen.get_prime_after(100) == 101


class TestNonceGenerator:
    """Tests para generador de números no primos"""
    
    def test_get_next_nonce(self):
        """Test generación de nonces no primos"""
        gen = NonceGenerator(start=0)
        prime_gen = PrimeGenerator()
        
        # Generar 10 nonces
        for _ in range(10):
            nonce = gen.get_next_nonce()
            assert not prime_gen.is_prime(nonce), f"{nonce} es primo (debe ser no primo)"
    
    def test_reset(self):
        """Test reinicio del generador"""
        gen = NonceGenerator(start=0)
        
        # Generar algunos nonces
        for _ in range(5):
            gen.get_next_nonce()
        
        # Reiniciar
        gen.reset(0)
        
        # Primer nonce después de reset debe ser 1 (no primo)
        assert gen.get_next_nonce() == 1


class TestBlock:
    """Tests para bloques"""
    
    def test_block_creation(self):
        """Test creación de bloque"""
        block = Block(
            block_id=5,
            expediente_id=3,
            timestamp=1234567890.0,
            data={"test": "data"},
            previous_hash="0" * 64,
            hash="abc123",
            nonce=4,
            difficulty=4
        )
        
        assert block.block_id == 5
        assert block.expediente_id == 3
        assert block.nonce == 4
    
    def test_block_to_dict(self):
        """Test conversión a diccionario"""
        block = Block(
            block_id=5,
            expediente_id=3,
            timestamp=1234567890.0,
            data={"test": "data"},
            previous_hash="0" * 64,
            hash="abc123",
            nonce=4,
            difficulty=4
        )
        
        block_dict = block.to_dict()
        
        assert block_dict['block_id'] == 5
        assert block_dict['nonce'] == 4
        assert block_dict['data'] == {"test": "data"}
    
    def test_block_from_dict(self):
        """Test creación desde diccionario"""
        block_dict = {
            'block_id': 5,
            'expediente_id': 3,
            'timestamp': 1234567890.0,
            'data': {"test": "data"},
            'previous_hash': "0" * 64,
            'hash': "abc123",
            'nonce': 4,
            'difficulty': 4
        }
        
        block = Block.from_dict(block_dict)
        
        assert block.block_id == 5
        assert block.nonce == 4


class TestExpedienteBlockchain:
    """Tests para blockchain de expedientes"""
    
    def test_blockchain_creation(self):
        """Test creación de blockchain"""
        blockchain = ExpedienteBlockchain(difficulty=2)
        
        # Debe tener bloque génesis
        assert len(blockchain.chain) == 1
        
        # Expediente ID debe ser primo
        assert blockchain.prime_gen.is_prime(blockchain.expediente_id)
        
        # Block ID del génesis debe ser primo
        genesis = blockchain.chain[0]
        assert blockchain.prime_gen.is_prime(genesis.block_id)
    
    def test_add_block(self):
        """Test agregar bloque"""
        blockchain = ExpedienteBlockchain(difficulty=2)
        
        # Agregar bloque
        new_block = blockchain.add_block({
            "type": "document",
            "title": "Test Document"
        })
        
        # Verificar
        assert len(blockchain.chain) == 2
        assert blockchain.prime_gen.is_prime(new_block.block_id)
        assert not blockchain.prime_gen.is_prime(new_block.nonce)
    
    def test_validate_chain(self):
        """Test validación de cadena"""
        blockchain = ExpedienteBlockchain(difficulty=2)
        
        # Agregar algunos bloques
        blockchain.add_block({"type": "doc1"})
        blockchain.add_block({"type": "doc2"})
        
        # Validar
        is_valid, errors = blockchain.validate_chain()
        
        assert is_valid == True
        assert len(errors) == 0
    
    def test_chain_integrity(self):
        """Test integridad de cadena (detectar modificaciones)"""
        blockchain = ExpedienteBlockchain(difficulty=2)
        
        # Agregar bloque
        blockchain.add_block({"type": "document"})
        
        # Modificar bloque (romper cadena)
        blockchain.chain[1].data["type"] = "modified"
        
        # Validar debe fallar
        is_valid, errors = blockchain.validate_chain()
        
        assert is_valid == False
        assert len(errors) > 0
    
    def test_block_ids_are_prime(self):
        """Test que todos los block IDs son primos"""
        blockchain = ExpedienteBlockchain(difficulty=2)
        
        # Agregar varios bloques
        for i in range(5):
            blockchain.add_block({"type": f"doc{i}"})
        
        # Verificar que todos los IDs son primos
        for block in blockchain.chain:
            assert blockchain.prime_gen.is_prime(block.block_id)
    
    def test_nonces_are_non_prime(self):
        """Test que todos los nonces son no primos"""
        blockchain = ExpedienteBlockchain(difficulty=2)
        
        # Agregar varios bloques
        for i in range(5):
            blockchain.add_block({"type": f"doc{i}"})
        
        # Verificar que todos los nonces (excepto génesis) son no primos
        for block in blockchain.chain[1:]:  # Excluir génesis
            assert not blockchain.prime_gen.is_prime(block.nonce)
    
    def test_get_chain_summary(self):
        """Test resumen de cadena"""
        blockchain = ExpedienteBlockchain(difficulty=2)
        
        # Agregar bloques
        blockchain.add_block({"type": "doc1"})
        blockchain.add_block({"type": "doc2"})
        
        # Obtener resumen
        summary = blockchain.get_chain_summary()
        
        assert summary['total_blocks'] == 3
        assert summary['expediente_id_is_prime'] == True
        assert summary['all_block_ids_are_prime'] == True
        assert summary['all_nonces_are_non_prime'] == True
        assert summary['is_valid'] == True
    
    def test_export_to_json(self):
        """Test exportación a JSON"""
        blockchain = ExpedienteBlockchain(difficulty=2)
        
        blockchain.add_block({"type": "document"})
        
        json_str = blockchain.export_to_json()
        
        assert isinstance(json_str, str)
        assert "expediente_id" in json_str
        assert "blocks" in json_str
    
    def test_export_for_legal_proof(self):
        """Test exportación para validez legal"""
        blockchain = ExpedienteBlockchain(difficulty=2)
        
        blockchain.add_block({
            "type": "document",
            "title": "Demanda"
        })
        
        legal_export = blockchain.export_for_legal_proof()
        
        # Verificar campos requeridos
        assert "expediente_id" in legal_export
        assert "tipo_documento" in legal_export
        assert "normas_aplicables" in legal_export
        assert "cadena_valida" in legal_export
        assert "bloques" in legal_export
        assert "firma_digital" in legal_export
        
        # Verificar normas
        assert "NOM-151-SCFI-2016" in legal_export["normas_aplicables"]
        assert "CNPP Art. 227" in legal_export["normas_aplicables"]
        
        # Verificar que cada bloque tiene info de primalidad
        for bloque in legal_export["bloques"]:
            assert "block_id_es_primo" in bloque
            assert "nonce_es_no_primo" in bloque
    
    def test_get_block(self):
        """Test obtener bloque por ID"""
        blockchain = ExpedienteBlockchain(difficulty=2)
        
        new_block = blockchain.add_block({"type": "document"})
        
        # Buscar bloque
        found_block = blockchain.get_block(new_block.block_id)
        
        assert found_block is not None
        assert found_block.block_id == new_block.block_id
        
        # Buscar bloque inexistente
        not_found = blockchain.get_block(999999)
        assert not_found is None


def run_all_tests():
    """Ejecuta todos los tests"""
    print("=" * 60)
    print("EJECUTANDO TESTS DEL MÓDULO BLOCKCHAIN")
    print("=" * 60)
    print()
    
    # Ejecutar con pytest
    pytest.main([__file__, "-v", "--tb=short"])


if __name__ == "__main__":
    run_all_tests()
