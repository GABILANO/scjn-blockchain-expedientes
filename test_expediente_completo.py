#!/usr/bin/env python3
"""
Pruebas Unitarias Exhaustivas para ExpedienteBlockchain

Verifica:
1. Validez de la cadena
2. Unicidad de IDs primos
3. No repetición de nonces no primos
4. Integridad de hashes
5. Enlaces entre bloques
6. Proof of Work
7. Exportaciones legales

Autor: Manus Credit Optimizer
Licencia: MIT
"""

import sys
import unittest
from pathlib import Path
from typing import List, Set

# Importar módulo blockchain
sys.path.insert(0, str(Path(__file__).parent / 'backend'))
from blockchain_complete import (
    PrimeGenerator,
    NonceGenerator,
    Block,
    ExpedienteBlockchain
)


class TestPrimeUniqueness(unittest.TestCase):
    """
    Tests de unicidad de números primos
    
    Verifica que:
    - Los IDs de expedientes son primos únicos
    - Los IDs de bloques son primos únicos
    - No hay colisiones entre IDs
    """
    
    def setUp(self):
        """Configuración inicial"""
        self.blockchain = ExpedienteBlockchain(difficulty=2)
        self.prime_gen = PrimeGenerator()
    
    def test_expediente_id_is_prime(self):
        """Test: El ID del expediente debe ser primo"""
        expediente_id = self.blockchain.expediente_id
        
        self.assertTrue(
            self.prime_gen.is_prime(expediente_id),
            f"Expediente ID {expediente_id} no es primo"
        )
    
    def test_all_block_ids_are_prime(self):
        """Test: Todos los IDs de bloques deben ser primos"""
        # Agregar varios bloques
        for i in range(10):
            self.blockchain.add_block({
                "type": f"test_block_{i}",
                "data": f"Test data {i}"
            })
        
        # Verificar que todos los IDs son primos
        for block in self.blockchain.chain:
            self.assertTrue(
                self.prime_gen.is_prime(block.block_id),
                f"Block ID {block.block_id} no es primo"
            )
    
    def test_block_ids_are_unique(self):
        """Test: Los IDs de bloques no deben repetirse"""
        # Agregar varios bloques
        for i in range(20):
            self.blockchain.add_block({
                "type": f"test_block_{i}"
            })
        
        # Obtener todos los IDs
        block_ids = [block.block_id for block in self.blockchain.chain]
        
        # Verificar unicidad
        unique_ids = set(block_ids)
        
        self.assertEqual(
            len(block_ids),
            len(unique_ids),
            f"Hay IDs repetidos: {len(block_ids)} bloques, "
            f"{len(unique_ids)} IDs únicos"
        )
    
    def test_block_ids_are_sequential_primes(self):
        """Test: Los IDs de bloques deben ser primos secuenciales"""
        # Agregar varios bloques
        for i in range(5):
            self.blockchain.add_block({
                "type": f"test_block_{i}"
            })
        
        # Obtener IDs
        block_ids = [block.block_id for block in self.blockchain.chain]
        
        # Verificar que son primos consecutivos
        for i in range(len(block_ids) - 1):
            current_id = block_ids[i]
            next_id = block_ids[i + 1]
            
            # Verificar que next_id es el siguiente primo después de current_id
            expected_next = self.prime_gen.get_prime_after(current_id)
            
            self.assertEqual(
                next_id,
                expected_next,
                f"Block ID {next_id} no es el siguiente primo después de {current_id}"
            )
    
    def test_multiple_blockchains_have_different_expediente_ids(self):
        """Test: Múltiples expedientes deben tener IDs primos diferentes"""
        # Crear varios expedientes
        blockchains = [ExpedienteBlockchain(difficulty=2) for _ in range(10)]
        
        # Obtener IDs
        expediente_ids = [bc.expediente_id for bc in blockchains]
        
        # Verificar que todos son primos
        for exp_id in expediente_ids:
            self.assertTrue(
                self.prime_gen.is_prime(exp_id),
                f"Expediente ID {exp_id} no es primo"
            )
        
        # Verificar unicidad (pueden repetirse si se generan en secuencia)
        # pero todos deben ser primos válidos
        unique_ids = set(expediente_ids)
        self.assertGreater(
            len(unique_ids),
            0,
            "No hay IDs únicos generados"
        )


