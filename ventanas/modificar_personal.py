import tkinter as tk
from tkinter import ttk, messagebox
from database.conexion import db
from database.queries import Queries
from utils.validaciones import Validaciones

class VentanaModificar:
    """Ventana para modificar personal existente"""
    
    def __init__(self, parent, callback_actualizar):
        self.parent = parent
        self.callback_actualizar = callback_actualizar
        self.empleado_seleccionado = None
        self.empleado_id = None
        
        # Primero mostrar ventana de selección
        self.ventana_seleccion = tk.Toplevel(parent)
        self.ventana_seleccion.title("Seleccionar Empleado a Modificar")
        self.ventana_seleccion.geometry("1000x600")
        self.ventana_seleccion.transient(parent)
        self.ventana_seleccion.grab_set()
        
        self.centrar_ventana(self.ventana_seleccion, 1000, 600)
        self.crear_seleccion()
    
    def centrar_ventana(self, ventana, ancho, alto):
        ventana.update_idletasks()
        x = (ventana.winfo_screenwidth() // 2) - (ancho // 2)
        y = (ventana.winfo_screenheight() // 2) - (alto // 2)
        ventana.geometry(f'{ancho}x{alto}+{x}+{y}')
    
    def crear_seleccion(self):
        """Crea la interfaz para seleccionar empleado"""
        
        main_frame = ttk.Frame(self.ventana_seleccion, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Título
        titulo = ttk.Label(main_frame, text="Seleccionar Empleado para Modificar",
                          font=('Helvetica', 14, 'bold'))
        titulo.pack(pady=(0, 10))
        
        # Frame de búsqueda
        search_frame = ttk.Frame(main_frame)
        search_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(search_frame, text="Buscar por cédula:").pack(side=tk.LEFT, padx=5)
        
        self.buscar_cedula = tk.StringVar()
        entry_buscar = ttk.Entry(search_frame, textvariable=self.buscar_cedula, width=20)
        entry_buscar.pack(side=tk.LEFT, padx=5)
        entry_buscar.bind('<Return>', lambda e: self.buscar_empleado())
        
        btn_buscar = tk.Button(search_frame, text="🔍 Buscar", command=self.buscar_empleado,
                              bg="#3498db", fg="white", cursor='hand2')
        btn_buscar.pack(side=tk.LEFT, padx=5)
        
        btn_limpiar = tk.Button(search_frame, text="🗑️ Limpiar", command=self.cargar_todos,
                               bg="#95a5a6", fg="white", cursor='hand2')
        btn_limpiar.pack(side=tk.LEFT, padx=5)
        
        # Treeview para resultados
        tree_frame = ttk.LabelFrame(main_frame, text="Empleados", padding="10")
        tree_frame.pack(fill=tk.BOTH, expand=True)
        
        scroll_y = ttk.Scrollbar(tree_frame, orient="vertical")
        scroll_x = ttk.Scrollbar(tree_frame, orient="horizontal")
        
        columnas = ("ID", "Cédula", "Nombre", "Cargo", "Teléfono", "Email", "Estatus")
        
        self.tree = ttk.Treeview(tree_frame, columns=columnas, show="headings",
                                 yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)
        
        scroll_y.config(command=self.tree.yview)
        scroll_x.config(command=self.tree.xview)
        
        scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
        scroll_x.pack(side=tk.BOTTOM, fill=tk.X)
        self.tree.pack(fill=tk.BOTH, expand=True)
        
        # Configurar columnas
        anchos = [50, 100, 250, 150, 100, 150, 80]
        for col, ancho in zip(columnas, anchos):
            self.tree.heading(col, text=col)
            self.tree.column(col, width=ancho)
        
        # Configurar colores para inactivos
        self.tree.tag_configure('inactivo', background='#ffe6e6')
        
        # Doble click para seleccionar
        self.tree.bind("<Double-1>", self.seleccionar_empleado)
        
        # Botón seleccionar
        btn_seleccionar = tk.Button(main_frame, text="✏️ Seleccionar para Modificar", 
                                   command=self.seleccionar_empleado,
                                   bg="#f39c12", fg="white", font=('Helvetica', 11),
                                   padx=20, pady=5, cursor='hand2')
        btn_seleccionar.pack(pady=10)
        
        btn_cancelar = tk.Button(main_frame, text="❌ Cancelar", command=self.ventana_seleccion.destroy,
                                bg="#e74c3c", fg="white", cursor='hand2')
        btn_cancelar.pack()
        
        # Cargar todos los empleados
        self.cargar_todos()
    
    def cargar_todos(self):
        """Carga todos los empleados (activos e inactivos)"""
        self.buscar_cedula.set("")
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        resultados = Queries.buscar_empleado(solo_activos=False)
        if resultados:
            for row in resultados:
                estatus = row[3]
                valores = (row[0], row[1], row[2], row[4], row[9], row[10], estatus)
                if estatus == 'INACTIVO':
                    self.tree.insert("", tk.END, values=valores, tags=('inactivo',))
                else:
                    self.tree.insert("", tk.END, values=valores)
    
    def buscar_empleado(self):
        """Busca empleado por cédula (incluye inactivos)"""
        cedula = self.buscar_cedula.get().strip()
        if not cedula:
            self.cargar_todos()
            return
        
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        resultados = Queries.buscar_empleado(cedula=cedula, solo_activos=False)
        if resultados:
            for row in resultados:
                estatus = row[3]
                valores = (row[0], row[1], row[2], row[4], row[9], row[10], estatus)
                if estatus == 'INACTIVO':
                    self.tree.insert("", tk.END, values=valores, tags=('inactivo',))
                else:
                    self.tree.insert("", tk.END, values=valores)
        else:
            messagebox.showinfo("Información", "No se encontró empleado con esa cédula")
    
    def seleccionar_empleado(self, event=None):
        """Selecciona el empleado y abre el formulario de modificación"""
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Seleccione un empleado")
            return
        
        item = self.tree.item(seleccion[0])
        self.empleado_id = item['values'][0]
        
        # Obtener datos completos del empleado
        self.empleado_seleccionado = Queries.obtener_empleado_por_id(self.empleado_id)
        
        # Depuración
        print(f"DEBUG: Número de campos: {len(self.empleado_seleccionado) if self.empleado_seleccionado else 0}")
        
        if self.empleado_seleccionado:
            self.ventana_seleccion.destroy()
            self.crear_formulario_modificacion()
    
    def crear_formulario_modificacion(self):
        """Crea el formulario para modificar empleado"""
        
        self.ventana = tk.Toplevel(self.parent)
        self.ventana.title(f"Modificar Personal - {self.empleado_seleccionado[3]}")
        self.ventana.geometry("750x800")
        self.ventana.transient(self.parent)
        self.ventana.grab_set()
        
        self.centrar_ventana(self.ventana, 750, 800)
        
        # Cargar datos maestros
        self.tipos_personal = Queries.get_tipos_personal() or []
        self.cargos = Queries.get_cargos() or []
        self.tipos_nomina = Queries.get_tipos_nomina() or []
        self.zonas_residencia = Queries.get_zonas_residencia() or []
        self.parroquias = Queries.get_parroquias() or []
        self.bancos = Queries.get_bancos() or []
        
        self.crear_formulario_completo()
    
    def crear_formulario_completo(self):
        """Crea el formulario completo con los datos actuales del empleado"""
        
        # Frame principal con scroll
        main_frame = ttk.Frame(self.ventana, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Canvas para scroll
        canvas = tk.Canvas(main_frame)
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Título con ID y Cédula
        titulo_frame = ttk.Frame(scrollable_frame)
        titulo_frame.pack(fill=tk.X, pady=(0, 20))
        
        ttk.Label(titulo_frame, text=f"Modificando empleado ID: {self.empleado_seleccionado[0]}",
                 font=('Helvetica', 12, 'bold')).pack(side=tk.LEFT, padx=5)
        
        ttk.Label(titulo_frame, text=f"Cédula: {self.empleado_seleccionado[4]} (No modificable)",
                 font=('Helvetica', 10), foreground='red').pack(side=tk.RIGHT, padx=5)
        
        # Crear frame para dos columnas
        columns_frame = ttk.Frame(scrollable_frame)
        columns_frame.pack(fill=tk.BOTH, expand=True)
        
        col1 = ttk.Frame(columns_frame)
        col1.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        col2 = ttk.Frame(columns_frame)
        col2.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(10, 0))
        
        # Diccionario para almacenar los campos
        self.campos = {}
        
        # Obtener la longitud real del tuple para manejar índices dinámicamente
        num_campos = len(self.empleado_seleccionado)
        print(f"DEBUG: Número de campos en empleado_seleccionado: {num_campos}")
        
        # === COLUMNA 1 ===
        # Datos personales
        frame_personal = ttk.LabelFrame(col1, text="Datos Personales", padding="10")
        frame_personal.pack(fill=tk.X, pady=(0, 10))
        
        self.crear_campo_modificacion(frame_personal, "Nombres y Apellidos:", "nombres", 0, 
                                     self.empleado_seleccionado[3])
        self.crear_campo_modificacion(frame_personal, "Nacionalidad:", "nacionalidad", 1, 
                                     self.empleado_seleccionado[5], valores=["V", "E"], tipo="combobox")
        self.crear_campo_modificacion(frame_personal, "Fecha de Nacimiento:", "fecha_nac", 2, 
                                     self.empleado_seleccionado[8], placeholder="YYYY-MM-DD")
        self.crear_campo_modificacion(frame_personal, "Sexo:", "sexo", 3,
                                     self.empleado_seleccionado[10] if num_campos > 10 else None, 
                                     valores=["M", "F"], tipo="combobox")
        self.crear_campo_modificacion(frame_personal, "Estado Civil:", "estado_civil", 4,
                                     self.empleado_seleccionado[11] if num_campos > 11 else None, 
                                     valores=["SOLTERO", "CASADO", "DIVORCIADO", "VIUDO", "CONCUBINO"], 
                                     tipo="combobox")
        self.crear_campo_modificacion(frame_personal, "Tipo de Sangre:", "tipo_sangre", 5,
                                     self.empleado_seleccionado[12] if num_campos > 12 else None,
                                     valores=["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"], 
                                     tipo="combobox")
        
        # Hijos
        frame_hijos = ttk.LabelFrame(col1, text="Hijos", padding="10")
        frame_hijos.pack(fill=tk.X, pady=(0, 10))
        
        self.crear_campo_modificacion(frame_hijos, "Cantidad de Hijos:", "cant_hijos", 0, 
                                     self.empleado_seleccionado[13] if num_campos > 13 else 0, 
                                     tipo="spinbox", from_=0, to=20)
        self.crear_campo_modificacion(frame_hijos, "Hijos 0-5 años:", "hijos_0_5", 1, 
                                     self.empleado_seleccionado[14] if num_campos > 14 else 0, 
                                     tipo="spinbox", from_=0, to=10)
        self.crear_campo_modificacion(frame_hijos, "Hijos 6-12 años:", "hijos_6_12", 2, 
                                     self.empleado_seleccionado[15] if num_campos > 15 else 0, 
                                     tipo="spinbox", from_=0, to=10)
        self.crear_campo_modificacion(frame_hijos, "Hijos 13-18 años:", "hijos_13_18", 3, 
                                     self.empleado_seleccionado[16] if num_campos > 16 else 0, 
                                     tipo="spinbox", from_=0, to=10)
        
        # === COLUMNA 2 ===
        # Datos laborales
        frame_laboral = ttk.LabelFrame(col2, text="Datos Laborales", padding="10")
        frame_laboral.pack(fill=tk.X, pady=(0, 10))
        
        # Obtener nombres actuales para los combobox (con manejo seguro)
        cargo_actual = ""
        tipo_personal_actual = ""
        tipo_nomina_actual = ""
        zona_actual = ""
        parroquia_actual = ""
        banco_actual = ""
        
        if num_campos > 27:
            cargo_actual = next((c[1] for c in self.cargos if c[0] == self.empleado_seleccionado[27]), "")
        if num_campos > 30:
            tipo_personal_actual = next((tp[1] for tp in self.tipos_personal if tp[0] == self.empleado_seleccionado[30]), "")
        if num_campos > 7:
            tipo_nomina_actual = next((tn[1] for tn in self.tipos_nomina if tn[0] == self.empleado_seleccionado[7]), "")
        if num_campos > 18:
            zona_actual = next((z[1] for z in self.zonas_residencia if z[0] == self.empleado_seleccionado[18]), "")
        if num_campos > 31:
            parroquia_actual = next((p[1] for p in self.parroquias if p[0] == self.empleado_seleccionado[31]), "")
        if num_campos > 33:
            banco_actual = next((b[2] for b in self.bancos if b[0] == self.empleado_seleccionado[33]), "")
        
        self.crear_campo_modificacion(frame_laboral, "Estatus:", "estatus", 0,
                                     self.empleado_seleccionado[1] if num_campos > 1 else "ACTIVO", 
                                     valores=["ACTIVO", "INACTIVO"], tipo="combobox")
        self.crear_campo_modificacion(frame_laboral, "Tipo de Personal:", "tipo_personal", 1,
                                     tipo_personal_actual, 
                                     valores=[f"{tp[1]}" for tp in self.tipos_personal], tipo="combobox")
        self.crear_campo_modificacion(frame_laboral, "Cargo:", "cargo", 2,
                                     cargo_actual,
                                     valores=[f"{c[1]}" for c in self.cargos], tipo="combobox")
        self.crear_campo_modificacion(frame_laboral, "Tipo de Nómina:", "tipo_nomina", 3,
                                     tipo_nomina_actual,
                                     valores=[f"{tn[1]}" for tn in self.tipos_nomina], tipo="combobox")
        self.crear_campo_modificacion(frame_laboral, "Área:", "area", 4,
                                     self.empleado_seleccionado[28] if num_campos > 28 else None)
        self.crear_campo_modificacion(frame_laboral, "Grupo:", "grupo", 5,
                                     self.empleado_seleccionado[29] if num_campos > 29 else None)
        self.crear_campo_modificacion(frame_laboral, "Nivel Académico:", "nivel_academico", 6,
                                     self.empleado_seleccionado[17] if num_campos > 17 else None,
                                     valores=["PRIMARIA", "BACHILLER", "TECNICO MEDIO", "TSU", 
                                             "UNIVERSITARIA", "POSTGRADO"], tipo="combobox")
        self.crear_campo_modificacion(frame_laboral, "Fecha de Ingreso:", "fecha_ingreso", 7,
                                     self.empleado_seleccionado[2] if num_campos > 2 else None, 
                                     placeholder="YYYY-MM-DD")
        
        # Ubicación
        frame_ubicacion = ttk.LabelFrame(col2, text="Ubicación", padding="10")
        frame_ubicacion.pack(fill=tk.X, pady=(0, 10))
        
        self.crear_campo_modificacion(frame_ubicacion, "Zona de Residencia:", "zona_residencia", 0,
                                     zona_actual,
                                     valores=[f"{z[1]}" for z in self.zonas_residencia], tipo="combobox")
        self.crear_campo_modificacion(frame_ubicacion, "Parroquia:", "parroquia", 1,
                                     parroquia_actual,
                                     valores=[f"{p[1]}" for p in self.parroquias], tipo="combobox")
        self.crear_campo_modificacion(frame_ubicacion, "Sector:", "sector", 2,
                                     self.empleado_seleccionado[19] if num_campos > 19 else None)
        
        # Contacto
        frame_contacto = ttk.LabelFrame(col2, text="Contacto y Datos Bancarios", padding="10")
        frame_contacto.pack(fill=tk.X, pady=(0, 10))
        
        self.crear_campo_modificacion(frame_contacto, "Teléfono:", "telefono", 0,
                                     self.empleado_seleccionado[20] if num_campos > 20 else None)
        self.crear_campo_modificacion(frame_contacto, "Correo Electrónico:", "email", 1,
                                     self.empleado_seleccionado[21] if num_campos > 21 else None)
        self.crear_campo_modificacion(frame_contacto, "Número de Cuenta:", "num_cuenta", 2,
                                     self.empleado_seleccionado[6] if num_campos > 6 else None)
        self.crear_campo_modificacion(frame_contacto, "Banco:", "banco", 3,
                                     banco_actual,
                                     valores=[f"{b[2]}" for b in self.bancos], tipo="combobox")
        
        # Tallas
        frame_tallas = ttk.LabelFrame(col2, text="Tallas", padding="10")
        frame_tallas.pack(fill=tk.X, pady=(0, 10))
        
        valores_tallas = ["XS", "S", "M", "L", "XL", "XXL", "XXXL"]
        
        self.crear_campo_modificacion(frame_tallas, "Talla de Calzado:", "talla_calzado", 0,
                                     self.empleado_seleccionado[24] if num_campos > 24 else None)
        self.crear_campo_modificacion(frame_tallas, "Talla de Pantalón:", "talla_pantalon", 1,
                                     self.empleado_seleccionado[25] if num_campos > 25 else None,
                                     valores=valores_tallas, tipo="combobox")
        self.crear_campo_modificacion(frame_tallas, "Talla de Camisa:", "talla_camisa", 2,
                                     self.empleado_seleccionado[26] if num_campos > 26 else None,
                                     valores=valores_tallas, tipo="combobox")
        
        # Otros
        frame_otros = ttk.LabelFrame(col2, text="Otros", padding="10")
        frame_otros.pack(fill=tk.X, pady=(0, 10))
        
        self.crear_campo_modificacion(frame_otros, "Condición Médica:", "condicion", 0,
                                     self.empleado_seleccionado[22] if num_campos > 22 else None)
        
        # Checkbox para lentes
        self.campos['usa_lentes'] = tk.BooleanVar(value=self.empleado_seleccionado[23] if num_campos > 23 else False)
        chk_lentes = ttk.Checkbutton(frame_otros, text="Usa Lentes", 
                                     variable=self.campos['usa_lentes'])
        chk_lentes.grid(row=1, column=0, columnspan=2, sticky='w', pady=5)
        
        # Botones
        frame_botones = ttk.Frame(scrollable_frame)
        frame_botones.pack(pady=20)
        
        btn_guardar = tk.Button(frame_botones, text="💾 Guardar Cambios", command=self.guardar_cambios,
                               bg="#2ecc71", fg="white", font=('Helvetica', 11),
                               padx=20, pady=5, cursor='hand2')
        btn_guardar.pack(side=tk.LEFT, padx=5)
        
        btn_cancelar = tk.Button(frame_botones, text="❌ Cancelar", command=self.ventana.destroy,
                                bg="#95a5a6", fg="white", cursor='hand2')
        btn_cancelar.pack(side=tk.LEFT, padx=5)
    
    def crear_campo_modificacion(self, parent, label, nombre, fila, valor_actual, 
                                 tipo="entry", valores=None, from_=None, to=None, placeholder=""):
        """Crea un campo de formulario con valor actual precargado"""
        ttk.Label(parent, text=label).grid(row=fila, column=0, sticky='w', pady=5, padx=(0, 10))
        
        if tipo == "entry":
            var = tk.StringVar(value=str(valor_actual) if valor_actual else "")
            entry = ttk.Entry(parent, textvariable=var, width=30)
            entry.grid(row=fila, column=1, sticky='w', pady=5)
            self.campos[nombre] = var
        
        elif tipo == "combobox":
            var = tk.StringVar(value=valor_actual if valor_actual else "")
            combo = ttk.Combobox(parent, textvariable=var, values=valores or [], 
                                width=27, state="readonly")
            combo.grid(row=fila, column=1, sticky='w', pady=5)
            self.campos[nombre] = var
        
        elif tipo == "spinbox":
            var = tk.StringVar(value=str(valor_actual) if valor_actual else "0")
            spinbox = ttk.Spinbox(parent, from_=from_, to=to, textvariable=var, width=27)
            spinbox.grid(row=fila, column=1, sticky='w', pady=5)
            self.campos[nombre] = var
    
    def guardar_cambios(self):
        """Guarda los cambios realizados en el empleado"""
        
        # Recopilar datos del formulario
        datos_formulario = {
            'nombres': self.campos['nombres'].get().strip(),
            'estatus': self.campos['estatus'].get(),
            'num_cuenta': self.campos['num_cuenta'].get().strip(),
            'nacionalidad': self.campos['nacionalidad'].get(),
            'telefono': self.campos['telefono'].get().strip(),
            'email': self.campos['email'].get().strip(),
            'fecha_nac': self.campos['fecha_nac'].get().strip(),
            'fecha_ingreso': self.campos['fecha_ingreso'].get().strip(),
            'sexo': self.campos['sexo'].get(),
            'estado_civil': self.campos['estado_civil'].get(),
            'tipo_sangre': self.campos['tipo_sangre'].get(),
            'cant_hijos': self.campos['cant_hijos'].get(),
            'hijos_0_5': self.campos['hijos_0_5'].get(),
            'hijos_6_12': self.campos['hijos_6_12'].get(),
            'hijos_13_18': self.campos['hijos_13_18'].get(),
            'nivel_academico': self.campos['nivel_academico'].get(),
            'tipo_personal': self.campos['tipo_personal'].get(),
            'cargo': self.campos['cargo'].get(),
            'tipo_nomina': self.campos['tipo_nomina'].get(),
            'zona_residencia': self.campos['zona_residencia'].get(),
            'parroquia': self.campos['parroquia'].get(),
            'sector': self.campos['sector'].get(),
            'area': self.campos['area'].get(),
            'grupo': self.campos['grupo'].get(),
            'condicion': self.campos['condicion'].get(),
            'talla_calzado': self.campos['talla_calzado'].get(),
            'talla_pantalon': self.campos['talla_pantalon'].get(),
            'talla_camisa': self.campos['talla_camisa'].get(),
            'banco': self.campos['banco'].get()
        }
        
        # Validar nombres
        val_nombres, msg_nombres = Validaciones.validar_nombres(datos_formulario['nombres'])
        if not val_nombres:
            messagebox.showerror("Error", msg_nombres)
            return
        
        # Validar estatus
        val_estatus, msg_estatus = Validaciones.validar_estatus(datos_formulario['estatus'])
        if not val_estatus:
            messagebox.showerror("Error", msg_estatus)
            return
        
        # Validar número de cuenta
        if datos_formulario['num_cuenta']:
            val_cuenta, msg_cuenta = Validaciones.validar_numero_cuenta(datos_formulario['num_cuenta'])
            if not val_cuenta:
                messagebox.showerror("Error", msg_cuenta)
                return
        
        # Validar fecha de ingreso
        if datos_formulario['fecha_ingreso']:
            val_fecha_ingreso, msg_fecha_ingreso = Validaciones.validar_fecha_ingreso(datos_formulario['fecha_ingreso'])
            if not val_fecha_ingreso:
                messagebox.showerror("Error", msg_fecha_ingreso)
                return
        
        # Validar teléfono
        val_tel, msg_tel = Validaciones.validar_telefono(datos_formulario['telefono'])
        if not val_tel and datos_formulario['telefono']:
            messagebox.showerror("Error", msg_tel)
            return
        
        # Validar email
        val_email, msg_email = Validaciones.validar_email(datos_formulario['email'])
        if not val_email and datos_formulario['email']:
            messagebox.showerror("Error", msg_email)
            return
        
        # Validar fecha de nacimiento
        fecha_nac = datos_formulario['fecha_nac']
        if fecha_nac:
            val_fecha, msg_fecha = Validaciones.validar_fecha(fecha_nac)
            if not val_fecha:
                messagebox.showerror("Error", msg_fecha)
                return
            edad, msg_edad = Validaciones.validar_edad(fecha_nac)
            if msg_edad:
                if not messagebox.askyesno("Advertencia", f"{msg_edad}\n¿Desea continuar?"):
                    return
        else:
            edad = None
        
        # Obtener IDs
        id_tipo_personal = next((t[0] for t in self.tipos_personal if t[1] == datos_formulario['tipo_personal']), None)
        id_cargo = next((c[0] for c in self.cargos if c[1] == datos_formulario['cargo']), None)
        id_tipo_nomina = next((tn[0] for tn in self.tipos_nomina if tn[1] == datos_formulario['tipo_nomina']), None)
        id_zona = next((z[0] for z in self.zonas_residencia if z[1] == datos_formulario['zona_residencia']), None)
        id_parroquia = next((p[0] for p in self.parroquias if p[1] == datos_formulario['parroquia']), None)
        id_banco = next((b[0] for b in self.bancos if b[2] == datos_formulario['banco']), None)
        
        # Preparar datos para actualización
        datos = (
            datos_formulario['estatus'] or 'ACTIVO',
            datos_formulario['nombres'].upper(),
            datos_formulario['nacionalidad'] or 'V',
            datos_formulario['num_cuenta'] if datos_formulario['num_cuenta'] else None,
            id_tipo_nomina,
            fecha_nac if fecha_nac else None,
            edad,
            datos_formulario['sexo'] or None,
            datos_formulario['estado_civil'] or None,
            datos_formulario['tipo_sangre'] or None,
            int(datos_formulario['cant_hijos'] or 0),
            int(datos_formulario['hijos_0_5'] or 0),
            int(datos_formulario['hijos_6_12'] or 0),
            int(datos_formulario['hijos_13_18'] or 0),
            datos_formulario['nivel_academico'] or None,
            id_zona,
            datos_formulario['sector'].upper() if datos_formulario['sector'] else None,
            datos_formulario['telefono'] if datos_formulario['telefono'] else None,
            datos_formulario['email'].lower() if datos_formulario['email'] else None,
            datos_formulario['condicion'] or None,
            self.campos['usa_lentes'].get(),
            float(datos_formulario['talla_calzado']) if datos_formulario['talla_calzado'] else None,
            datos_formulario['talla_pantalon'] or None,
            datos_formulario['talla_camisa'] or None,
            id_cargo,
            datos_formulario['area'].upper() if datos_formulario['area'] else None,
            datos_formulario['grupo'].upper() if datos_formulario['grupo'] else None,
            id_tipo_personal,
            id_parroquia,
            id_banco
        )
        
        # Confirmar cambios
        if not messagebox.askyesno("Confirmar", "¿Está seguro de guardar los cambios?"):
            return
        
        try:
            resultado = Queries.actualizar_empleado(self.empleado_id, datos)
            if resultado is not None:
                messagebox.showinfo("Éxito", "Empleado modificado correctamente")
                self.callback_actualizar()
                self.ventana.destroy()
            else:
                messagebox.showerror("Error", "No se pudo modificar el empleado")
        except Exception as e:
            messagebox.showerror("Error", f"Error al guardar: {str(e)}")