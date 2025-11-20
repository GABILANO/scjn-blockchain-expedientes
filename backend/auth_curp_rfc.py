#!/usr/bin/env python3
"""
Sistema de Autenticación CURP/RFC
Validación cruzada de identidades para expedientes virtuales
"""

import re
import hashlib
import secrets
from datetime import datetime
from typing import Dict, Tuple, Optional
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ValidadorCURP:
    """
    Validador de CURP según especificaciones de RENAPO
    """
    
    # Formato: AAAA######HHHHHH##
    PATTERN = r'^[A-Z]{4}\d{6}[HM][A-Z]{5}[0-9A-Z]\d$'
    
    # Tabla de valores para dígito verificador
    VALORES = "0123456789ABCDEFGHIJKLMNÑOPQRSTUVWXYZ"
    
    @classmethod
    def validar_formato(cls, curp: str) -> Tuple[bool, str]:
        """Valida el formato básico del CURP"""
        if not curp:
            return False, "CURP vacío"
        
        curp = curp.upper().strip()
        
        if len(curp) != 18:
            return False, f"Longitud incorrecta: {len(curp)} (debe ser 18)"
        
        if not re.match(cls.PATTERN, curp):
            return False, "Formato inválido"
        
        return True, "Formato válido"
    
    @classmethod
    def validar_fecha_nacimiento(cls, curp: str) -> Tuple[bool, str]:
        """Valida la fecha de nacimiento en el CURP"""
        try:
            year = int(curp[4:6])
            month = int(curp[6:8])
            day = int(curp[8:10])
            
            # Determinar siglo
            current_year = datetime.now().year % 100
            if year <= current_year:
                full_year = 2000 + year
            else:
                full_year = 1900 + year
            
            # Validar mes
            if month < 1 or month > 12:
                return False, f"Mes inválido: {month}"
            
            # Validar día
            if day < 1 or day > 31:
                return False, f"Día inválido: {day}"
            
            # Validar fecha completa
            try:
                fecha = datetime(full_year, month, day)
                
                # Verificar que no sea fecha futura
                if fecha > datetime.now():
                    return False, "Fecha de nacimiento en el futuro"
                
                return True, f"Fecha válida: {fecha.strftime('%Y-%m-%d')}"
                
            except ValueError as e:
                return False, f"Fecha inválida: {e}"
                
        except Exception as e:
            return False, f"Error validando fecha: {e}"
    
    @classmethod
    def validar_digito_verificador(cls, curp: str) -> Tuple[bool, str]:
        """Valida el dígito verificador del CURP"""
        try:
            suma = 0
            
            for i, char in enumerate(curp[:-1]):
                valor = cls.VALORES.index(char)
                suma += valor * (18 - i)
            
            digito_esperado = (10 - (suma % 10)) % 10
            digito_actual = int(curp[-1])
            
            if digito_esperado == digito_actual:
                return True, "Dígito verificador correcto"
            else:
                return False, f"Dígito verificador incorrecto (esperado: {digito_esperado}, actual: {digito_actual})"
                
        except Exception as e:
            return False, f"Error validando dígito verificador: {e}"
    
    @classmethod
    def validar(cls, curp: str) -> Tuple[bool, str, Dict]:
        """Validación completa del CURP"""
        curp = curp.upper().strip()
        
        # Validar formato
        valido, mensaje = cls.validar_formato(curp)
        if not valido:
            return False, mensaje, {}
        
        # Validar fecha de nacimiento
        valido, mensaje_fecha = cls.validar_fecha_nacimiento(curp)
        if not valido:
            return False, mensaje_fecha, {}
        
        # Validar dígito verificador
        valido, mensaje_digito = cls.validar_digito_verificador(curp)
        if not valido:
            return False, mensaje_digito, {}
        
        # Extraer información
        info = {
            'curp': curp,
            'apellido_paterno': curp[0],
            'apellido_materno': curp[2],
            'nombre': curp[3],
            'fecha_nacimiento': mensaje_fecha.split(': ')[1],
            'sexo': 'Hombre' if curp[10] == 'H' else 'Mujer',
            'estado_nacimiento': curp[11:13],
            'valido': True
        }
        
        return True, "CURP válido", info