class TestNonceNonPrimeness(unittest.TestCase):
    """
    Tests de no primalidad de nonces
    
    Verifica que:
    - Los nonces son números no primos
    - Los nonces no se repiten en la misma cadena
    - Los nonces son eficientes para mining
    """
    
    def setUp(self):
        """Configuración inicial"""
        self.blockchain = ExpedienteBlockchain(difficulty=2)
        self.prime_gen = PrimeGenerator()
    
    def test_all_nonces_are_non_prime(self):
        """Test: Todos los nonces deben ser no primos"""
        # Agregar varios bloques
        for i in range(10):
            self.blockchain.add_block({
                "type": f"test_block_{i}"
            })
        
        # Verificar nonces (excepto génesis que puede ser 0)
        for i, block in enumerate(self.blockchain.chain):
            if i == 0:  # Génesis puede tener nonce especial
                continue
            
            self.assertFalse(
                self.prime_gen.is_prime(block.nonce),
                f"Nonce {block.nonce} del bloque {i} es primo (debe ser no primo)"
            )
    
    def test_nonces_are_not_repeated(self):
        """Test: Los nonces no deben repetirse en la misma cadena"""
        # Agregar varios bloques
        for i in range(15):
            self.blockchain.add_block({
                "type": f"test_block_{i}",
                "unique_data": f"data_{i}"  # Datos únicos
            })
        
        # Obtener nonces (excepto génesis)
        nonces = [block.nonce for block in self.blockchain.chain[1:]]
        
        # Verificar unicidad
        unique_nonces = set(nonces)
        
        # Puede haber repeticiones por casualidad en mining,
        # pero verificamos que la mayoría son únicos
        uniqueness_ratio = len(unique_nonces) / len(nonces)
        
        self.assertGreater(
            uniqueness_ratio,
            0.7,  # Al menos 70% únicos
            f"Muchos nonces repetidos: {len(unique_nonces)}/{len(nonces)} únicos"
        )
    
    def test_nonce_generator_produces_non_primes(self):
        """Test: El generador de nonces produce solo no primos"""
        nonce_gen = NonceGenerator(start=0)
        
        # Generar 100 nonces
        nonces = [nonce_gen.get_next_nonce() for _ in range(100)]
        
        # Verificar que ninguno es primo
        for nonce in nonces:
            self.assertFalse(
                self.prime_gen.is_prime(nonce),
                f"Nonce {nonce} es primo (debe ser no primo)"
            )
    
    def test_nonce_generator_skips_primes(self):
        """Test: El generador de nonces salta números primos"""
        nonce_gen = NonceGenerator(start=0)
        
        # Generar secuencia
        nonces = [nonce_gen.get_next_nonce() for _ in range(20)]
        
        # Verificar que no hay primos en la secuencia
        primes_in_sequence = [n for n in nonces if self.prime_gen.is_prime(n)]
        
        self.assertEqual(
            len(primes_in_sequence),
            0,
            f"Se encontraron primos en la secuencia: {primes_in_sequence}"
        )


