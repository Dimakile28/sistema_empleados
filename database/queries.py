from database.conexion import db

class Queries:
    """Clase con todas las consultas SQL necesarias"""
    
    @staticmethod
    def get_tipos_personal():
        """Obtiene todos los tipos de personal"""
        query = "SELECT id, nombre_tipo FROM tipos_personal ORDER BY id"
        return db.execute_query(query)
    
    @staticmethod
    def get_cargos():
        """Obtiene todos los cargos"""
        query = "SELECT id, nombre_cargo FROM cargos ORDER BY nombre_cargo"
        return db.execute_query(query)
    
    @staticmethod
    def get_tipos_nomina():
        """Obtiene todos los tipos de nómina"""
        query = "SELECT id, nombre_nomina FROM tipos_nomina ORDER BY id"
        return db.execute_query(query)
    
    @staticmethod
    def get_zonas_residencia():
        """Obtiene todas las zonas de residencia"""
        query = "SELECT id, nombre_zona FROM zonas_residencia ORDER BY nombre_zona"
        return db.execute_query(query)
    
    @staticmethod
    def get_parroquias():
        """Obtiene todas las parroquias"""
        query = "SELECT id, nombre_parroquia FROM parroquias ORDER BY nombre_parroquia"
        return db.execute_query(query)
    
    @staticmethod
    def get_bancos():
        """Obtiene todos los bancos"""
        query = "SELECT id, codigo_banco, nombre_banco FROM bancos WHERE activo = true ORDER BY nombre_banco"
        return db.execute_query(query)
    
    @staticmethod
    def insertar_empleado(datos):
        """Inserta un nuevo empleado"""
        query = """
            INSERT INTO empleados (
                estatus, nombres_apellidos, cedula, nacionalidad, numero_cuenta,
                id_tipo_nomina, fecha_nacimiento, edad, sexo, estado_civil,
                tipo_sangre, cantidad_hijos, hijos_0_5, hijos_6_12, hijos_13_18,
                nivel_academico, id_zona_residencia, sector, telefono,
                correo_electronico, condicion, usa_lentes, talla_calzado,
                talla_pantalon, talla_camisa, id_cargo, area, grupo, 
                id_tipo_personal, id_parroquia, fecha_ingreso, id_banco
            ) VALUES (
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
            ) RETURNING id
        """
        return db.execute_query(query, datos)
    
    @staticmethod
    def buscar_empleado(cedula=None, nombre=None, apellido=None, solo_activos=False):
        """
        Busca empleados por diferentes criterios
        """
        conditions = []
        params = []
        
        if cedula:
            conditions.append("e.cedula = %s")
            params.append(cedula)
        if nombre:
            conditions.append("e.nombres_apellidos ILIKE %s")
            params.append(f"%{nombre}%")
        if apellido:
            conditions.append("e.nombres_apellidos ILIKE %s")
            params.append(f"%{apellido}%")
        
        if solo_activos:
            conditions.append("e.estatus = 'ACTIVO'")
        
        where_clause = " AND ".join(conditions) if conditions else "1=1"
        
        query = f"""
            SELECT e.id, e.cedula, e.nombres_apellidos, e.estatus,
                c.nombre_cargo, tp.nombre_tipo, tn.nombre_nomina,
                z.nombre_zona, p.nombre_parroquia, e.telefono,
                e.correo_electronico, e.fecha_nacimiento, e.edad,
                e.sexo, e.estado_civil, e.tipo_sangre, e.cantidad_hijos,
                e.nivel_academico, e.sector, e.condicion, e.usa_lentes,
                e.talla_calzado, e.talla_pantalon, e.talla_camisa,
                e.area, e.grupo, e.numero_cuenta, e.fecha_ingreso,
                b.nombre_banco, b.codigo_banco
            FROM empleados e
            LEFT JOIN cargos c ON e.id_cargo = c.id
            LEFT JOIN tipos_personal tp ON e.id_tipo_personal = tp.id
            LEFT JOIN tipos_nomina tn ON e.id_tipo_nomina = tn.id
            LEFT JOIN zonas_residencia z ON e.id_zona_residencia = z.id
            LEFT JOIN parroquias p ON e.id_parroquia = p.id
            LEFT JOIN bancos b ON e.id_banco = b.id
            WHERE {where_clause}
            ORDER BY e.nombres_apellidos
        """
        return db.execute_query(query, tuple(params))
    
    @staticmethod
    def obtener_empleado_por_id(empleado_id):
        """Obtiene un empleado específico por su ID con TODOS los campos"""
        query = """
            SELECT 
                e.id, e.estatus, e.fecha_ingreso, e.nombres_apellidos, e.cedula,
                e.nacionalidad, e.numero_cuenta, e.id_tipo_nomina, e.fecha_nacimiento, e.edad,
                e.sexo, e.estado_civil, e.tipo_sangre, e.cantidad_hijos, e.hijos_0_5,
                e.hijos_6_12, e.hijos_13_18, e.nivel_academico, e.id_zona_residencia,
                e.sector, e.telefono, e.correo_electronico, e.condicion, e.usa_lentes,
                e.talla_calzado, e.talla_pantalon, e.talla_camisa, e.id_cargo,
                e.area, e.grupo, e.id_tipo_personal, e.id_parroquia, e.id_banco
            FROM empleados e
            WHERE e.id = %s
        """
        resultado = db.execute_query(query, (empleado_id,))
        return resultado[0] if resultado else None
    
    @staticmethod
    def actualizar_empleado(empleado_id, datos):
        """Actualiza los datos de un empleado"""
        query = """
            UPDATE empleados SET
                estatus = %s, nombres_apellidos = %s, nacionalidad = %s,
                numero_cuenta = %s, id_tipo_nomina = %s, fecha_nacimiento = %s,
                edad = %s, sexo = %s, estado_civil = %s, tipo_sangre = %s,
                cantidad_hijos = %s, hijos_0_5 = %s, hijos_6_12 = %s, hijos_13_18 = %s,
                nivel_academico = %s, id_zona_residencia = %s, sector = %s,
                telefono = %s, correo_electronico = %s, condicion = %s, usa_lentes = %s,
                talla_calzado = %s, talla_pantalon = %s, talla_camisa = %s, id_cargo = %s,
                area = %s, grupo = %s, id_tipo_personal = %s, id_parroquia = %s, id_banco = %s
            WHERE id = %s
        """
        params = list(datos) + [empleado_id]
        return db.execute_query(query, tuple(params))
    
    @staticmethod
    def eliminar_empleado(empleado_id):
        """Cambia el estatus del empleado a INACTIVO"""
        query = "UPDATE empleados SET estatus = 'INACTIVO' WHERE id = %s"
        return db.execute_query(query, (empleado_id,))
    
    @staticmethod
    def contar_empleados():
        """Cuenta el total de empleados activos"""
        query = "SELECT COUNT(*) FROM empleados WHERE estatus = 'ACTIVO'"
        resultado = db.execute_query(query)
        return resultado[0][0] if resultado else 0
    
    @staticmethod
    def obtener_todos_empleados():
        """Obtiene todos los empleados para exportación"""
        query = """
            SELECT e.cedula, e.nombres_apellidos, e.estatus,
                   c.nombre_cargo, tp.nombre_tipo, tn.nombre_nomina,
                   z.nombre_zona, p.nombre_parroquia, e.telefono,
                   e.correo_electronico, e.fecha_nacimiento, e.edad,
                   e.sexo, e.estado_civil, e.tipo_sangre, e.cantidad_hijos,
                   e.nivel_academico, e.sector, e.condicion,
                   CASE WHEN e.usa_lentes THEN 'SI' ELSE 'NO' END as usa_lentes,
                   e.talla_calzado, e.talla_pantalon, e.talla_camisa,
                   e.area, e.grupo, e.numero_cuenta, e.fecha_ingreso,
                   b.nombre_banco, b.codigo_banco
            FROM empleados e
            LEFT JOIN cargos c ON e.id_cargo = c.id
            LEFT JOIN tipos_personal tp ON e.id_tipo_personal = tp.id
            LEFT JOIN tipos_nomina tn ON e.id_tipo_nomina = tn.id
            LEFT JOIN zonas_residencia z ON e.id_zona_residencia = z.id
            LEFT JOIN parroquias p ON e.id_parroquia = p.id
            LEFT JOIN bancos b ON e.id_banco = b.id
            WHERE e.estatus = 'ACTIVO'
            ORDER BY e.nombres_apellidos
        """
        return db.execute_query(query)
    
    @staticmethod
    def contar_empleados_activos():
        """Cuenta el total de empleados activos"""
        query = "SELECT COUNT(*) FROM empleados WHERE estatus = 'ACTIVO'"
        resultado = db.execute_query(query)
        return resultado[0][0] if resultado else 0

    @staticmethod
    def contar_empleados_inactivos():
        """Cuenta el total de empleados inactivos"""
        query = "SELECT COUNT(*) FROM empleados WHERE estatus = 'INACTIVO'"
        resultado = db.execute_query(query)
        return resultado[0][0] if resultado else 0

    @staticmethod
    def contar_empleados():
        """Cuenta el total de empleados (activos + inactivos)"""
        query = "SELECT COUNT(*) FROM empleados"
        resultado = db.execute_query(query)
        return resultado[0][0] if resultado else 0