class ValidadorRFC:
    """
    Validador de RFC según especificaciones del SAT
    """
    
    # Persona física: AAAA######XXX (13 caracteres)
    PATTERN_FISICA = r'^[A-ZÑ&]{4}\d{6}[A-Z0-9]{3}$'
    
    # Persona moral: AAA######XXX (12 caracteres)
    PATTERN_MORAL = r'^[A-ZÑ&]{3}\d{6}[A-Z0-9]{3}$'
    
    @classmethod
    def identificar_tipo(cls, rfc: str) -> Optional[str]:
        """Identifica si es persona física o moral"""
        rfc = rfc.upper().strip()
        
        if len(rfc) == 13:
            return 'fisica'
        elif len(rfc) == 12:
            return 'moral'
        else:
            return None
    
    @classmethod
    def validar_formato(cls, rfc: str, tipo: str = None) -> Tuple[bool, str]:
        """Valida el formato del RFC"""
        if not rfc:
            return False, "RFC vacío"
        
        rfc = rfc.upper().strip()
        
        if tipo is None:
            tipo = cls.identificar_tipo(rfc)
        
        if tipo is None:
            return False, f"Longitud incorrecta: {len(rfc)} (debe ser 12 o 13)"
        
        if tipo == 'fisica':
            if not re.match(cls.PATTERN_FISICA, rfc):
                return False, "Formato inválido para persona física"
        else:
            if not re.match(cls.PATTERN_MORAL, rfc):
                return False, "Formato inválido para persona moral"
        
        return True, f"Formato válido ({tipo})"
    
    @classmethod
    def validar_fecha_nacimiento(cls, rfc: str) -> Tuple[bool, str]:
        """Valida la fecha de nacimiento en el RFC"""
        try:
            # Extraer fecha (posición 4-10 para física, 3-9 para moral)
            tipo = cls.identificar_tipo(rfc)
            
            if tipo == 'fisica':
                year = int(rfc[4:6])
                month = int(rfc[6:8])
                day = int(rfc[8:10])
            else:
                year = int(rfc[3:5])
                month = int(rfc[5:7])
                day = int(rfc[7:9])
            
            # Determinar siglo
            current_year = datetime.now().year % 100
            if year <= current_year:
                full_year = 2000 + year
            else:
                full_year = 1900 + year
            
            # Validar mes
            if month < 1 or month > 12:
                return False, f"Mes inválido: {month}"
            
            # Validar día
            if day < 1 or day > 31:
                return False, f"Día inválido: {day}"
            
            # Validar fecha completa
            try:
                fecha = datetime(full_year, month, day)
                return True, f"Fecha válida: {fecha.strftime('%Y-%m-%d')}"
            except ValueError as e:
                return False, f"Fecha inválida: {e}"
                
        except Exception as e:
            return False, f"Error validando fecha: {e}"
    
    @classmethod
    def validar_homoclave(cls, rfc: str) -> Tuple[bool, str]:
        """Valida la homoclave del RFC (simplificado)"""
        # Nota: La validación completa de homoclave requiere el algoritmo del SAT
        # Esta es una validación simplificada
        
        homoclave = rfc[-3:]
        
        # Verificar que sean caracteres alfanuméricos
        if not re.match(r'^[A-Z0-9]{3}$', homoclave):
            return False, "Homoclave inválida"
        
        return True, "Homoclave válida"
    
    @classmethod
    def validar(cls, rfc: str, tipo: str = None) -> Tuple[bool, str, Dict]:
        """Validación completa del RFC"""
        rfc = rfc.upper().strip()
        
        if tipo is None:
            tipo = cls.identificar_tipo(rfc)
        
        # Validar formato
        valido, mensaje = cls.validar_formato(rfc, tipo)
        if not valido:
            return False, mensaje, {}
        
        # Validar fecha de nacimiento
        valido, mensaje_fecha = cls.validar_fecha_nacimiento(rfc)
        if not valido:
            return False, mensaje_fecha, {}
        
        # Validar homoclave
        valido, mensaje_homoclave = cls.validar_homoclave(rfc)
        if not valido:
            return False, mensaje_homoclave, {}
        
        # Extraer información
        info = {
            'rfc': rfc,
            'tipo': tipo,
            'fecha_nacimiento': mensaje_fecha.split(': ')[1],
            'homoclave': rfc[-3:],
            'valido': True
        }
        
        return True, f"RFC válido ({tipo})", info


