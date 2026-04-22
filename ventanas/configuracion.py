import tkinter as tk
from tkinter import ttk, messagebox
from database.conexion import db
from database.queries import Queries

class VentanaConfiguracion:
    """Ventana para administrar tablas maestras"""
    
    def __init__(self, parent):
        self.parent = parent
        
        self.ventana = tk.Toplevel(parent)
        self.ventana.title("Configuración del Sistema")
        self.ventana.geometry("950x700")
        self.ventana.transient(parent)
        self.ventana.grab_set()
        
        self.centrar_ventana()
        self.crear_interfaz()
        self.cargar_datos_iniciales()
    
    def centrar_ventana(self):
        self.ventana.update_idletasks()
        ancho = 950
        alto = 700
        x = (self.ventana.winfo_screenwidth() // 2) - (ancho // 2)
        y = (self.ventana.winfo_screenheight() // 2) - (alto // 2)
        self.ventana.geometry(f'{ancho}x{alto}+{x}+{y}')
    
    def crear_interfaz(self):
        # Frame principal
        main_frame = ttk.Frame(self.ventana, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Título
        titulo = ttk.Label(main_frame, text="Configuración del Sistema", 
                          font=('Helvetica', 16, 'bold'))
        titulo.pack(pady=(0, 10))
        
        subtitulo = ttk.Label(main_frame, text="Administración de tablas maestras",
                             font=('Helvetica', 10), foreground='gray')
        subtitulo.pack(pady=(0, 20))
        
        # Notebook (pestañas)
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Crear cada pestaña
        self.crear_pestana_parroquias()
        self.crear_pestana_cargos()
        self.crear_pestana_nominas()
        self.crear_pestana_tipos_personal()
        self.crear_pestana_zonas_residencia()
        
        # Botón cerrar
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(fill=tk.X, pady=10)
        
        btn_cerrar = tk.Button(btn_frame, text="Cerrar", command=self.ventana.destroy,
                              bg="#e74c3c", fg="white", font=('Helvetica', 11),
                              padx=20, pady=5, cursor='hand2')
        btn_cerrar.pack(side=tk.RIGHT, padx=5)
    
    # ==================== PESTAÑA PARROQUIAS ====================
    def crear_pestana_parroquias(self):
        frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(frame, text="Parroquias")
        
        # Frame para agregar nueva
        add_frame = ttk.LabelFrame(frame, text="Agregar Nueva Parroquia", padding="10")
        add_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(add_frame, text="Nombre:").pack(side=tk.LEFT, padx=5)
        self.nueva_parroquia = tk.StringVar()
        entry_parroquia = ttk.Entry(add_frame, textvariable=self.nueva_parroquia, width=40)
        entry_parroquia.pack(side=tk.LEFT, padx=5)
        
        btn_agregar = tk.Button(add_frame, text="➕ Agregar", command=self.agregar_parroquia,
                               bg="#2ecc71", fg="white", cursor='hand2')
        btn_agregar.pack(side=tk.LEFT, padx=5)
        
        # Treeview para listar
        list_frame = ttk.LabelFrame(frame, text="Lista de Parroquias", padding="10")
        list_frame.pack(fill=tk.BOTH, expand=True)
        
        scroll_y = ttk.Scrollbar(list_frame, orient="vertical")
        scroll_x = ttk.Scrollbar(list_frame, orient="horizontal")
        
        self.tree_parroquias = ttk.Treeview(list_frame, columns=("ID", "Nombre"), 
                                           show="headings",
                                           yscrollcommand=scroll_y.set, 
                                           xscrollcommand=scroll_x.set)
        
        scroll_y.config(command=self.tree_parroquias.yview)
        scroll_x.config(command=self.tree_parroquias.xview)
        
        scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
        scroll_x.pack(side=tk.BOTTOM, fill=tk.X)
        self.tree_parroquias.pack(fill=tk.BOTH, expand=True)
        
        self.tree_parroquias.heading("ID", text="ID")
        self.tree_parroquias.heading("Nombre", text="Nombre")
        self.tree_parroquias.column("ID", width=50)
        self.tree_parroquias.column("Nombre", width=300)
        
        # Botones de acción
        btn_frame = ttk.Frame(frame)
        btn_frame.pack(fill=tk.X, pady=5)
        
        btn_eliminar = tk.Button(btn_frame, text="🗑️ Eliminar Seleccionado", 
                                command=self.eliminar_parroquia,
                                bg="#e74c3c", fg="white", cursor='hand2')
        btn_eliminar.pack(side=tk.LEFT, padx=5)
        
        btn_refresh = tk.Button(btn_frame, text="🔄 Actualizar", command=self.cargar_parroquias,
                               bg="#3498db", fg="white", cursor='hand2')
        btn_refresh.pack(side=tk.LEFT, padx=5)
    
    def cargar_parroquias(self):
        for item in self.tree_parroquias.get_children():
            self.tree_parroquias.delete(item)
        
        resultados = db.execute_query("SELECT id, nombre_parroquia FROM parroquias ORDER BY nombre_parroquia")
        if resultados:
            for row in resultados:
                self.tree_parroquias.insert("", tk.END, values=row)
    
    def agregar_parroquia(self):
        nombre = self.nueva_parroquia.get().strip().upper()
        if not nombre:
            messagebox.showerror("Error", "El nombre de la parroquia es obligatorio")
            return
        
        try:
            db.execute_query("INSERT INTO parroquias (nombre_parroquia) VALUES (%s)", (nombre,))
            messagebox.showinfo("Éxito", f"Parroquia '{nombre}' agregada correctamente")
            self.nueva_parroquia.set("")
            self.cargar_parroquias()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo agregar: {str(e)}")
    
    def eliminar_parroquia(self):
        seleccion = self.tree_parroquias.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Seleccione una parroquia para eliminar")
            return
        
        item = self.tree_parroquias.item(seleccion[0])
        parroquia_id = item['values'][0]
        parroquia_nombre = item['values'][1]
        
        if messagebox.askyesno("Confirmar", f"¿Eliminar la parroquia '{parroquia_nombre}'?\n(No se eliminarán empleados asociados)"):
            try:
                db.execute_query("DELETE FROM parroquias WHERE id = %s", (parroquia_id,))
                messagebox.showinfo("Éxito", "Parroquia eliminada correctamente")
                self.cargar_parroquias()
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo eliminar: {str(e)}")
    
    # ==================== PESTAÑA CARGOS ====================
    def crear_pestana_cargos(self):
        frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(frame, text="Cargos")
        
        # Frame para agregar nuevo
        add_frame = ttk.LabelFrame(frame, text="Agregar Nuevo Cargo", padding="10")
        add_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(add_frame, text="Nombre:").pack(side=tk.LEFT, padx=5)
        self.nuevo_cargo = tk.StringVar()
        entry_cargo = ttk.Entry(add_frame, textvariable=self.nuevo_cargo, width=40)
        entry_cargo.pack(side=tk.LEFT, padx=5)
        
        btn_agregar = tk.Button(add_frame, text="➕ Agregar", command=self.agregar_cargo,
                               bg="#2ecc71", fg="white", cursor='hand2')
        btn_agregar.pack(side=tk.LEFT, padx=5)
        
        # Treeview para listar
        list_frame = ttk.LabelFrame(frame, text="Lista de Cargos", padding="10")
        list_frame.pack(fill=tk.BOTH, expand=True)
        
        scroll_y = ttk.Scrollbar(list_frame, orient="vertical")
        scroll_x = ttk.Scrollbar(list_frame, orient="horizontal")
        
        self.tree_cargos = ttk.Treeview(list_frame, columns=("ID", "Nombre"), 
                                       show="headings",
                                       yscrollcommand=scroll_y.set, 
                                       xscrollcommand=scroll_x.set)
        
        scroll_y.config(command=self.tree_cargos.yview)
        scroll_x.config(command=self.tree_cargos.xview)
        
        scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
        scroll_x.pack(side=tk.BOTTOM, fill=tk.X)
        self.tree_cargos.pack(fill=tk.BOTH, expand=True)
        
        self.tree_cargos.heading("ID", text="ID")
        self.tree_cargos.heading("Nombre", text="Nombre")
        self.tree_cargos.column("ID", width=50)
        self.tree_cargos.column("Nombre", width=300)
        
        # Botones de acción
        btn_frame = ttk.Frame(frame)
        btn_frame.pack(fill=tk.X, pady=5)
        
        btn_eliminar = tk.Button(btn_frame, text="🗑️ Eliminar Seleccionado", 
                                command=self.eliminar_cargo,
                                bg="#e74c3c", fg="white", cursor='hand2')
        btn_eliminar.pack(side=tk.LEFT, padx=5)
        
        btn_refresh = tk.Button(btn_frame, text="🔄 Actualizar", command=self.cargar_cargos,
                               bg="#3498db", fg="white", cursor='hand2')
        btn_refresh.pack(side=tk.LEFT, padx=5)
    
    def cargar_cargos(self):
        for item in self.tree_cargos.get_children():
            self.tree_cargos.delete(item)
        
        resultados = db.execute_query("SELECT id, nombre_cargo FROM cargos ORDER BY nombre_cargo")
        if resultados:
            for row in resultados:
                self.tree_cargos.insert("", tk.END, values=row)
    
    def agregar_cargo(self):
        nombre = self.nuevo_cargo.get().strip().upper()
        if not nombre:
            messagebox.showerror("Error", "El nombre del cargo es obligatorio")
            return
        
        try:
            db.execute_query("INSERT INTO cargos (nombre_cargo) VALUES (%s)", (nombre,))
            messagebox.showinfo("Éxito", f"Cargo '{nombre}' agregado correctamente")
            self.nuevo_cargo.set("")
            self.cargar_cargos()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo agregar: {str(e)}")
    
    def eliminar_cargo(self):
        seleccion = self.tree_cargos.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Seleccione un cargo para eliminar")
            return
        
        item = self.tree_cargos.item(seleccion[0])
        cargo_id = item['values'][0]
        cargo_nombre = item['values'][1]
        
        if messagebox.askyesno("Confirmar", f"¿Eliminar el cargo '{cargo_nombre}'?\n(No se eliminarán empleados asociados)"):
            try:
                db.execute_query("DELETE FROM cargos WHERE id = %s", (cargo_id,))
                messagebox.showinfo("Éxito", "Cargo eliminado correctamente")
                self.cargar_cargos()
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo eliminar: {str(e)}")
    
    # ==================== PESTAÑA NÓMINAS ====================
    def crear_pestana_nominas(self):
        frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(frame, text="Tipos de Nómina")
        
        # Frame para agregar nuevo
        add_frame = ttk.LabelFrame(frame, text="Agregar Nuevo Tipo de Nómina", padding="10")
        add_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(add_frame, text="Nombre:").pack(side=tk.LEFT, padx=5)
        self.nueva_nomina = tk.StringVar()
        entry_nomina = ttk.Entry(add_frame, textvariable=self.nueva_nomina, width=40)
        entry_nomina.pack(side=tk.LEFT, padx=5)
        
        btn_agregar = tk.Button(add_frame, text="➕ Agregar", command=self.agregar_nomina,
                               bg="#2ecc71", fg="white", cursor='hand2')
        btn_agregar.pack(side=tk.LEFT, padx=5)
        
        # Treeview para listar
        list_frame = ttk.LabelFrame(frame, text="Lista de Tipos de Nómina", padding="10")
        list_frame.pack(fill=tk.BOTH, expand=True)
        
        scroll_y = ttk.Scrollbar(list_frame, orient="vertical")
        scroll_x = ttk.Scrollbar(list_frame, orient="horizontal")
        
        self.tree_nominas = ttk.Treeview(list_frame, columns=("ID", "Nombre"), 
                                        show="headings",
                                        yscrollcommand=scroll_y.set, 
                                        xscrollcommand=scroll_x.set)
        
        scroll_y.config(command=self.tree_nominas.yview)
        scroll_x.config(command=self.tree_nominas.xview)
        
        scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
        scroll_x.pack(side=tk.BOTTOM, fill=tk.X)
        self.tree_nominas.pack(fill=tk.BOTH, expand=True)
        
        self.tree_nominas.heading("ID", text="ID")
        self.tree_nominas.heading("Nombre", text="Nombre")
        self.tree_nominas.column("ID", width=50)
        self.tree_nominas.column("Nombre", width=300)
        
        # Botones de acción
        btn_frame = ttk.Frame(frame)
        btn_frame.pack(fill=tk.X, pady=5)
        
        btn_eliminar = tk.Button(btn_frame, text="🗑️ Eliminar Seleccionado", 
                                command=self.eliminar_nomina,
                                bg="#e74c3c", fg="white", cursor='hand2')
        btn_eliminar.pack(side=tk.LEFT, padx=5)
        
        btn_refresh = tk.Button(btn_frame, text="🔄 Actualizar", command=self.cargar_nominas,
                               bg="#3498db", fg="white", cursor='hand2')
        btn_refresh.pack(side=tk.LEFT, padx=5)
    
    def cargar_nominas(self):
        for item in self.tree_nominas.get_children():
            self.tree_nominas.delete(item)
        
        resultados = db.execute_query("SELECT id, nombre_nomina FROM tipos_nomina ORDER BY nombre_nomina")
        if resultados:
            for row in resultados:
                self.tree_nominas.insert("", tk.END, values=row)
    
    def agregar_nomina(self):
        nombre = self.nueva_nomina.get().strip().upper()
        if not nombre:
            messagebox.showerror("Error", "El nombre de la nómina es obligatorio")
            return
        
        try:
            db.execute_query("INSERT INTO tipos_nomina (nombre_nomina) VALUES (%s)", (nombre,))
            messagebox.showinfo("Éxito", f"Nómina '{nombre}' agregada correctamente")
            self.nueva_nomina.set("")
            self.cargar_nominas()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo agregar: {str(e)}")
    
    def eliminar_nomina(self):
        seleccion = self.tree_nominas.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Seleccione una nómina para eliminar")
            return
        
        item = self.tree_nominas.item(seleccion[0])
        nomina_id = item['values'][0]
        nomina_nombre = item['values'][1]
        
        if messagebox.askyesno("Confirmar", f"¿Eliminar la nómina '{nomina_nombre}'?\n(No se eliminarán empleados asociados)"):
            try:
                db.execute_query("DELETE FROM tipos_nomina WHERE id = %s", (nomina_id,))
                messagebox.showinfo("Éxito", "Nómina eliminada correctamente")
                self.cargar_nominas()
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo eliminar: {str(e)}")
    
    # ==================== PESTAÑA TIPOS DE PERSONAL ====================
    def crear_pestana_tipos_personal(self):
        frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(frame, text="Tipos de Personal")
        
        # Frame para agregar nuevo
        add_frame = ttk.LabelFrame(frame, text="Agregar Nuevo Tipo de Personal", padding="10")
        add_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(add_frame, text="Nombre:").pack(side=tk.LEFT, padx=5)
        self.nuevo_tipo_personal = tk.StringVar()
        entry_tipo = ttk.Entry(add_frame, textvariable=self.nuevo_tipo_personal, width=40)
        entry_tipo.pack(side=tk.LEFT, padx=5)
        
        btn_agregar = tk.Button(add_frame, text="➕ Agregar", command=self.agregar_tipo_personal,
                               bg="#2ecc71", fg="white", cursor='hand2')
        btn_agregar.pack(side=tk.LEFT, padx=5)
        
        # Treeview para listar
        list_frame = ttk.LabelFrame(frame, text="Lista de Tipos de Personal", padding="10")
        list_frame.pack(fill=tk.BOTH, expand=True)
        
        scroll_y = ttk.Scrollbar(list_frame, orient="vertical")
        scroll_x = ttk.Scrollbar(list_frame, orient="horizontal")
        
        self.tree_tipos = ttk.Treeview(list_frame, columns=("ID", "Nombre"), 
                                      show="headings",
                                      yscrollcommand=scroll_y.set, 
                                      xscrollcommand=scroll_x.set)
        
        scroll_y.config(command=self.tree_tipos.yview)
        scroll_x.config(command=self.tree_tipos.xview)
        
        scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
        scroll_x.pack(side=tk.BOTTOM, fill=tk.X)
        self.tree_tipos.pack(fill=tk.BOTH, expand=True)
        
        self.tree_tipos.heading("ID", text="ID")
        self.tree_tipos.heading("Nombre", text="Nombre")
        self.tree_tipos.column("ID", width=50)
        self.tree_tipos.column("Nombre", width=300)
        
        # Botones de acción
        btn_frame = ttk.Frame(frame)
        btn_frame.pack(fill=tk.X, pady=5)
        
        btn_eliminar = tk.Button(btn_frame, text="🗑️ Eliminar Seleccionado", 
                                command=self.eliminar_tipo_personal,
                                bg="#e74c3c", fg="white", cursor='hand2')
        btn_eliminar.pack(side=tk.LEFT, padx=5)
        
        btn_refresh = tk.Button(btn_frame, text="🔄 Actualizar", command=self.cargar_tipos_personal,
                               bg="#3498db", fg="white", cursor='hand2')
        btn_refresh.pack(side=tk.LEFT, padx=5)
    
    def cargar_tipos_personal(self):
        for item in self.tree_tipos.get_children():
            self.tree_tipos.delete(item)
        
        resultados = db.execute_query("SELECT id, nombre_tipo FROM tipos_personal ORDER BY nombre_tipo")
        if resultados:
            for row in resultados:
                self.tree_tipos.insert("", tk.END, values=row)
    
    def agregar_tipo_personal(self):
        nombre = self.nuevo_tipo_personal.get().strip().upper()
        if not nombre:
            messagebox.showerror("Error", "El nombre del tipo de personal es obligatorio")
            return
        
        if nombre not in ['DIRECTIVO', 'ADMINISTRATIVO', 'OPERATIVO']:
            messagebox.showerror("Error", "Los tipos permitidos son: DIRECTIVO, ADMINISTRATIVO, OPERATIVO")
            return
        
        try:
            db.execute_query("INSERT INTO tipos_personal (nombre_tipo) VALUES (%s)", (nombre,))
            messagebox.showinfo("Éxito", f"Tipo '{nombre}' agregado correctamente")
            self.nuevo_tipo_personal.set("")
            self.cargar_tipos_personal()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo agregar: {str(e)}")
    
    def eliminar_tipo_personal(self):
        seleccion = self.tree_tipos.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Seleccione un tipo para eliminar")
            return
        
        item = self.tree_tipos.item(seleccion[0])
        tipo_id = item['values'][0]
        tipo_nombre = item['values'][1]
        
        if messagebox.askyesno("Confirmar", f"¿Eliminar el tipo '{tipo_nombre}'?\n(No se eliminarán empleados asociados)"):
            try:
                db.execute_query("DELETE FROM tipos_personal WHERE id = %s", (tipo_id,))
                messagebox.showinfo("Éxito", "Tipo eliminado correctamente")
                self.cargar_tipos_personal()
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo eliminar: {str(e)}")
    
    # ==================== PESTAÑA ZONAS DE RESIDENCIA ====================
    def crear_pestana_zonas_residencia(self):
        frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(frame, text="Zonas de Residencia")
        
        # Frame para agregar nueva
        add_frame = ttk.LabelFrame(frame, text="Agregar Nueva Zona de Residencia", padding="10")
        add_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(add_frame, text="Nombre:").pack(side=tk.LEFT, padx=5)
        self.nueva_zona = tk.StringVar()
        entry_zona = ttk.Entry(add_frame, textvariable=self.nueva_zona, width=40)
        entry_zona.pack(side=tk.LEFT, padx=5)
        
        btn_agregar = tk.Button(add_frame, text="➕ Agregar", command=self.agregar_zona,
                               bg="#2ecc71", fg="white", cursor='hand2')
        btn_agregar.pack(side=tk.LEFT, padx=5)
        
        # Treeview para listar
        list_frame = ttk.LabelFrame(frame, text="Lista de Zonas de Residencia", padding="10")
        list_frame.pack(fill=tk.BOTH, expand=True)
        
        scroll_y = ttk.Scrollbar(list_frame, orient="vertical")
        scroll_x = ttk.Scrollbar(list_frame, orient="horizontal")
        
        self.tree_zonas = ttk.Treeview(list_frame, columns=("ID", "Nombre"), 
                                      show="headings",
                                      yscrollcommand=scroll_y.set, 
                                      xscrollcommand=scroll_x.set)
        
        scroll_y.config(command=self.tree_zonas.yview)
        scroll_x.config(command=self.tree_zonas.xview)
        
        scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
        scroll_x.pack(side=tk.BOTTOM, fill=tk.X)
        self.tree_zonas.pack(fill=tk.BOTH, expand=True)
        
        self.tree_zonas.heading("ID", text="ID")
        self.tree_zonas.heading("Nombre", text="Nombre")
        self.tree_zonas.column("ID", width=50)
        self.tree_zonas.column("Nombre", width=300)
        
        # Botones de acción
        btn_frame = ttk.Frame(frame)
        btn_frame.pack(fill=tk.X, pady=5)
        
        btn_eliminar = tk.Button(btn_frame, text="🗑️ Eliminar Seleccionado", 
                                command=self.eliminar_zona,
                                bg="#e74c3c", fg="white", cursor='hand2')
        btn_eliminar.pack(side=tk.LEFT, padx=5)
        
        btn_refresh = tk.Button(btn_frame, text="🔄 Actualizar", command=self.cargar_zonas,
                               bg="#3498db", fg="white", cursor='hand2')
        btn_refresh.pack(side=tk.LEFT, padx=5)
    
    def cargar_zonas(self):
        """Carga las zonas de residencia"""
        for item in self.tree_zonas.get_children():
            self.tree_zonas.delete(item)
        
        resultados = db.execute_query("SELECT id, nombre_zona FROM zonas_residencia ORDER BY nombre_zona")
        if resultados:
            for row in resultados:
                self.tree_zonas.insert("", tk.END, values=row)
    
    def agregar_zona(self):
        """Agrega una nueva zona de residencia"""
        nombre = self.nueva_zona.get().strip().upper()
        if not nombre:
            messagebox.showerror("Error", "El nombre de la zona es obligatorio")
            return
        
        try:
            db.execute_query("INSERT INTO zonas_residencia (nombre_zona) VALUES (%s)", (nombre,))
            messagebox.showinfo("Éxito", f"Zona '{nombre}' agregada correctamente")
            self.nueva_zona.set("")
            self.cargar_zonas()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo agregar: {str(e)}")
    
    def eliminar_zona(self):
        """Elimina una zona de residencia"""
        seleccion = self.tree_zonas.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Seleccione una zona para eliminar")
            return
        
        item = self.tree_zonas.item(seleccion[0])
        zona_id = item['values'][0]
        zona_nombre = item['values'][1]
        
        if messagebox.askyesno("Confirmar", f"¿Eliminar la zona '{zona_nombre}'?\n(No se eliminarán empleados asociados)"):
            try:
                db.execute_query("DELETE FROM zonas_residencia WHERE id = %s", (zona_id,))
                messagebox.showinfo("Éxito", "Zona eliminada correctamente")
                self.cargar_zonas()
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo eliminar: {str(e)}")
    
    
    # ==================== PESTAÑA BANCOS ====================
    def crear_pestana_bancos(self):
        frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(frame, text="Bancos")
        
        # Frame para agregar nuevo
        add_frame = ttk.LabelFrame(frame, text="Agregar Nuevo Banco", padding="10")
        add_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Código del banco
        ttk.Label(add_frame, text="Código:").grid(row=0, column=0, sticky='w', padx=5, pady=5)
        self.nuevo_codigo_banco = tk.StringVar()
        entry_codigo = ttk.Entry(add_frame, textvariable=self.nuevo_codigo_banco, width=10)
        entry_codigo.grid(row=0, column=1, padx=5, pady=5)
        
        # Nombre del banco
        ttk.Label(add_frame, text="Nombre:").grid(row=0, column=2, sticky='w', padx=5, pady=5)
        self.nuevo_nombre_banco = tk.StringVar()
        entry_nombre = ttk.Entry(add_frame, textvariable=self.nuevo_nombre_banco, width=30)
        entry_nombre.grid(row=0, column=3, padx=5, pady=5)
        
        btn_agregar = tk.Button(add_frame, text="➕ Agregar", command=self.agregar_banco,
                            bg="#2ecc71", fg="white", cursor='hand2')
        btn_agregar.grid(row=0, column=4, padx=10, pady=5)
        
        # Treeview para listar
        list_frame = ttk.LabelFrame(frame, text="Lista de Bancos", padding="10")
        list_frame.pack(fill=tk.BOTH, expand=True)
        
        scroll_y = ttk.Scrollbar(list_frame, orient="vertical")
        scroll_x = ttk.Scrollbar(list_frame, orient="horizontal")
        
        self.tree_bancos = ttk.Treeview(list_frame, columns=("ID", "Código", "Nombre", "Activo"), 
                                    show="headings",
                                    yscrollcommand=scroll_y.set, 
                                    xscrollcommand=scroll_x.set)
        
        scroll_y.config(command=self.tree_bancos.yview)
        scroll_x.config(command=self.tree_bancos.xview)
        
        scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
        scroll_x.pack(side=tk.BOTTOM, fill=tk.X)
        self.tree_bancos.pack(fill=tk.BOTH, expand=True)
        
        self.tree_bancos.heading("ID", text="ID")
        self.tree_bancos.heading("Código", text="Código")
        self.tree_bancos.heading("Nombre", text="Nombre")
        self.tree_bancos.heading("Activo", text="Activo")
        
        self.tree_bancos.column("ID", width=50)
        self.tree_bancos.column("Código", width=80)
        self.tree_bancos.column("Nombre", width=300)
        self.tree_bancos.column("Activo", width=60)
        
        # Botones de acción
        btn_frame = ttk.Frame(frame)
        btn_frame.pack(fill=tk.X, pady=5)
        
        btn_eliminar = tk.Button(btn_frame, text="🗑️ Eliminar Seleccionado", 
                                command=self.eliminar_banco,
                                bg="#e74c3c", fg="white", cursor='hand2')
        btn_eliminar.pack(side=tk.LEFT, padx=5)
        
        btn_toggle = tk.Button(btn_frame, text="🔄 Activar/Desactivar", 
                            command=self.toggle_banco,
                            bg="#f39c12", fg="white", cursor='hand2')
        btn_toggle.pack(side=tk.LEFT, padx=5)
        
        btn_refresh = tk.Button(btn_frame, text="🔄 Actualizar", command=self.cargar_bancos,
                            bg="#3498db", fg="white", cursor='hand2')
        btn_refresh.pack(side=tk.LEFT, padx=5)
        
        self.cargar_bancos()

    def cargar_bancos(self):
        """Carga la lista de bancos"""
        for item in self.tree_bancos.get_children():
            self.tree_bancos.delete(item)
        
        resultados = db.execute_query("SELECT id, codigo_banco, nombre_banco, activo FROM bancos ORDER BY nombre_banco")
        if resultados:
            for row in resultados:
                activo = "✅" if row[3] else "❌"
                self.tree_bancos.insert("", tk.END, values=(row[0], row[1], row[2], activo))

    def agregar_banco(self):
        """Agrega un nuevo banco"""
        codigo = self.nuevo_codigo_banco.get().strip()
        nombre = self.nuevo_nombre_banco.get().strip().upper()
        
        if not codigo:
            messagebox.showerror("Error", "El código del banco es obligatorio")
            return
        
        if not nombre:
            messagebox.showerror("Error", "El nombre del banco es obligatorio")
            return
        
        try:
            db.execute_query(
                "INSERT INTO bancos (codigo_banco, nombre_banco, activo) VALUES (%s, %s, %s)",
                (codigo, nombre, True)
            )
            messagebox.showinfo("Éxito", f"Banco '{nombre}' agregado correctamente")
            self.nuevo_codigo_banco.set("")
            self.nuevo_nombre_banco.set("")
            self.cargar_bancos()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo agregar: {str(e)}")

    def eliminar_banco(self):
        """Elimina un banco"""
        seleccion = self.tree_bancos.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Seleccione un banco para eliminar")
            return
        
        item = self.tree_bancos.item(seleccion[0])
        banco_id = item['values'][0]
        banco_nombre = item['values'][2]
        
        if messagebox.askyesno("Confirmar", f"¿Eliminar el banco '{banco_nombre}'?\n(No se eliminarán empleados asociados)"):
            try:
                db.execute_query("DELETE FROM bancos WHERE id = %s", (banco_id,))
                messagebox.showinfo("Éxito", "Banco eliminado correctamente")
                self.cargar_bancos()
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo eliminar: {str(e)}")

    def toggle_banco(self):
        """Activa o desactiva un banco"""
        seleccion = self.tree_bancos.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Seleccione un banco para activar/desactivar")
            return
        
        item = self.tree_bancos.item(seleccion[0])
        banco_id = item['values'][0]
        banco_nombre = item['values'][2]
        activo_actual = item['values'][3] == "✅"
        
        nuevo_estado = not activo_actual
        estado_texto = "activar" if nuevo_estado else "desactivar"
        
        if messagebox.askyesno("Confirmar", f"¿{estado_texto.upper()} el banco '{banco_nombre}'?"):
            try:
                db.execute_query("UPDATE bancos SET activo = %s WHERE id = %s", (nuevo_estado, banco_id))
                messagebox.showinfo("Éxito", f"Banco {estado_texto}do correctamente")
                self.cargar_bancos()
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo cambiar el estado: {str(e)}")
    
    # ==================== CARGA INICIAL ====================
    def cargar_datos_iniciales(self):
        """Carga todos los datos al abrir la ventana"""
        self.cargar_parroquias()
        self.cargar_cargos()
        self.cargar_nominas()
        self.cargar_tipos_personal()
        self.cargar_zonas()
        self.crear_pestana_bancos()