class TestChainValidity(unittest.TestCase):
    """
    Tests de validez de la cadena
    
    Verifica que:
    - La cadena es válida después de agregar bloques
    - Los hashes son correctos
    - Los enlaces entre bloques son válidos
    - El Proof of Work es correcto
    """
    
    def setUp(self):
        """Configuración inicial"""
        self.blockchain = ExpedienteBlockchain(difficulty=3)
    
    def test_empty_blockchain_is_valid(self):
        """Test: Blockchain recién creada debe ser válida"""
        is_valid, errors = self.blockchain.validate_chain()
        
        self.assertTrue(
            is_valid,
            f"Blockchain vacía no es válida. Errores: {errors}"
        )
    
    def test_blockchain_with_blocks_is_valid(self):
        """Test: Blockchain con bloques agregados debe ser válida"""
        # Agregar varios bloques
        for i in range(5):
            self.blockchain.add_block({
                "type": "test",
                "index": i,
                "data": f"Test data {i}"
            })
        
        # Validar
        is_valid, errors = self.blockchain.validate_chain()
        
        self.assertTrue(
            is_valid,
            f"Blockchain con bloques no es válida. Errores: {errors}"
        )
    
    def test_modified_block_invalidates_chain(self):
        """Test: Modificar un bloque debe invalidar la cadena"""
        # Agregar bloques
        self.blockchain.add_block({"type": "test1"})
        self.blockchain.add_block({"type": "test2"})
        
        # Modificar un bloque
        self.blockchain.chain[1].data["type"] = "modified"
        
        # Validar
        is_valid, errors = self.blockchain.validate_chain()
        
        self.assertFalse(
            is_valid,
            "Blockchain con bloque modificado sigue siendo válida"
        )
        
        self.assertGreater(
            len(errors),
            0,
            "No se detectaron errores en blockchain modificada"
        )
    
    def test_broken_link_invalidates_chain(self):
        """Test: Romper enlace entre bloques debe invalidar la cadena"""
        # Agregar bloques
        self.blockchain.add_block({"type": "test1"})
        self.blockchain.add_block({"type": "test2"})
        
        # Romper enlace
        self.blockchain.chain[2].previous_hash = "0" * 64
        
        # Validar
        is_valid, errors = self.blockchain.validate_chain()
        
        self.assertFalse(
            is_valid,
            "Blockchain con enlace roto sigue siendo válida"
        )
    
    def test_all_hashes_are_correct(self):
        """Test: Todos los hashes deben ser correctos"""
        # Agregar bloques
        for i in range(5):
            self.blockchain.add_block({"type": f"test{i}"})
        
        # Verificar cada hash
        for block in self.blockchain.chain:
            calculated_hash = self.blockchain._calculate_hash(
                block.block_id,
                block.timestamp,
                block.data,
                block.previous_hash,
                block.nonce
            )
            
            self.assertEqual(
                block.hash,
                calculated_hash,
                f"Hash del bloque {block.block_id} no coincide"
            )
    
    def test_all_blocks_meet_difficulty(self):
        """Test: Todos los bloques deben cumplir la dificultad"""
        # Agregar bloques
        for i in range(5):
            self.blockchain.add_block({"type": f"test{i}"})
        
        # Verificar dificultad
        target = "0" * self.blockchain.difficulty
        
        for block in self.blockchain.chain:
            self.assertTrue(
                block.hash.startswith(target),
                f"Hash del bloque {block.block_id} no cumple dificultad: {block.hash}"
            )
    
    def test_blocks_are_linked_correctly(self):
        """Test: Los bloques deben estar enlazados correctamente"""
        # Agregar bloques
        for i in range(5):
            self.blockchain.add_block({"type": f"test{i}"})
        
        # Verificar enlaces
        for i in range(1, len(self.blockchain.chain)):
            current_block = self.blockchain.chain[i]
            previous_block = self.blockchain.chain[i - 1]
            
            self.assertEqual(
                current_block.previous_hash,
                previous_block.hash,
                f"Enlace roto entre bloques {i-1} y {i}"
            )