class ValidadorCruzado:
    """
    Validador cruzado de CURP y RFC
    """
    
    @classmethod
    def validar_coincidencia(cls, curp: str, rfc: str) -> Tuple[bool, str, Dict]:
        """
        Valida que CURP y RFC correspondan a la misma persona
        """
        curp = curp.upper().strip()
        rfc = rfc.upper().strip()
        
        # Validar CURP
        valido_curp, mensaje_curp, info_curp = ValidadorCURP.validar(curp)
        if not valido_curp:
            return False, f"CURP inválido: {mensaje_curp}", {}
        
        # Validar RFC
        valido_rfc, mensaje_rfc, info_rfc = ValidadorRFC.validar(rfc)
        if not valido_rfc:
            return False, f"RFC inválido: {mensaje_rfc}", {}
        
        # Verificar tipo de persona
        if info_rfc['tipo'] != 'fisica':
            return False, "Solo se permite validación cruzada para personas físicas", {}
        
        # Extraer fechas de nacimiento
        fecha_curp = info_curp['fecha_nacimiento']
        fecha_rfc = info_rfc['fecha_nacimiento']
        
        if fecha_curp != fecha_rfc:
            return False, f"Fechas de nacimiento no coinciden (CURP: {fecha_curp}, RFC: {fecha_rfc})", {}
        
        # Extraer iniciales del CURP
        iniciales_curp = curp[0:4]
        
        # Extraer iniciales del RFC
        iniciales_rfc = rfc[0:4]
        
        if iniciales_curp != iniciales_rfc:
            return False, f"Iniciales no coinciden (CURP: {iniciales_curp}, RFC: {iniciales_rfc})", {}
        
        # Validación exitosa
        info = {
            'curp': curp,
            'rfc': rfc,
            'fecha_nacimiento': fecha_curp,
            'sexo': info_curp['sexo'],
            'tipo_persona': 'fisica',
            'validacion_cruzada': True
        }
        
        return True, "CURP y RFC coinciden correctamente", info


