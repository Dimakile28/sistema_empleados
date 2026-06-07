# SIGEP - Sistema Integral de Gestión de Personal

![Versión](https://img.shields.io/badge/version-1.0-blue)
![Python](https://img.shields.io/badge/python-3.14-green)
![PostgreSQL](https://img.shields.io/badge/postgresql-17-blue)
![License](https://img.shields.io/badge/license-Proprietary-red)

## 📋 Descripción General

SIGEP es una aplicación de escritorio para la gestión completa del personal, desarrollada en Python con interfaz gráfica Tkinter y base de datos PostgreSQL. Permite registrar, consultar, modificar, exportar datos y gestionar suspensiones temporales de empleados.

## 🚀 Características Principales

- ✅ **Registro de Personal**: Formulario completo con validaciones
- ✅ **Carga Masiva**: Importación desde archivos Excel
- ✅ **Consulta de Personal**: Búsqueda por cédula, nombre o apellido
- ✅ **Modificación de Datos**: Edición completa de empleados
- ✅ **Suspensiones Temporales**: Control de ausencias (vacaciones, licencias)
- ✅ **Exportación a Excel**: Datos de personal y asistencia/nómina
- ✅ **Control de Acceso**: Temporizador para activar/desactivar el sistema
- ✅ **Administración de Usuarios**: Gestión de roles (ADMINISTRADOR/USUARIO)
- ✅ **Bitácora de Actividades**: Registro de todas las acciones

## 🛠️ Tecnologías Utilizadas

| Tecnología | Versión | Uso |
|------------|---------|-----|
| Python | 3.14.0 | Lenguaje principal |
| PostgreSQL | 17 | Base de datos relacional |
| psycopg2 | 2.9.12 | Conector PostgreSQL |
| Tkinter | - | Interfaz gráfica |
| pandas | 2.0.3 | Manipulación de datos |
| openpyxl | 3.1.2 | Archivos Excel |
| PyInstaller | 6.20.0 | Compilación a ejecutable |

## 📁 Estructura del Proyecto

```
sistema_gestion_personal/
│
├── main.py                          # Punto de entrada
├── requirements.txt                 # Dependencias
│
├── database/                        # Capa de acceso a datos
│   ├── conexion.py                  # Conexión a PostgreSQL
│   └── queries.py                   # Consultas SQL
│
├── ventanas/                        # Interfaz de usuario
│   ├── login.py                     # Inicio de sesión
│   ├── menu_principal.py            # Menú principal
│   ├── registro_personal.py         # Registro de empleados
│   ├── consulta_personal.py         # Consulta de empleados
│   ├── modificar_personal.py        # Modificación de empleados
│   ├── suspensiones.py              # Suspensiones temporales
│   ├── exportar_datos.py            # Exportación a Excel
│   ├── exportar_asistencia.py       # Exportación con plantilla
│   ├── configuracion.py             # Configuración del sistema
│   ├── carga_masiva.py              # Importación masiva
│   ├── usuarios.py                  # Administración de usuarios
│   └── control_acceso.py            # Control de acceso temporal
│
└── utils/                           # Utilidades
    ├── validaciones.py              # Validaciones de datos
    └── seguridad.py                 # Autenticación y bitácora
```

## 🗄️ Diagrama de Base de Datos

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│    usuarios     │     │    cargos       │     │  tipos_nomina   │
├─────────────────┤     ├─────────────────┤     ├─────────────────┤
│ id (PK)         │     │ id (PK)         │     │ id (PK)         │
│ nombre_usuario  │     │ nombre_cargo    │     │ nombre_nomina   │
│ contrasena      │     └─────────────────┘     └─────────────────┘
│ nombre_completo │
│ rol             │     ┌─────────────────┐     ┌─────────────────┐
│ activo          │     │ tipos_personal  │     │ zonas_residencia│
└─────────────────┘     ├─────────────────┤     ├─────────────────┤
                        │ id (PK)         │     │ id (PK)         │
┌─────────────────┐     │ nombre_tipo     │     │ nombre_zona     │
│   parroquias    │     └─────────────────┘     └─────────────────┘
├─────────────────┤
│ id (PK)         │     ┌─────────────────────────────────────────┐
│ nombre_parroquia│     │               empleados                  │
└─────────────────┘     ├─────────────────────────────────────────┤
                        │ id (PK), cedula (UK), nombres_apellidos │
┌─────────────────┐     │ estatus, suspendido, fechas_suspension  │
│  control_acceso │     │ motivo_suspension, suspendido_por       │
├─────────────────┤     │ id_cargo (FK), id_tipo_nomina (FK)      │
│ id (PK)         │     │ id_zona_residencia (FK)                 │
│ activado        │     │ id_tipo_personal (FK), id_parroquia (FK)│
│ modo_temporizador│     └─────────────────────────────────────────┘
│ fecha_inicio    │
│ fecha_fin       │     ┌─────────────────┐
│ mensaje         │     │    bitacora     │
└─────────────────┘     ├─────────────────┤
                        │ id (PK)         │
                        │ usuario_id (FK) │
                        │ accion          │
                        │ fecha           │
                        └─────────────────┘
```

## 📥 Instalación

### Requisitos Previos

- **Python 3.11, 3.12 o 3.14** (recomendado 3.11)
- **PostgreSQL 14, 15, 16 o 17** instalado y corriendo
- **Git** (opcional, para clonar el repositorio)

### Pasos de Instalación

```bash
# 1. Clonar o descargar el proyecto
git clone https://github.com/tu-usuario/sigep.git
cd sigep

# 2. Crear y activar entorno virtual (Python 3.11 recomendado)
C:\Python311\python -m venv venv_sigep
venv_sigep\Scripts\activate

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Configurar base de datos
#    - Crear base de datos 'sistema_nomina' en PostgreSQL
#    - Ejecutar el script 'prueba.sql' (incluye todas las tablas)
```

### Configuración de Conexión

Editar `database/conexion.py`:

```python
self.config = {
    'host': 'localhost',     # IP del servidor PostgreSQL
    'port': '5432',          # Puerto (default 5432)
    'database': 'sistema_nomina',
    'user': 'postgres',      # Usuario de PostgreSQL
    'password': '1234'       # Contraseña
}
```

### Ejecutar la Aplicación

```bash
python main.py
```

### Credenciales por Defecto

| Usuario | Contraseña | Rol |
|---------|------------|-----|
| admin | admin123 | ADMINISTRADOR |

## 🔧 Compilación a Ejecutable (.exe)

### Comando Completo

```powershell
cd "C:\ruta\del\proyecto"

C:\Python314\python.exe -m PyInstaller --onefile --windowed --name=SIGEP ^
    --hidden-import=psycopg2 ^
    --hidden-import=psycopg2._psycopg ^
    --hidden-import=psycopg2.extensions ^
    --hidden-import=psycopg2.extras ^
    --collect-all=psycopg2 ^
    --add-data "C:\Program Files\PostgreSQL\17\bin\libpq.dll;." ^
    --add-data "database;database" ^
    --add-data "ventanas;ventanas" ^
    --add-data "utils;utils" ^
    main.py
```

### Script de Compilación (compilar.bat)

```batch
@echo off
cd /d "C:\ruta\del\proyecto"
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
C:\Python314\python.exe -m PyInstaller --onefile --windowed --name=SIGEP ^
    --hidden-import=psycopg2 --collect-all=psycopg2 ^
    --add-data "C:\Program Files\PostgreSQL\17\bin\libpq.dll;." ^
    --add-data "database;database" --add-data "ventanas;ventanas" --add-data "utils;utils" ^
    main.py
pause
```

> **Nota**: El ejecutable generado estará en `dist/SIGEP.exe`

## 📖 Guía de Uso

### 1. Inicio de Sesión
- Usuario por defecto: `admin`
- Contraseña por defecto: `admin123`

### 2. Registro de Personal
- Complete todos los campos obligatorios (*)
- Los campos con lista desplegable solo permiten valores predefinidos
- El número de cuenta debe tener exactamente 20 dígitos

### 3. Suspensiones Temporales
- Seleccione un empleado activo
- Defina fechas de inicio y fin
- Indique el motivo de suspensión
- El empleado no aparecerá en reportes de nómina durante el período

### 4. Exportación de Asistencia
- Seleccione su plantilla Excel personalizada
- Ingrese la fecha de inicio del período
- Ingrese la tasa de cambio del mes
- El sistema llenará automáticamente los datos

### 5. Control de Acceso
- **Modo Manual**: Active/Desactive el sistema instantáneamente
- **Modo Temporizador**: Programe horarios de acceso

## 👥 Roles y Permisos

| Rol | Permisos |
|-----|----------|
| **ADMINISTRADOR** | Acceso total a todos los módulos |
| **USUARIO** | Registro, consulta, modificación, exportación |

## 🔒 Seguridad

- Contraseñas encriptadas con SHA-256
- Bitácora de todas las acciones de usuarios
- Control de acceso temporal al sistema
- Roles y permisos diferenciados

## 🛠️ Guía para Desarrolladores

### Agregar un Nuevo Campo a Empleados

1. **Modificar BD**: `ALTER TABLE empleados ADD COLUMN nuevo_campo VARCHAR(100);`
2. **Actualizar queries.py**: Modificar `insertar_empleado()`, `actualizar_empleado()`, `obtener_empleado_por_id()`
3. **Actualizar registro_personal.py**: Agregar campo en formulario y validación
4. **Actualizar modificar_personal.py**: Agregar campo en edición
5. **Actualizar exportar_datos.py**: Agregar a lista de campos exportables

### Agregar un Nuevo Módulo

1. Crear archivo en `ventanas/nuevo_modulo.py`
2. Importar en `ventanas/__init__.py`
3. Agregar botón en `menu_principal.py`

### Convenciones de Código

- **Clases**: PascalCase (`VentanaRegistro`)
- **Métodos**: snake_case (`guardar_empleado()`)
- **Variables**: snake_case (`id_empleado`)
- **Constantes**: UPPER_CASE (`MAX_INTENTOS`)

## 🐛 Solución de Problemas Comunes

### Error: "No module named 'psycopg2'"
```bash
pip install psycopg2-binary
```

### Error: "connection refused"
- Verificar que PostgreSQL esté corriendo
- Verificar credenciales en `database/conexion.py`

### Error al compilar: "No module named 'psycopg2'"
- Incluir `--hidden-import=psycopg2` en comando PyInstaller
- Incluir DLLs de PostgreSQL con `--add-data`

## 📋 Dependencias

```
psycopg2-binary==2.9.9
pandas==2.0.3
openpyxl==3.1.2
Pillow==10.0.0
pyinstaller==6.20.0
```

## 🔮 Mejoras Futuras

- [ ] Módulo de reportes gráficos (Dashboard)
- [ ] Notificaciones por email
- [ ] Módulo de vacaciones y permisos
- [ ] Integración con sistemas de nómina externos
- [ ] Historial de cambios de empleados
- [ ] Exportación a PDF de constancias
- [ ] Modo oscuro/claro
- [ ] API REST para integraciones

## 📞 Contacto y Soporte

| Tipo | Información |
|------|-------------|
| **Desarrollador** | DIMAIKEL SANTIAGO |
| **Email** | dsantiagojb@gmail.com |
| **Versión** | 1.0 |
| **Última actualización** | 2026 |