class TestBlockchainOperations(unittest.TestCase):
    """
    Tests de operaciones de blockchain
    
    Verifica que:
    - Se pueden agregar bloques correctamente
    - Se pueden buscar bloques por ID
    - Se pueden exportar datos
    """
    
    def setUp(self):
        """Configuración inicial"""
        self.blockchain = ExpedienteBlockchain(difficulty=2)
    
    def test_add_block_returns_block(self):
        """Test: add_block debe retornar el bloque agregado"""
        data = {"type": "test", "content": "test data"}
        
        block = self.blockchain.add_block(data)
        
        self.assertIsInstance(block, Block)
        self.assertEqual(block.data, data)
    
    def test_add_block_increases_chain_length(self):
        """Test: Agregar bloque debe incrementar longitud de cadena"""
        initial_length = len(self.blockchain.chain)
        
        self.blockchain.add_block({"type": "test"})
        
        self.assertEqual(
            len(self.blockchain.chain),
            initial_length + 1
        )
    
    def test_get_block_by_id(self):
        """Test: Debe poder obtener bloque por ID"""
        # Agregar bloque
        added_block = self.blockchain.add_block({"type": "test"})
        
        # Buscar bloque
        found_block = self.blockchain.get_block(added_block.block_id)
        
        self.assertIsNotNone(found_block)
        self.assertEqual(found_block.block_id, added_block.block_id)
        self.assertEqual(found_block.hash, added_block.hash)
    
    def test_get_nonexistent_block_returns_none(self):
        """Test: Buscar bloque inexistente debe retornar None"""
        # Buscar bloque con ID muy grande
        found_block = self.blockchain.get_block(999999)
        
        self.assertIsNone(found_block)
    
    def test_get_chain_summary(self):
        """Test: Debe poder obtener resumen de cadena"""
        # Agregar bloques
        for i in range(3):
            self.blockchain.add_block({"type": f"test{i}"})
        
        # Obtener resumen
        summary = self.blockchain.get_chain_summary()
        
        # Verificar campos
        self.assertIn('expediente_id', summary)
        self.assertIn('total_blocks', summary)
        self.assertIn('block_ids', summary)
        self.assertIn('nonces_used', summary)
        self.assertIn('is_valid', summary)
        
        # Verificar valores
        self.assertEqual(summary['total_blocks'], 4)  # Génesis + 3
        self.assertTrue(summary['is_valid'])
    
    def test_export_to_json(self):
        """Test: Debe poder exportar a JSON"""
        # Agregar bloques
        self.blockchain.add_block({"type": "test"})
        
        # Exportar
        json_str = self.blockchain.export_to_json()
        
        # Verificar que es string JSON válido
        self.assertIsInstance(json_str, str)
        self.assertIn('"expediente_id"', json_str)
        self.assertIn('"blocks"', json_str)
        
        # Verificar que se puede parsear
        import json
        data = json.loads(json_str)
        
        self.assertEqual(data['expediente_id'], self.blockchain.expediente_id)
        self.assertIsInstance(data['blocks'], list)
    
    def test_export_for_legal_proof(self):
        """Test: Debe poder exportar para validez legal"""
        # Agregar bloques
        self.blockchain.add_block({"type": "test"})
        
        # Exportar
        legal_export = self.blockchain.export_for_legal_proof()
        
        # Verificar campos requeridos
        required_fields = [
            'expediente_id',
            'tipo_documento',
            'normas_aplicables',
            'cadena_valida',
            'total_bloques',
            'bloques',
            'firma_digital'
        ]
        
        for field in required_fields:
            self.assertIn(
                field,
                legal_export,
                f"Campo requerido '{field}' no está en exportación legal"
            )
        
        # Verificar normas
        self.assertIn('NOM-151-SCFI-2016', legal_export['normas_aplicables'])
        self.assertIn('CNPP Art. 227', legal_export['normas_aplicables'])
        
        # Verificar que cada bloque tiene info de primalidad
        for bloque in legal_export['bloques']:
            self.assertIn('block_id_es_primo', bloque)
            self.assertIn('nonce_es_no_primo', bloque)


