import tkinter as tk
from tkinter import ttk, messagebox
from database.conexion import db
from utils.seguridad import Seguridad, set_usuario_actual

class VentanaLogin:
    """Ventana de inicio de sesión"""
    
    def __init__(self):
        self.ventana = tk.Tk()
        self.ventana.title("Sistema de Gestión de Personal - Inicio de Sesión")
        self.ventana.geometry("450x350")
        self.ventana.resizable(False, False)
        
        self.centrar_ventana()
        self.conectar_base_datos()
        self.crear_interfaz()
        
        self.ventana.mainloop()
    
    def centrar_ventana(self):
        self.ventana.update_idletasks()
        ancho = 450
        alto = 350
        x = (self.ventana.winfo_screenwidth() // 2) - (ancho // 2)
        y = (self.ventana.winfo_screenheight() // 2) - (alto // 2)
        self.ventana.geometry(f'{ancho}x{alto}+{x}+{y}')
    
    def conectar_base_datos(self):
        if not db.connect():
            messagebox.showerror("Error", "No se pudo conectar a la base de datos")
            self.ventana.destroy()
            return
    
    def crear_interfaz(self):
        # Frame principal
        main_frame = ttk.Frame(self.ventana, padding="30")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Logo o título
        titulo = ttk.Label(main_frame, text="SIGEP", 
                          font=('Helvetica', 24, 'bold'))
        titulo.pack(pady=(0, 5))
        
        subtitulo = ttk.Label(main_frame, text="Sistema Integral de Gestión de Personal",
                             font=('Helvetica', 10))
        subtitulo.pack(pady=(0, 30))
        
        # Frame para formulario
        form_frame = ttk.Frame(main_frame)
        form_frame.pack(pady=20)
        
        # Usuario
        ttk.Label(form_frame, text="Usuario:", font=('Helvetica', 11)).grid(row=0, column=0, sticky='w', pady=10)
        self.usuario_var = tk.StringVar()
        entry_usuario = ttk.Entry(form_frame, textvariable=self.usuario_var, width=25, font=('Helvetica', 11))
        entry_usuario.grid(row=0, column=1, padx=10, pady=10)
        entry_usuario.focus()
        
        # Contraseña
        ttk.Label(form_frame, text="Contraseña:", font=('Helvetica', 11)).grid(row=1, column=0, sticky='w', pady=10)
        self.contrasena_var = tk.StringVar()
        entry_contrasena = ttk.Entry(form_frame, textvariable=self.contrasena_var, width=25, 
                                     font=('Helvetica', 11), show="•")
        entry_contrasena.grid(row=1, column=1, padx=10, pady=10)
        
        # Bind Enter para iniciar sesión
        entry_usuario.bind('<Return>', lambda e: self.iniciar_sesion())
        entry_contrasena.bind('<Return>', lambda e: self.iniciar_sesion())
        
        # Botón iniciar sesión
        btn_login = tk.Button(form_frame, text="Iniciar Sesión", command=self.iniciar_sesion,
                             bg="#2ecc71", fg="white", font=('Helvetica', 11, 'bold'),
                             padx=30, pady=8, cursor='hand2')
        btn_login.grid(row=2, column=0, columnspan=2, pady=20)
        
        # Mensaje de información
        info_frame = ttk.Frame(main_frame)
        info_frame.pack(pady=20)
        
        ttk.Label(info_frame, text="Usuario por defecto: admin", 
                 font=('Helvetica', 8), foreground='gray').pack()
        ttk.Label(info_frame, text="Contraseña por defecto: admin123", 
                 font=('Helvetica', 8), foreground='gray').pack()
        
        # Footer
        footer = ttk.Label(main_frame, text="© 2024 - Sistema de Gestión de Personal",
                          font=('Helvetica', 8), foreground='gray')
        footer.pack(side=tk.BOTTOM, pady=(20, 0))
    
    def iniciar_sesion(self):
        usuario = self.usuario_var.get().strip()
        contrasena = self.contrasena_var.get()
        
        if not usuario:
            messagebox.showerror("Error", "Ingrese su nombre de usuario")
            return
        
        if not contrasena:
            messagebox.showerror("Error", "Ingrese su contraseña")
            return
        
        # Autenticar
        user_data, error = Seguridad.autenticar_usuario(usuario, contrasena)
        
        if user_data:
            set_usuario_actual(user_data)
            
            # Registrar inicio de sesión en bitácora
            Seguridad.registrar_bitacora(
                user_data['id'], user_data['usuario'], 
                "INICIO DE SESIÓN", ip_address=self.obtener_ip()
            )
            
            self.ventana.destroy()
            from ventanas.menu_principal import MenuPrincipal
            MenuPrincipal()
        else:
            messagebox.showerror("Error", error)
    
    def obtener_ip(self):
        """Obtiene la IP local (simulada)"""
        import socket
        try:
            return socket.gethostbyname(socket.gethostname())
        except:
            return "127.0.0.1"