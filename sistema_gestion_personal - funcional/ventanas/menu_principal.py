import tkinter as tk
from tkinter import ttk, messagebox
from database.conexion import db
from ventanas.registro_personal import VentanaRegistro
from ventanas.consulta_personal import VentanaConsulta
from ventanas.modificar_personal import VentanaModificar
from ventanas.exportar_datos import VentanaExportar
from ventanas.configuracion import VentanaConfiguracion
from ventanas.carga_masiva import VentanaCargaMasiva
from ventanas.exportar_asistencia import VentanaExportarAsistencia
from ventanas.usuarios import VentanaUsuarios
from utils.seguridad import get_usuario_actual, set_usuario_actual, Seguridad, tiene_permiso

class MenuPrincipal:
    """Ventana principal del sistema"""
    
    def __init__(self):
        self.ventana = tk.Tk()
        self.ventana.title("Sistema de Gestión de Personal - SIGEP")
        self.ventana.geometry("800x650")
        self.ventana.resizable(False, False)
        
        # Centrar la ventana
        self.centrar_ventana()
        
        # Conectar a la base de datos
        if not db.connect():
            messagebox.showerror("Error", "No se pudo conectar a la base de datos")
            self.ventana.destroy()
            return
        
        # Configurar estilo
        self.configurar_estilo()
        
        # Crear interfaz
        self.crear_interfaz()
        
        # Cargar datos iniciales
        self.cargar_estadisticas()
        
        self.ventana.mainloop()
    
    def centrar_ventana(self):
        """Centra la ventana en la pantalla"""
        self.ventana.update_idletasks()
        ancho = 800
        alto = 950
        x = (self.ventana.winfo_screenwidth() // 2) - (ancho // 2)
        y = (self.ventana.winfo_screenheight() // 2) - (alto // 2)
        self.ventana.geometry(f'{ancho}x{alto}+{x}+{y}')
    
    def configurar_estilo(self):
        """Configura el estilo de la aplicación"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configurar colores
        style.configure('Title.TLabel', font=('Helvetica', 24, 'bold'), foreground='#2c3e50')
        style.configure('Subtitle.TLabel', font=('Helvetica', 12), foreground='#7f8c8d')
        style.configure('Stat.TLabel', font=('Helvetica', 11))
        style.configure('StatValue.TLabel', font=('Helvetica', 18, 'bold'), foreground='#3498db')
        
        # Configurar botones
        style.configure('Menu.TButton', font=('Helvetica', 11), padding=10)
    
    def crear_interfaz(self):
        """Crea la interfaz de la ventana principal"""
        
        # Frame superior con información del usuario
        top_frame = ttk.Frame(self.ventana)
        top_frame.pack(fill=tk.X, padx=10, pady=5)
        
        usuario_actual = get_usuario_actual()
        
        if usuario_actual:
            ttk.Label(top_frame, text=f"👤 {usuario_actual['nombre_completo']} ({usuario_actual['rol']})", 
                    font=('Helvetica', 9)).pack(side=tk.LEFT)
            
            btn_cerrar_sesion = tk.Button(top_frame, text="Cerrar Sesión", command=self.cerrar_sesion,
                                        bg="#e74c3c", fg="white", font=('Helvetica', 9),
                                        padx=10, pady=2, cursor='hand2')
            btn_cerrar_sesion.pack(side=tk.RIGHT)
        
        # Frame principal
        main_frame = ttk.Frame(self.ventana, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Título
        titulo = ttk.Label(main_frame, text="SIGEP", style='Title.TLabel')
        titulo.pack(pady=(0, 5))
        
        subtitulo = ttk.Label(main_frame, text="Sistema Integral de Gestión de Personal", 
                            style='Subtitle.TLabel')
        subtitulo.pack(pady=(0, 30))
        
        # Frame para estadísticas
        stats_frame = ttk.LabelFrame(main_frame, text="Estadísticas", padding="15")
        stats_frame.pack(fill=tk.X, pady=(0, 20))
        
        self.stats_vars = {}
        stats_grid = ttk.Frame(stats_frame)
        stats_grid.pack()
        
        # Estadísticas - PRIMERA FILA
        estadisticas_fila1 = [
            ("Total Empleados", "total_empleados"),
            ("Empleados Activos", "empleados_activos"),
            ("Empleados Inactivos", "empleados_inactivos"),
        ]
        
        for i, (label, var_name) in enumerate(estadisticas_fila1):
            frame = ttk.Frame(stats_grid)
            frame.grid(row=0, column=i, padx=20, pady=5)
            
            ttk.Label(frame, text=label, style='Stat.TLabel').pack()
            self.stats_vars[var_name] = ttk.Label(frame, text="0", style='StatValue.TLabel')
            self.stats_vars[var_name].pack()
        
        # Estadísticas - SEGUNDA FILA (tipos de personal)
        estadisticas_fila2 = [
            ("Directivos", "directivos"),
            ("Administrativos", "administrativos"),
            ("Operativos", "operativos"),
        ]
        
        for i, (label, var_name) in enumerate(estadisticas_fila2):
            frame = ttk.Frame(stats_grid)
            frame.grid(row=1, column=i, padx=20, pady=5)
            
            ttk.Label(frame, text=label, style='Stat.TLabel').pack()
            self.stats_vars[var_name] = ttk.Label(frame, text="0", style='StatValue.TLabel')
            self.stats_vars[var_name].pack()
            
        # Frame para botones de menú
        menu_frame = ttk.Frame(main_frame)
        menu_frame.pack(fill=tk.BOTH, expand=True, pady=20)
        
        # Botones
        botones = [
            ("📝 Registrar Personal", self.abrir_registro, "#2ecc71"),
            ("📥 Carga Masiva", self.abrir_carga_masiva, "#1abc9c"),
            ("🔍 Consultar Personal", self.abrir_consulta, "#3498db"),
            ("✏️ Modificar Personal", self.abrir_modificar, "#f39c12"),
            ("⚙️ Configuración", self.abrir_configuracion, "#8e44ad"),
            ("📊 Exportar Datos", self.abrir_exportar, "#9b59b6"),
            ("💰 Exportar Asistencia", self.abrir_exportar_asistencia, "#e67e22"),
        ]
        
        # Solo mostrar administración de usuarios si es ADMINISTRADOR
        if tiene_permiso('ADMINISTRADOR'):
            botones.insert(5, ("👥 Administrar Usuarios", self.abrir_usuarios, "#16a085"))
        
        botones.append(("❌ Salir", self.salir, "#e74c3c"))
        
        for i, (texto, comando, color) in enumerate(botones):
            btn = tk.Button(menu_frame, text=texto, command=comando,
                           font=('Helvetica', 12), bg=color, fg='white',
                           relief=tk.RAISED, bd=2, padx=20, pady=10,
                           cursor='hand2', activebackground='#34495e')
            btn.pack(pady=8, fill=tk.X, padx=50)
            
            # Cambiar color al pasar el mouse
            def on_enter(e, btn=btn, color=color):
                btn['background'] = '#34495e'
            def on_leave(e, btn=btn, color=color):
                btn['background'] = color
            
            btn.bind("<Enter>", on_enter)
            btn.bind("<Leave>", on_leave)
        
        # Footer
        footer = ttk.Label(main_frame, text="© 2024 - Sistema de Gestión de Personal", 
                          style='Subtitle.TLabel')
        footer.pack(side=tk.BOTTOM, pady=(20, 0))
    
    def cargar_estadisticas(self):
        """Carga las estadísticas desde la base de datos"""
        from database.queries import Queries
        
        try:
            # Total de empleados ACTIVOS
            total_activos = db.execute_query("SELECT COUNT(*) FROM empleados WHERE estatus = 'ACTIVO'")
            total_activos = total_activos[0][0] if total_activos else 0
            
            # Total de empleados INACTIVOS
            total_inactivos = db.execute_query("SELECT COUNT(*) FROM empleados WHERE estatus = 'INACTIVO'")
            total_inactivos = total_inactivos[0][0] if total_inactivos else 0
            
            # Total de empleados GENERAL
            total_general = total_activos + total_inactivos
            
            # Actualizar variables de estadísticas
            self.stats_vars['total_empleados'].config(text=str(total_general))
            self.stats_vars['empleados_activos'].config(text=str(total_activos))
            self.stats_vars['empleados_inactivos'].config(text=str(total_inactivos))
            
            # Contar por tipo de personal (solo activos)
            query = """
                SELECT tp.nombre_tipo, COUNT(e.id)
                FROM empleados e
                LEFT JOIN tipos_personal tp ON e.id_tipo_personal = tp.id
                WHERE e.estatus = 'ACTIVO'
                GROUP BY tp.nombre_tipo
            """
            resultados = db.execute_query(query)
            
            for tipo, cantidad in resultados:
                if tipo == 'DIRECTIVO':
                    self.stats_vars['directivos'].config(text=str(cantidad))
                elif tipo == 'ADMINISTRATIVO':
                    self.stats_vars['administrativos'].config(text=str(cantidad))
                elif tipo == 'OPERATIVO':
                    self.stats_vars['operativos'].config(text=str(cantidad))
                    
        except Exception as e:
            print(f"Error cargando estadísticas: {e}")
    
    def abrir_registro(self):
        """Abre la ventana de registro"""
        VentanaRegistro(self.ventana, self.cargar_estadisticas)
    
    def abrir_carga_masiva(self):
        """Abre la ventana de carga masiva"""
        VentanaCargaMasiva(self.ventana, self.cargar_estadisticas)
    
    def abrir_consulta(self):
        """Abre la ventana de consulta"""
        VentanaConsulta(self.ventana)
    
    def abrir_modificar(self):
        """Abre la ventana de modificación"""
        VentanaModificar(self.ventana, self.cargar_estadisticas)
    
    def abrir_configuracion(self):
        """Abre la ventana de configuración"""
        VentanaConfiguracion(self.ventana)
    
    def abrir_exportar(self):
        """Abre la ventana de exportación"""
        VentanaExportar(self.ventana)
    
    def abrir_exportar_asistencia(self):
        """Abre la ventana de exportación de asistencia"""
        VentanaExportarAsistencia(self.ventana)
    
    def abrir_usuarios(self):
        """Abre la ventana de administración de usuarios"""
        VentanaUsuarios(self.ventana)
    
    def cerrar_sesion(self):
        """Cierra la sesión actual"""
        usuario_actual = get_usuario_actual()
        
        if usuario_actual:
            Seguridad.registrar_bitacora(
                usuario_actual['id'], usuario_actual['usuario'], 
                "CIERRE DE SESIÓN"
            )
        
        set_usuario_actual(None)
        self.ventana.destroy()
        
        from ventanas.login import VentanaLogin
        VentanaLogin()
    
    def salir(self):
        """Sale de la aplicación"""
        if messagebox.askyesno("Salir", "¿Está seguro que desea salir?"):
            db.disconnect()
            self.ventana.destroy()

if __name__ == "__main__":
    MenuPrincipal()