import tkinter as tk
from tkinter import ttk, messagebox
from database.conexion import db
from utils.seguridad import Seguridad, get_usuario_actual, tiene_permiso

class VentanaUsuarios:
    """Ventana para administrar usuarios del sistema"""
    
    def __init__(self, parent):
        self.parent = parent
        
        if not tiene_permiso('ADMINISTRADOR'):
            messagebox.showerror("Acceso Denegado", "Solo los administradores pueden acceder a esta sección")
            return
        
        self.ventana = tk.Toplevel(parent)
        self.ventana.title("Administración de Usuarios")
        self.ventana.geometry("900x650")
        self.ventana.transient(parent)
        self.ventana.grab_set()
        
        self.centrar_ventana()
        self.crear_interfaz()
        self.cargar_usuarios()
    
    def centrar_ventana(self):
        self.ventana.update_idletasks()
        ancho = 900
        alto = 650
        x = (self.ventana.winfo_screenwidth() // 2) - (ancho // 2)
        y = (self.ventana.winfo_screenheight() // 2) - (alto // 2)
        self.ventana.geometry(f'{ancho}x{alto}+{x}+{y}')
    
    def crear_interfaz(self):
        # Frame principal
        main_frame = ttk.Frame(self.ventana, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Título
        titulo = ttk.Label(main_frame, text="Administración de Usuarios",
                          font=('Helvetica', 14, 'bold'))
        titulo.pack(pady=(0, 10))
        
        # Frame para formulario de nuevo usuario
        form_frame = ttk.LabelFrame(main_frame, text="Registrar Nuevo Usuario", padding="10")
        form_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Campos del formulario
        ttk.Label(form_frame, text="Usuario:").grid(row=0, column=0, sticky='w', pady=5, padx=5)
        self.nuevo_usuario = tk.StringVar()
        ttk.Entry(form_frame, textvariable=self.nuevo_usuario, width=20).grid(row=0, column=1, pady=5, padx=5)
        
        ttk.Label(form_frame, text="Contraseña:").grid(row=0, column=2, sticky='w', pady=5, padx=5)
        self.nueva_contrasena = tk.StringVar()
        ttk.Entry(form_frame, textvariable=self.nueva_contrasena, width=20, show="•").grid(row=0, column=3, pady=5, padx=5)
        
        ttk.Label(form_frame, text="Nombre Completo:").grid(row=1, column=0, sticky='w', pady=5, padx=5)
        self.nuevo_nombre = tk.StringVar()
        ttk.Entry(form_frame, textvariable=self.nuevo_nombre, width=30).grid(row=1, column=1, columnspan=3, pady=5, padx=5, sticky='ew')
        
        ttk.Label(form_frame, text="Email:").grid(row=2, column=0, sticky='w', pady=5, padx=5)
        self.nuevo_email = tk.StringVar()
        ttk.Entry(form_frame, textvariable=self.nuevo_email, width=30).grid(row=2, column=1, columnspan=2, pady=5, padx=5, sticky='ew')
        
        ttk.Label(form_frame, text="Rol:").grid(row=2, column=3, sticky='w', pady=5, padx=5)
        self.nuevo_rol = tk.StringVar(value="USUARIO")
        combo_rol = ttk.Combobox(form_frame, textvariable=self.nuevo_rol, values=["ADMINISTRADOR", "USUARIO"], width=15, state="readonly")
        combo_rol.grid(row=2, column=4, pady=5, padx=5)
        
        btn_crear = tk.Button(form_frame, text="➕ Crear Usuario", command=self.crear_usuario,
                             bg="#2ecc71", fg="white", cursor='hand2')
        btn_crear.grid(row=3, column=0, columnspan=5, pady=10)
        
        # Frame para lista de usuarios
        list_frame = ttk.LabelFrame(main_frame, text="Usuarios del Sistema", padding="10")
        list_frame.pack(fill=tk.BOTH, expand=True)
        
        # Treeview
        scroll_y = ttk.Scrollbar(list_frame, orient="vertical")
        scroll_x = ttk.Scrollbar(list_frame, orient="horizontal")
        
        columnas = ("ID", "Usuario", "Nombre Completo", "Email", "Rol", "Activo", "Fecha Creación", "Último Acceso")
        
        self.tree_usuarios = ttk.Treeview(list_frame, columns=columnas, show="headings",
                                         yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)
        
        scroll_y.config(command=self.tree_usuarios.yview)
        scroll_x.config(command=self.tree_usuarios.xview)
        
        scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
        scroll_x.pack(side=tk.BOTTOM, fill=tk.X)
        self.tree_usuarios.pack(fill=tk.BOTH, expand=True)
        
        # Configurar columnas
        anchos = [40, 120, 200, 180, 100, 60, 120, 150]
        for col, ancho in zip(columnas, anchos):
            self.tree_usuarios.heading(col, text=col)
            self.tree_usuarios.column(col, width=ancho)
        
        # Botones de acción
        action_frame = ttk.Frame(main_frame)
        action_frame.pack(fill=tk.X, pady=10)
        
        btn_editar = tk.Button(action_frame, text="✏️ Editar Usuario", command=self.editar_usuario,
                              bg="#f39c12", fg="white", cursor='hand2')
        btn_editar.pack(side=tk.LEFT, padx=5)
        
        btn_cambiar_pass = tk.Button(action_frame, text="🔑 Cambiar Contraseña", command=self.cambiar_contrasena,
                                    bg="#3498db", fg="white", cursor='hand2')
        btn_cambiar_pass.pack(side=tk.LEFT, padx=5)
        
        btn_eliminar = tk.Button(action_frame, text="🗑️ Eliminar Usuario", command=self.eliminar_usuario,
                                bg="#e74c3c", fg="white", cursor='hand2')
        btn_eliminar.pack(side=tk.LEFT, padx=5)
        
        btn_refresh = tk.Button(action_frame, text="🔄 Actualizar", command=self.cargar_usuarios,
                               bg="#95a5a6", fg="white", cursor='hand2')
        btn_refresh.pack(side=tk.RIGHT, padx=5)
    
    def cargar_usuarios(self):
        """Carga la lista de usuarios"""
        for item in self.tree_usuarios.get_children():
            self.tree_usuarios.delete(item)
        
        usuarios = Seguridad.obtener_usuarios()
        if usuarios:
            for user in usuarios:
                activo = "✅" if user[5] else "❌"
                fecha_creacion = user[6].strftime('%Y-%m-%d %H:%M') if user[6] else ""
                ultimo_acceso = user[7].strftime('%Y-%m-%d %H:%M') if user[7] else "Nunca"
                self.tree_usuarios.insert("", tk.END, values=(
                    user[0], user[1], user[2], user[3], user[4], activo, fecha_creacion, ultimo_acceso
                ))
    
    def crear_usuario(self):
        """Crea un nuevo usuario"""
        usuario = self.nuevo_usuario.get().strip()
        contrasena = self.nueva_contrasena.get()
        nombre = self.nuevo_nombre.get().strip()
        email = self.nuevo_email.get().strip()
        rol = self.nuevo_rol.get()
        
        if not usuario:
            messagebox.showerror("Error", "El nombre de usuario es obligatorio")
            return
        
        if not contrasena:
            messagebox.showerror("Error", "La contraseña es obligatoria")
            return
        
        if len(contrasena) < 6:
            messagebox.showerror("Error", "La contraseña debe tener al menos 6 caracteres")
            return
        
        if not nombre:
            messagebox.showerror("Error", "El nombre completo es obligatorio")
            return
        
        exito, mensaje = Seguridad.crear_usuario(usuario, contrasena, nombre, email, rol)
        
        if exito:
            messagebox.showinfo("Éxito", mensaje)
            # Limpiar campos
            self.nuevo_usuario.set("")
            self.nueva_contrasena.set("")
            self.nuevo_nombre.set("")
            self.nuevo_email.set("")
            self.nuevo_rol.set("USUARIO")
            self.cargar_usuarios()
        else:
            messagebox.showerror("Error", mensaje)
    
    def editar_usuario(self):
        """Edita los datos de un usuario"""
        seleccion = self.tree_usuarios.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Seleccione un usuario para editar")
            return
        
        item = self.tree_usuarios.item(seleccion[0])
        user_id = item['values'][0]
        usuario_actual = item['values'][1]
        nombre_actual = item['values'][2]
        email_actual = item['values'][3]
        rol_actual = item['values'][4]
        activo_actual = item['values'][5] == "✅"
        
        # Ventana de edición
        edit_win = tk.Toplevel(self.ventana)
        edit_win.title(f"Editar Usuario - {usuario_actual}")
        edit_win.geometry("450x350")
        edit_win.transient(self.ventana)
        edit_win.grab_set()
        
        # Centrar ventana
        edit_win.update_idletasks()
        x = (edit_win.winfo_screenwidth() // 2) - 225
        y = (edit_win.winfo_screenheight() // 2) - 175
        edit_win.geometry(f'450x350+{x}+{y}')
        
        frame = ttk.Frame(edit_win, padding="20")
        frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(frame, text=f"Editando usuario: {usuario_actual}", 
                 font=('Helvetica', 12, 'bold')).pack(pady=(0, 20))
        
        # Campos
        ttk.Label(frame, text="Nombre Completo:").pack(anchor='w', pady=5)
        nombre_var = tk.StringVar(value=nombre_actual)
        ttk.Entry(frame, textvariable=nombre_var, width=40).pack(fill=tk.X, pady=5)
        
        ttk.Label(frame, text="Email:").pack(anchor='w', pady=5)
        email_var = tk.StringVar(value=email_actual if email_actual else "")
        ttk.Entry(frame, textvariable=email_var, width=40).pack(fill=tk.X, pady=5)
        
        ttk.Label(frame, text="Rol:").pack(anchor='w', pady=5)
        rol_var = tk.StringVar(value=rol_actual)
        combo_rol = ttk.Combobox(frame, textvariable=rol_var, values=["ADMINISTRADOR", "USUARIO"], 
                                 width=20, state="readonly")
        combo_rol.pack(anchor='w', pady=5)
        
        ttk.Label(frame, text="Estado:").pack(anchor='w', pady=5)
        activo_var = tk.BooleanVar(value=activo_actual)
        ttk.Checkbutton(frame, text="Activo", variable=activo_var).pack(anchor='w', pady=5)
        
        def guardar():
            exito, mensaje = Seguridad.actualizar_usuario(
                user_id, nombre_var.get().strip(), email_var.get().strip(), 
                rol_var.get(), activo_var.get()
            )
            if exito:
                messagebox.showinfo("Éxito", mensaje)
                edit_win.destroy()
                self.cargar_usuarios()
            else:
                messagebox.showerror("Error", mensaje)
        
        btn_guardar = tk.Button(frame, text="Guardar Cambios", command=guardar,
                               bg="#2ecc71", fg="white", cursor='hand2')
        btn_guardar.pack(pady=20)
    
    def cambiar_contrasena(self):
        """Cambia la contraseña de un usuario"""
        seleccion = self.tree_usuarios.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Seleccione un usuario para cambiar su contraseña")
            return
        
        item = self.tree_usuarios.item(seleccion[0])
        user_id = item['values'][0]
        usuario = item['values'][1]
        
        # Ventana de cambio de contraseña
        pass_win = tk.Toplevel(self.ventana)
        pass_win.title(f"Cambiar Contraseña - {usuario}")
        pass_win.geometry("400x250")
        pass_win.transient(self.ventana)
        pass_win.grab_set()
        
        # Centrar ventana
        pass_win.update_idletasks()
        x = (pass_win.winfo_screenwidth() // 2) - 200
        y = (pass_win.winfo_screenheight() // 2) - 125
        pass_win.geometry(f'400x250+{x}+{y}')
        
        frame = ttk.Frame(pass_win, padding="20")
        frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(frame, text=f"Cambiar contraseña para: {usuario}", 
                 font=('Helvetica', 12, 'bold')).pack(pady=(0, 20))
        
        ttk.Label(frame, text="Nueva Contraseña:").pack(anchor='w', pady=5)
        nueva_pass_var = tk.StringVar()
        ttk.Entry(frame, textvariable=nueva_pass_var, width=30, show="•").pack(fill=tk.X, pady=5)
        
        ttk.Label(frame, text="Confirmar Contraseña:").pack(anchor='w', pady=5)
        confirmar_pass_var = tk.StringVar()
        ttk.Entry(frame, textvariable=confirmar_pass_var, width=30, show="•").pack(fill=tk.X, pady=5)
        
        def guardar_pass():
            nueva = nueva_pass_var.get()
            confirmar = confirmar_pass_var.get()
            
            if not nueva:
                messagebox.showerror("Error", "Ingrese la nueva contraseña")
                return
            
            if len(nueva) < 6:
                messagebox.showerror("Error", "La contraseña debe tener al menos 6 caracteres")
                return
            
            if nueva != confirmar:
                messagebox.showerror("Error", "Las contraseñas no coinciden")
                return
            
            exito, mensaje = Seguridad.cambiar_contrasena(user_id, nueva)
            if exito:
                messagebox.showinfo("Éxito", mensaje)
                pass_win.destroy()
            else:
                messagebox.showerror("Error", mensaje)
        
        btn_guardar = tk.Button(frame, text="Cambiar Contraseña", command=guardar_pass,
                               bg="#3498db", fg="white", cursor='hand2')
        btn_guardar.pack(pady=20)
    
    def eliminar_usuario(self):
        """Elimina un usuario"""
        seleccion = self.tree_usuarios.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Seleccione un usuario para eliminar")
            return
        
        item = self.tree_usuarios.item(seleccion[0])
        user_id = item['values'][0]
        usuario = item['values'][1]
        usuario_actual = get_usuario_actual()
        
        if usuario == usuario_actual['usuario']:
            messagebox.showerror("Error", "No puede eliminar su propio usuario")
            return
        
        if messagebox.askyesno("Confirmar", f"¿Eliminar el usuario '{usuario}'?\nEsta acción no se puede deshacer."):
            exito, mensaje = Seguridad.eliminar_usuario(user_id)
            if exito:
                messagebox.showinfo("Éxito", mensaje)
                self.cargar_usuarios()
            else:
                messagebox.showerror("Error", mensaje)