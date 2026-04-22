import hashlib
import secrets
from datetime import datetime
from database.conexion import db

class Seguridad:
    """Clase para manejar seguridad y autenticación"""
    
    @staticmethod
    def hash_contrasena(contrasena):
        """Genera hash SHA-256 de la contraseña (sin caracteres adicionales)"""
        # Limpiar la contraseña de posibles espacios o saltos de línea
        contrasena_limpia = contrasena.strip()
        return hashlib.sha256(contrasena_limpia.encode('utf-8')).hexdigest()
    
    @staticmethod
    def verificar_contrasena(contrasena, hash_almacenado):
        """Verifica si la contraseña coincide con el hash"""
        return Seguridad.hash_contrasena(contrasena) == hash_almacenado
    
    @staticmethod
    def generar_token():
        """Genera un token aleatorio para sesiones"""
        return secrets.token_hex(32)
    
    @staticmethod
    def autenticar_usuario(usuario, contrasena):
        """Autentica un usuario y retorna sus datos si es exitoso"""
        query = """
            SELECT id, nombre_usuario, nombre_completo, email, rol, activo
            FROM usuarios 
            WHERE nombre_usuario = %s
        """
        resultado = db.execute_query(query, (usuario,))
        
        if not resultado:
            return None, "Usuario no encontrado"
        
        user = resultado[0]
        
        if not user[5]:  # activo = False
            return None, "Usuario inactivo. Contacte al administrador"
        
        # Obtener hash de la contraseña
        query_pass = "SELECT contrasena FROM usuarios WHERE nombre_usuario = %s"
        hash_result = db.execute_query(query_pass, (usuario,))
        
        if not hash_result:
            return None, "Error al verificar contraseña"
        
        hash_almacenado = hash_result[0][0]
        hash_ingresado = Seguridad.hash_contrasena(contrasena.strip())
        
        # Depuración (eliminar después de resolver)
        print(f"Debug - Hash ingresado: {hash_ingresado}")
        print(f"Debug - Hash almacenado: {hash_almacenado}")
        
        if hash_ingresado == hash_almacenado:
            # Actualizar último acceso
            db.execute_query(
                "UPDATE usuarios SET ultimo_acceso = %s WHERE id = %s",
                (datetime.now(), user[0])
            )
            return {
                'id': user[0],
                'usuario': user[1],
                'nombre_completo': user[2],
                'email': user[3],
                'rol': user[4]
            }, None
        
        return None, "Contraseña incorrecta"
    
    @staticmethod
    def registrar_bitacora(usuario_id, usuario_nombre, accion, tabla_afectada=None, 
                          registro_id=None, descripcion=None, ip_address=None):
        """Registra una acción en la bitácora"""
        query = """
            INSERT INTO bitacora (usuario_id, usuario_nombre, accion, tabla_afectada, 
                                  registro_id, descripcion, ip_address, fecha)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        db.execute_query(query, (usuario_id, usuario_nombre, accion, tabla_afectada,
                                 registro_id, descripcion, ip_address, datetime.now()))
    
    @staticmethod
    def crear_usuario(usuario, contrasena, nombre_completo, email, rol):
        """Crea un nuevo usuario en el sistema"""
        # Verificar si el usuario ya existe
        query_check = "SELECT id FROM usuarios WHERE nombre_usuario = %s"
        existe = db.execute_query(query_check, (usuario,))
        
        if existe:
            return False, "El nombre de usuario ya existe"
        
        # Crear usuario
        hash_pass = Seguridad.hash_contrasena(contrasena)
        query = """
            INSERT INTO usuarios (nombre_usuario, contrasena, nombre_completo, email, rol, activo)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        db.execute_query(query, (usuario, hash_pass, nombre_completo, email, rol, True))
        
        return True, "Usuario creado exitosamente"
    
    @staticmethod
    def obtener_usuarios():
        """Obtiene lista de usuarios"""
        query = """
            SELECT id, nombre_usuario, nombre_completo, email, rol, activo, 
                   fecha_creacion, ultimo_acceso
            FROM usuarios
            ORDER BY id
        """
        return db.execute_query(query)
    
    @staticmethod
    def actualizar_usuario(user_id, nombre_completo, email, rol, activo):
        """Actualiza los datos de un usuario"""
        query = """
            UPDATE usuarios 
            SET nombre_completo = %s, email = %s, rol = %s, activo = %s
            WHERE id = %s
        """
        db.execute_query(query, (nombre_completo, email, rol, activo, user_id))
        return True, "Usuario actualizado exitosamente"
    
    @staticmethod
    def cambiar_contrasena(user_id, nueva_contrasena):
        """Cambia la contraseña de un usuario"""
        hash_pass = Seguridad.hash_contrasena(nueva_contrasena)
        query = "UPDATE usuarios SET contrasena = %s WHERE id = %s"
        db.execute_query(query, (hash_pass, user_id))
        return True, "Contraseña actualizada exitosamente"
    
    @staticmethod
    def eliminar_usuario(user_id):
        """Elimina un usuario (no permite eliminar el último administrador)"""
        # Verificar si es el único administrador
        query_admin = "SELECT COUNT(*) FROM usuarios WHERE rol = 'ADMINISTRADOR' AND activo = true"
        count_admin = db.execute_query(query_admin)[0][0]
        
        query_rol = "SELECT rol FROM usuarios WHERE id = %s"
        rol_usuario = db.execute_query(query_rol, (user_id,))
        
        if rol_usuario and rol_usuario[0][0] == 'ADMINISTRADOR' and count_admin <= 1:
            return False, "No se puede eliminar el único administrador del sistema"
        
        db.execute_query("DELETE FROM usuarios WHERE id = %s", (user_id,))
        return True, "Usuario eliminado exitosamente"
    
    @staticmethod
    def obtener_bitacora(filtro_usuario=None, limite=100):
        """Obtiene registros de la bitácora"""
        query = """
            SELECT b.id, b.usuario_nombre, b.accion, b.tabla_afectada, 
                   b.registro_id, b.descripcion, b.ip_address, b.fecha
            FROM bitacora b
        """
        params = []
        
        if filtro_usuario:
            query += " WHERE b.usuario_nombre = %s"
            params.append(filtro_usuario)
        
        query += " ORDER BY b.fecha DESC LIMIT %s"
        params.append(limite)
        
        return db.execute_query(query, tuple(params))


# Variable global para almacenar el usuario actual
usuario_actual = None

def set_usuario_actual(user):
    global usuario_actual
    usuario_actual = user

def get_usuario_actual():
    return usuario_actual

def tiene_permiso(rol_requerido):
    """Verifica si el usuario actual tiene el rol requerido"""
    if not usuario_actual:
        return False
    if rol_requerido == 'ADMINISTRADOR':
        return usuario_actual['rol'] == 'ADMINISTRADOR'
    if rol_requerido == 'USUARIO':
        return usuario_actual['rol'] in ['ADMINISTRADOR', 'USUARIO']
    return False