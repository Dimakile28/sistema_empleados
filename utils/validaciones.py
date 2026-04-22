import re
from datetime import datetime

class Validaciones:
    """Clase para validar los datos de entrada"""
    
    @staticmethod
    def validar_cedula(cedula):
        """Valida que la cédula tenga entre 6 y 8 dígitos"""
        if not cedula or not str(cedula).strip():
            return False, "La cédula es obligatoria"
        
        cedula_str = str(cedula).strip()
        
        # Eliminar puntos si los tiene (ej: 12.345.678)
        cedula_str = cedula_str.replace('.', '')
        
        if not cedula_str.isdigit():
            return False, "La cédula debe contener solo números"
        
        if len(cedula_str) < 6 or len(cedula_str) > 8:
            return False, "La cédula debe tener entre 6 y 8 dígitos"
        
        return True, ""
    
    @staticmethod
    def validar_nombres(nombres):
        """Valida que los nombres no estén vacíos y tengan formato válido"""
        if not nombres or not str(nombres).strip():
            return False, "Los nombres y apellidos son obligatorios"
        
        nombre_str = str(nombres).strip()
        
        if len(nombre_str) < 3:
            return False, "Los nombres son demasiado cortos (mínimo 3 caracteres)"
        
        if len(nombre_str) > 150:
            return False, "Los nombres son demasiado largos (máximo 150 caracteres)"
        
        # Permitir letras, espacios, ñ, tildes
        patron = r'^[a-zA-ZáéíóúüñÁÉÍÓÚÜÑ\s]+$'
        if not re.match(patron, nombre_str):
            return False, "Los nombres solo pueden contener letras y espacios"
        
        return True, ""
    
    @staticmethod
    def validar_telefono(telefono):
        """Valida el formato del teléfono venezolano"""
        if not telefono or not str(telefono).strip():
            return True, ""  # Teléfono opcional
        
        telefono_str = str(telefono).strip()
        # Eliminar cualquier caracter no numérico
        telefono_limpio = re.sub(r'[^0-9]', '', telefono_str)
        
        if len(telefono_limpio) == 0:
            return True, ""
        
        # Validar formato venezolano: 0412XXXXXXX, 0414XXXXXXX, 0416XXXXXXX, 0424XXXXXXX, 0426XXXXXXX
        if len(telefono_limpio) == 11 and telefono_limpio.startswith('0'):
            operadoras = ['0412', '0414', '0416', '0424', '0426', '0422']
            if telefono_limpio[:4] in operadoras:
                return True, ""
            return False, "El teléfono debe comenzar con 0412, 0414, 0416, 0424, 0426 o 0422"
        
        if len(telefono_limpio) == 10 and telefono_limpio.startswith('4'):
            return True, ""
        
        if len(telefono_limpio) > 0:
            return False, "El teléfono debe tener 10 u 11 dígitos"
        
        return True, ""
    
    @staticmethod
    def validar_email(email):
        """Valida el formato del email"""
        if not email or not str(email).strip():
            return True, ""  # Email opcional
        
        email_str = str(email).strip().lower()
        
        # Patrón básico de email
        patron = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if re.match(patron, email_str):
            return True, ""
        return False, "Formato de email inválido. Ejemplo: nombre@dominio.com"
    
    @staticmethod
    def validar_fecha(fecha):
        """Valida que la fecha sea válida y tenga formato YYYY-MM-DD"""
        if not fecha or not str(fecha).strip():
            return True, ""  # Fecha opcional
        
        fecha_str = str(fecha).strip()
        
        # Verificar formato YYYY-MM-DD
        patron = r'^\d{4}-\d{2}-\d{2}$'
        if not re.match(patron, fecha_str):
            return False, "Formato de fecha inválido. Use YYYY-MM-DD (ejemplo: 1990-05-15)"
        
        try:
            fecha_obj = datetime.strptime(fecha_str, '%Y-%m-%d')
            
            # Verificar que la fecha no sea futura (con un margen de 1 día)
            hoy = datetime.now().date()
            if fecha_obj.date() > hoy:
                return False, "La fecha de nacimiento no puede ser futura"
            
            return True, ""
        except ValueError:
            return False, "Fecha inválida (día o mes incorrecto)"
    
    @staticmethod
    def validar_edad(fecha_nacimiento):
        """Calcula y valida la edad basada en la fecha de nacimiento"""
        if not fecha_nacimiento:
            return None, ""
        
        try:
            if isinstance(fecha_nacimiento, str):
                fecha = datetime.strptime(fecha_nacimiento, '%Y-%m-%d')
            else:
                fecha = fecha_nacimiento
            
            hoy = datetime.now()
            edad = hoy.year - fecha.year
            
            # Ajustar si aún no ha cumplido años este año
            if hoy.month < fecha.month or (hoy.month == fecha.month and hoy.day < fecha.day):
                edad -= 1
            
            if edad < 18:
                return edad, "La persona es menor de edad (debe tener al menos 18 años)"
            if edad > 100:
                return edad, "La edad parece ser incorrecta (más de 100 años)"
            
            return edad, ""
        except:
            return None, "Error al calcular la edad"
    
    @staticmethod
    def validar_numero_cuenta(numero_cuenta):
        """
        Valida el número de cuenta bancaria
        Debe tener exactamente 20 dígitos
        """
        if not numero_cuenta or not str(numero_cuenta).strip():
            return False, "El número de cuenta es obligatorio"
        
        cuenta_str = str(numero_cuenta).strip()
        
        # Eliminar espacios y guiones si los tiene
        cuenta_str = cuenta_str.replace(' ', '').replace('-', '')
        
        # Verificar que sean solo números
        if not cuenta_str.isdigit():
            return False, "El número de cuenta debe contener solo números"
        
        # Verificar longitud exacta de 20 dígitos
        if len(cuenta_str) != 20:
            return False, f"El número de cuenta debe tener exactamente 20 dígitos (actual: {len(cuenta_str)})"
        
        return True, ""
    
    @staticmethod
    def validar_estatus(estatus):
        """Valida que el estatus sea válido"""
        if not estatus:
            return False, "El estatus es obligatorio"
        
        estatus_str = str(estatus).upper().strip()
        if estatus_str not in ['ACTIVO', 'INACTIVO']:
            return False, "El estatus debe ser ACTIVO o INACTIVO"
        
        return True, ""
    
    @staticmethod
    def validar_nacionalidad(nacionalidad):
        """Valida la nacionalidad"""
        if not nacionalidad:
            return True, ""  # Opcional, por defecto V
        
        nacionalidad_str = str(nacionalidad).upper().strip()
        if nacionalidad_str not in ['V', 'E']:
            return False, "La nacionalidad debe ser V (Venezolano) o E (Extranjero)"
        
        return True, ""
    
    @staticmethod
    def validar_sexo(sexo):
        """Valida el sexo"""
        if not sexo:
            return True, ""  # Opcional
        
        sexo_str = str(sexo).upper().strip()
        if sexo_str not in ['M', 'F']:
            return False, "El sexo debe ser M (Masculino) o F (Femenino)"
        
        return True, ""
    
    @staticmethod
    def validar_talla_calzado(talla):
        """Valida la talla de calzado"""
        if not talla or not str(talla).strip():
            return True, ""  # Opcional
        
        try:
            talla_num = float(str(talla).strip())
            if talla_num < 20 or talla_num > 50:
                return False, "La talla de calzado debe estar entre 20 y 50"
            return True, ""
        except ValueError:
            return False, "La talla de calzado debe ser un número"
    
    @staticmethod
    def validar_talla_ropa(talla):
        """Valida la talla de ropa (pantalón/camisa)"""
        if not talla or not str(talla).strip():
            return True, ""  # Opcional
        
        talla_str = str(talla).upper().strip()
        tallas_validas = ['XS', 'S', 'M', 'L', 'XL', 'XXL', 'XXXL']
        
        if talla_str not in tallas_validas:
            return False, f"La talla debe ser una de: {', '.join(tallas_validas)}"
        
        return True, ""
    
    @staticmethod
    def validar_cantidad_hijos(cantidad):
        """Valida la cantidad de hijos"""
        if not cantidad or cantidad == "":
            return True, ""  # Opcional
        
        try:
            cantidad_int = int(cantidad)
            if cantidad_int < 0:
                return False, "La cantidad de hijos no puede ser negativa"
            if cantidad_int > 20:
                return False, "La cantidad de hijos parece excesiva (máximo 20)"
            return True, ""
        except ValueError:
            return False, "La cantidad de hijos debe ser un número entero"
    
    @staticmethod
    def validar_campos_obligatorios(datos):
        """
        Valida que los campos obligatorios no estén vacíos
        Campos obligatorios: cédula, nombres, estatus, número de cuenta
        """
        errores = []
        
        # Cédula
        if not datos.get('cedula') or not str(datos.get('cedula')).strip():
            errores.append("La cédula es obligatoria")
        
        # Nombres
        if not datos.get('nombres') or not str(datos.get('nombres')).strip():
            errores.append("Los nombres y apellidos son obligatorios")
        
        # Estatus
        if not datos.get('estatus') or not str(datos.get('estatus')).strip():
            errores.append("El estatus es obligatorio")
        
        # Número de cuenta
        if not datos.get('num_cuenta') or not str(datos.get('num_cuenta')).strip():
            errores.append("El número de cuenta es obligatorio")
        
        return errores
    

    @staticmethod
    def validar_fecha_ingreso(fecha):
        """Valida la fecha de ingreso (obligatoria, no puede ser futura)"""
        if not fecha or not str(fecha).strip():
            return False, "La fecha de ingreso es obligatoria"
        
        fecha_str = str(fecha).strip()
        
        # Verificar formato YYYY-MM-DD
        patron = r'^\d{4}-\d{2}-\d{2}$'
        if not re.match(patron, fecha_str):
            return False, "Formato de fecha inválido. Use YYYY-MM-DD (ejemplo: 2024-01-15)"
        
        try:
            fecha_obj = datetime.strptime(fecha_str, '%Y-%m-%d')
            
            # Verificar que la fecha no sea futura (con un margen de 1 día)
            hoy = datetime.now().date()
            if fecha_obj.date() > hoy:
                return False, "La fecha de ingreso no puede ser futura"
            
            return True, ""
        except ValueError:
            return False, "Fecha inválida (día o mes incorrecto)"