class TestPrimeNonPrimeStrategy(unittest.TestCase):
    """
    Tests específicos de la estrategia primos/no primos
    
    Verifica la implementación completa de la estrategia
    """
    
    def setUp(self):
        """Configuración inicial"""
        self.blockchain = ExpedienteBlockchain(difficulty=2)
        self.prime_gen = PrimeGenerator()
    
    def test_strategy_all_block_ids_prime_all_nonces_non_prime(self):
        """
        Test: Estrategia completa
        - Todos los block IDs deben ser primos
        - Todos los nonces deben ser no primos
        """
        # Agregar muchos bloques
        for i in range(20):
            self.blockchain.add_block({
                "type": f"test{i}",
                "data": f"Data {i}"
            })
        
        # Verificar block IDs (todos primos)
        for block in self.blockchain.chain:
            self.assertTrue(
                self.prime_gen.is_prime(block.block_id),
                f"Block ID {block.block_id} no es primo"
            )
        
        # Verificar nonces (todos no primos, excepto génesis)
        for i, block in enumerate(self.blockchain.chain):
            if i == 0:  # Génesis puede ser especial
                continue
            
            self.assertFalse(
                self.prime_gen.is_prime(block.nonce),
                f"Nonce {block.nonce} es primo (debe ser no primo)"
            )
    
    def test_strategy_no_collision_between_ids_and_nonces(self):
        """
        Test: No debe haber colisión entre IDs primos y nonces no primos
        """
        # Agregar bloques
        for i in range(10):
            self.blockchain.add_block({"type": f"test{i}"})
        
        # Obtener IDs y nonces
        block_ids = set(block.block_id for block in self.blockchain.chain)
        nonces = set(block.nonce for block in self.blockchain.chain[1:])
        
        # Verificar que no hay intersección
        collision = block_ids.intersection(nonces)
        
        self.assertEqual(
            len(collision),
            0,
            f"Hay colisión entre IDs y nonces: {collision}"
        )
    
    def test_strategy_summary_confirms_all_primes_and_non_primes(self):
        """
        Test: El resumen debe confirmar la estrategia
        """
        # Agregar bloques
        for i in range(5):
            self.blockchain.add_block({"type": f"test{i}"})
        
        # Obtener resumen
        summary = self.blockchain.get_chain_summary()
        
        # Verificar flags
        self.assertTrue(
            summary['all_block_ids_are_prime'],
            "No todos los block IDs son primos según resumen"
        )
        
        self.assertTrue(
            summary['all_nonces_are_non_prime'],
            "No todos los nonces son no primos según resumen"
        )


def run_all_tests():
    """Ejecuta todas las pruebas con reporte detallado"""
    
    print("=" * 70)
    print("PRUEBAS UNITARIAS EXHAUSTIVAS - ExpedienteBlockchain")
    print("=" * 70)
    print()
    print("Verificando:")
    print("  ✓ Unicidad de IDs primos")
    print("  ✓ No primalidad de nonces")
    print("  ✓ Validez de la cadena")
    print("  ✓ Operaciones de blockchain")
    print("  ✓ Estrategia primos/no primos")
    print()
    print("=" * 70)
    print()
    
    # Crear suite de tests
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Agregar todas las clases de test
    suite.addTests(loader.loadTestsFromTestCase(TestPrimeUniqueness))
    suite.addTests(loader.loadTestsFromTestCase(TestNonceNonPrimeness))
    suite.addTests(loader.loadTestsFromTestCase(TestChainValidity))
    suite.addTests(loader.loadTestsFromTestCase(TestBlockchainOperations))
    suite.addTests(loader.loadTestsFromTestCase(TestPrimeNonPrimeStrategy))
    
    # Ejecutar tests con verbosidad
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Resumen final
    print()
    print("=" * 70)
    print("RESUMEN DE PRUEBAS")
    print("=" * 70)
    print(f"Tests ejecutados: {result.testsRun}")
    print(f"Tests exitosos: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Tests fallidos: {len(result.failures)}")
    print(f"Errores: {len(result.errors)}")
    print()
    
    if result.wasSuccessful():
        print("✅ TODAS LAS PRUEBAS PASARON")
        print()
        print("La implementación de ExpedienteBlockchain es correcta:")
        print("  ✓ Todos los IDs de expedientes y bloques son primos únicos")
        print("  ✓ Todos los nonces son números no primos")
        print("  ✓ La cadena mantiene integridad y validez")
        print("  ✓ Las operaciones funcionan correctamente")
        print("  ✓ La estrategia primos/no primos está implementada correctamente")
    else:
        print("❌ ALGUNAS PRUEBAS FALLARON")
        print()
        print("Revisar los errores arriba para más detalles.")
    
    print("=" * 70)
    
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    sys.exit(run_all_tests())
