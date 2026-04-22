import psycopg2
from psycopg2 import sql, Error
import sys
import os

class DatabaseConnection:
    """Gestor de conexión a PostgreSQL"""
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DatabaseConnection, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance
    
    def _initialize(self):
        """Inicializa la conexión"""
        self.connection = None
        self.cursor = None
        self.config = {
            'host': 'localhost',
            'port': '5432',
            'database': 'sistema_nomina',
            'user': 'postgres',
            'password': '1234'
        }
    
    def connect(self):
        """Establece la conexión con la base de datos"""
        try:
            self.connection = psycopg2.connect(
                host=self.config['host'],
                port=self.config['port'],
                database=self.config['database'],
                user=self.config['user'],
                password=self.config['password']
            )
            self.cursor = self.connection.cursor()
            return True
        except Error as e:
            print(f"Error de conexión: {e}")
            return False
    
    def disconnect(self):
        """Cierra la conexión"""
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
    
    def execute_query(self, query, params=None):
        """Ejecuta una consulta y retorna resultados"""
        try:
            if not self.connection or self.connection.closed:
                self.connect()
            
            self.cursor.execute(query, params or ())
            
            if query.strip().upper().startswith('SELECT'):
                return self.cursor.fetchall()
            else:
                self.connection.commit()
                return self.cursor.rowcount
        except Error as e:
            print(f"Error en consulta: {e}")
            self.connection.rollback()
            return None
    
    def get_cursor(self):
        """Retorna el cursor para operaciones más complejas"""
        if not self.connection or self.connection.closed:
            self.connect()
        return self.cursor

# Instancia global
db = DatabaseConnection()