class GestorExpedientesVirtuales:
    """
    Gestor de expedientes virtuales con autenticación CURP/RFC
    """
    
    def __init__(self, salt_global: str = None):
        if salt_global is None:
            self.salt_global = secrets.token_hex(32)
        else:
            self.salt_global = salt_global
    
    def generar_hash_usuario(self, curp: str, rfc: str) -> Dict:
        """
        Genera hash único para usuario
        """
        # Salt específico del usuario
        salt_usuario = secrets.token_hex(16)
        
        # Concatenar datos
        data = f"{curp}{rfc}{self.salt_global}{salt_usuario}"
        
        # Generar hash SHA-256
        hash_obj = hashlib.sha256(data.encode())
        user_hash = hash_obj.hexdigest()
        
        # Generar email personalizado
        email = f"{user_hash[:16]}@scjn-expedientes.mx"
        
        return {
            'user_hash': user_hash,
            'user_hash_short': user_hash[:16],
            'salt_usuario': salt_usuario,
            'email_personalizado': email,
            'curp_hash': hashlib.sha256(curp.encode()).hexdigest(),
            'rfc_hash': hashlib.sha256(rfc.encode()).hexdigest(),
            'fecha_creacion': datetime.now().isoformat()
        }
    
    def verificar_usuario(self, curp: str, rfc: str, user_hash: str, salt_usuario: str) -> bool:
        """
        Verifica que CURP y RFC correspondan al hash
        """
        data = f"{curp}{rfc}{self.salt_global}{salt_usuario}"
        hash_obj = hashlib.sha256(data.encode())
        calculated_hash = hash_obj.hexdigest()
        
        return calculated_hash == user_hash
    
    def registrar_usuario(self, curp: str, rfc: str) -> Tuple[bool, str, Dict]:
        """
        Registra un nuevo usuario en el sistema
        """
        # Validar coincidencia CURP/RFC
        valido, mensaje, info_validacion = ValidadorCruzado.validar_coincidencia(curp, rfc)
        
        if not valido:
            return False, mensaje, {}
        
        # Generar hash de usuario
        info_hash = self.generar_hash_usuario(curp, rfc)
        
        # Combinar información
        info_usuario = {
            **info_validacion,
            **info_hash,
            'estado': 'activo'
        }
        
        logger.info(f"Usuario registrado: {info_usuario['email_personalizado']}")
        
        return True, "Usuario registrado exitosamente", info_usuario
    
    def registrar_persona_moral(self, rfc: str, razon_social: str) -> Tuple[bool, str, Dict]:
        """
        Registra una persona moral en el sistema
        """
        # Validar RFC
        valido, mensaje, info_rfc = ValidadorRFC.validar(rfc, tipo='moral')
        
        if not valido:
            return False, mensaje, {}
        
        # Generar hash (sin CURP)
        salt_usuario = secrets.token_hex(16)
        data = f"{rfc}{razon_social}{self.salt_global}{salt_usuario}"
        hash_obj = hashlib.sha256(data.encode())
        user_hash = hash_obj.hexdigest()
        
        # Generar email personalizado
        email = f"{user_hash[:16]}@scjn-expedientes.mx"
        
        info_usuario = {
            'user_hash': user_hash,
            'user_hash_short': user_hash[:16],
            'salt_usuario': salt_usuario,
            'email_personalizado': email,
            'rfc': rfc,
            'rfc_hash': hashlib.sha256(rfc.encode()).hexdigest(),
            'razon_social': razon_social,
            'tipo_persona': 'moral',
            'fecha_creacion': datetime.now().isoformat(),
            'estado': 'activo'
        }
        
        logger.info(f"Persona moral registrada: {email}")
        
        return True, "Persona moral registrada exitosamente", info_usuario


def main():
    """Función de prueba"""
    print("═══════════════════════════════════════════════════")
    print("SISTEMA DE AUTENTICACIÓN CURP/RFC")
    print("═══════════════════════════════════════════════════\n")
    
    # Ejemplo de CURP válido (formato de prueba)
    curp_test = "GABC850101HDFRRL09"
    rfc_test = "GABC850101ABC"
    
    print(f"Probando CURP: {curp_test}")
    valido, mensaje, info = ValidadorCURP.validar(curp_test)
    print(f"Resultado: {mensaje}")
    if valido:
        print(f"Info: {info}\n")
    
    print(f"Probando RFC: {rfc_test}")
    valido, mensaje, info = ValidadorRFC.validar(rfc_test)
    print(f"Resultado: {mensaje}")
    if valido:
        print(f"Info: {info}\n")
    
    print("Probando validación cruzada...")
    valido, mensaje, info = ValidadorCruzado.validar_coincidencia(curp_test, rfc_test)
    print(f"Resultado: {mensaje}")
    if valido:
        print(f"Info: {info}\n")
    
    print("Registrando usuario...")
    gestor = GestorExpedientesVirtuales()
    valido, mensaje, info_usuario = gestor.registrar_usuario(curp_test, rfc_test)
    print(f"Resultado: {mensaje}")
    if valido:
        print(f"Email personalizado: {info_usuario['email_personalizado']}")
        print(f"User hash: {info_usuario['user_hash']}")
    
    print("\n═══════════════════════════════════════════════════")


if __name__ == '__main__':
    main()
