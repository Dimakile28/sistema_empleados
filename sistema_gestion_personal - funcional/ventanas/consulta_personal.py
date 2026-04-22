import tkinter as tk
from tkinter import ttk, messagebox
from database.conexion import db
from database.queries import Queries

class VentanaConsulta:
    """Ventana para consultar personal"""
    
    def __init__(self, parent):
        self.parent = parent
        
        self.ventana = tk.Toplevel(parent)
        self.ventana.title("Consultar Personal")
        self.ventana.geometry("1300x700")
        self.ventana.transient(parent)
        self.ventana.grab_set()
        
        self.centrar_ventana()
        self.crear_interfaz()
    
    def centrar_ventana(self):
        self.ventana.update_idletasks()
        ancho = 1300
        alto = 700
        x = (self.ventana.winfo_screenwidth() // 2) - (ancho // 2)
        y = (self.ventana.winfo_screenheight() // 2) - (alto // 2)
        self.ventana.geometry(f'{ancho}x{alto}+{x}+{y}')
    
    def crear_interfaz(self):
        # Frame principal
        main_frame = ttk.Frame(self.ventana, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Frame de búsqueda
        search_frame = ttk.LabelFrame(main_frame, text="Búsqueda", padding="10")
        search_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Opciones de búsqueda
        ttk.Label(search_frame, text="Buscar por:").grid(row=0, column=0, padx=5, pady=5)
        
        self.buscar_por = tk.StringVar(value="cedula")
        rb_cedula = ttk.Radiobutton(search_frame, text="Cédula", variable=self.buscar_por, value="cedula")
        rb_cedula.grid(row=0, column=1, padx=5, pady=5)
        
        rb_nombre = ttk.Radiobutton(search_frame, text="Nombre", variable=self.buscar_por, value="nombre")
        rb_nombre.grid(row=0, column=2, padx=5, pady=5)
        
        rb_apellido = ttk.Radiobutton(search_frame, text="Apellido", variable=self.buscar_por, value="apellido")
        rb_apellido.grid(row=0, column=3, padx=5, pady=5)
        
        rb_todos = ttk.Radiobutton(search_frame, text="Todos", variable=self.buscar_por, value="todos")
        rb_todos.grid(row=0, column=4, padx=5, pady=5)
        
        # Campo de búsqueda
        self.buscar_texto = tk.StringVar()
        entry_buscar = ttk.Entry(search_frame, textvariable=self.buscar_texto, width=30)
        entry_buscar.grid(row=1, column=0, columnspan=3, padx=5, pady=5, sticky='w')
        
        btn_buscar = tk.Button(search_frame, text="🔍 Buscar", command=self.buscar,
                              bg="#3498db", fg="white", cursor='hand2')
        btn_buscar.grid(row=1, column=3, padx=5, pady=5)
        
        btn_limpiar = tk.Button(search_frame, text="🗑️ Limpiar", command=self.limpiar,
                               bg="#95a5a6", fg="white", cursor='hand2')
        btn_limpiar.grid(row=1, column=4, padx=5, pady=5)
        
        # Treeview para resultados
        tree_frame = ttk.LabelFrame(main_frame, text="Resultados", padding="10")
        tree_frame.pack(fill=tk.BOTH, expand=True)
        
        # Scrollbars
        scroll_y = ttk.Scrollbar(tree_frame, orient="vertical")
        scroll_x = ttk.Scrollbar(tree_frame, orient="horizontal")
        
        # Columnas incluyendo BANCO
        columnas = ("ID", "Cédula", "Nombre", "Estatus", "Cargo", "Tipo", "Nómina", 
                   "Zona", "Parroquia", "Teléfono", "Email", "Banco")
        
        self.tree = ttk.Treeview(tree_frame, columns=columnas, show="headings",
                                 yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)
        
        scroll_y.config(command=self.tree.yview)
        scroll_x.config(command=self.tree.xview)
        
        scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
        scroll_x.pack(side=tk.BOTTOM, fill=tk.X)
        self.tree.pack(fill=tk.BOTH, expand=True)
        
        # Configurar columnas
        anchos = [50, 100, 250, 80, 120, 100, 120, 100, 120, 100, 180, 150]
        for col, ancho in zip(columnas, anchos):
            self.tree.heading(col, text=col)
            self.tree.column(col, width=ancho)
        
        # Bind doble click para ver detalles
        self.tree.bind("<Double-1>", self.ver_detalles)
        
        # Frame para botones de acción
        action_frame = ttk.Frame(main_frame)
        action_frame.pack(fill=tk.X, pady=(10, 0))
        
        btn_exportar = tk.Button(action_frame, text="📊 Exportar Resultados", command=self.exportar_resultados,
                                bg="#9b59b6", fg="white", cursor='hand2')
        btn_exportar.pack(side=tk.LEFT, padx=5)
        
        btn_cerrar = tk.Button(action_frame, text="❌ Cerrar", command=self.ventana.destroy,
                              bg="#e74c3c", fg="white", cursor='hand2')
        btn_cerrar.pack(side=tk.RIGHT, padx=5)
        
        # Cargar todos los empleados al inicio
        self.buscar()
    
    def buscar(self):
        """Ejecuta la búsqueda según el criterio seleccionado"""
        # Limpiar treeview
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        criterio = self.buscar_por.get()
        texto = self.buscar_texto.get().strip()
        
        if criterio == "todos":
            resultados = Queries.buscar_empleado()
        elif criterio == "cedula":
            if not texto:
                messagebox.showwarning("Advertencia", "Ingrese una cédula para buscar")
                return
            resultados = Queries.buscar_empleado(cedula=texto)
        elif criterio == "nombre":
            if not texto:
                messagebox.showwarning("Advertencia", "Ingrese un nombre para buscar")
                return
            resultados = Queries.buscar_empleado(nombre=texto)
        elif criterio == "apellido":
            if not texto:
                messagebox.showwarning("Advertencia", "Ingrese un apellido para buscar")
                return
            resultados = Queries.buscar_empleado(apellido=texto)
        else:
            resultados = []
        
        if resultados:
            for row in resultados:
                # row[0]=id, row[1]=cedula, row[2]=nombre, row[3]=estatus, row[4]=cargo,
                # row[5]=tipo_personal, row[6]=nomina, row[7]=zona, row[8]=parroquia,
                # row[9]=telefono, row[10]=email, row[28]=banco (índice 28)
                banco = row[28] if len(row) > 28 else ""
                valores = (row[0], row[1], row[2], row[3], row[4], row[5], row[6],
                          row[7], row[8], row[9], row[10], banco)
                self.tree.insert("", tk.END, values=valores)
        else:
            messagebox.showinfo("Información", "No se encontraron resultados")
    
    def limpiar(self):
        """Limpia los campos de búsqueda y muestra todos"""
        self.buscar_texto.set("")
        self.buscar_por.set("todos")
        self.buscar()
    
    def ver_detalles(self, event):
        """Muestra los detalles del empleado seleccionado"""
        seleccion = self.tree.selection()
        if not seleccion:
            return
        
        item = self.tree.item(seleccion[0])
        empleado_id = item['values'][0]
        
        # Ventana de detalles
        detalle_ventana = tk.Toplevel(self.ventana)
        detalle_ventana.title("Detalles del Empleado")
        detalle_ventana.geometry("700x600")
        detalle_ventana.transient(self.ventana)
        detalle_ventana.grab_set()
        
        # Centrar ventana
        detalle_ventana.update_idletasks()
        x = (detalle_ventana.winfo_screenwidth() // 2) - 350
        y = (detalle_ventana.winfo_screenheight() // 2) - 300
        detalle_ventana.geometry(f'700x600+{x}+{y}')
        
        # Obtener datos completos
        empleado = Queries.obtener_empleado_por_id(empleado_id)
        
        if empleado:
            # Crear frame con scroll
            canvas = tk.Canvas(detalle_ventana)
            scrollbar = ttk.Scrollbar(detalle_ventana, orient="vertical", command=canvas.yview)
            scrollable_frame = ttk.Frame(canvas)
            
            scrollable_frame.bind(
                "<Configure>",
                lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
            )
            
            canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
            canvas.configure(yscrollcommand=scrollbar.set)
            
            canvas.pack(side="left", fill="both", expand=True)
            scrollbar.pack(side="right", fill="y")
            
            # Obtener nombres de banco y zona
            nombre_banco = ""
            nombre_zona = ""
            nombre_parroquia = ""
            
            # Buscar nombre del banco
            if len(empleado) > 33 and empleado[33]:
                bancos = Queries.get_bancos()
                for b in bancos:
                    if b[0] == empleado[33]:
                        nombre_banco = b[2]
                        break
            
            # Buscar nombre de la zona
            if len(empleado) > 18 and empleado[18]:
                zonas = Queries.get_zonas_residencia()
                for z in zonas:
                    if z[0] == empleado[18]:
                        nombre_zona = z[1]
                        break
            
            # Buscar nombre de la parroquia
            if len(empleado) > 31 and empleado[31]:
                parroquias = Queries.get_parroquias()
                for p in parroquias:
                    if p[0] == empleado[31]:
                        nombre_parroquia = p[1]
                        break
            
            # Mostrar información
            campos = [
                ("ID:", empleado[0]),
                ("Cédula:", empleado[4]),
                ("Nombres:", empleado[3]),
                ("Estatus:", empleado[1]),
                ("Fecha de Ingreso:", empleado[2] if empleado[2] else "No registrada"),
                ("Nacionalidad:", empleado[5]),
                ("Número de Cuenta:", empleado[6]),
                ("Banco:", nombre_banco if nombre_banco else "No asignado"),
                ("Fecha de Nacimiento:", empleado[8] if empleado[8] else "No registrada"),
                ("Edad:", empleado[9] if empleado[9] else "N/A"),
                ("Sexo:", empleado[10] if empleado[10] else "N/A"),
                ("Estado Civil:", empleado[11] if empleado[11] else "N/A"),
                ("Tipo de Sangre:", empleado[12] if empleado[12] else "N/A"),
                ("Cantidad de Hijos:", empleado[13] if empleado[13] else "0"),
                ("Nivel Académico:", empleado[17] if empleado[17] else "N/A"),
                ("Zona de Residencia:", nombre_zona if nombre_zona else "No asignada"),
                ("Parroquia:", nombre_parroquia if nombre_parroquia else "No asignada"),
                ("Sector:", empleado[19] if empleado[19] else "N/A"),
                ("Teléfono:", empleado[20] if empleado[20] else "N/A"),
                ("Email:", empleado[21] if empleado[21] else "N/A"),
                ("Condición Médica:", empleado[22] if empleado[22] else "Ninguna"),
                ("Usa Lentes:", "Sí" if empleado[23] else "No"),
                ("Talla Calzado:", empleado[24] if empleado[24] else "N/A"),
                ("Talla Pantalón:", empleado[25] if empleado[25] else "N/A"),
                ("Talla Camisa:", empleado[26] if empleado[26] else "N/A"),
                ("Cargo:", empleado[27] if len(empleado) > 27 else "N/A"),
                ("Área:", empleado[28] if len(empleado) > 28 else "N/A"),
                ("Grupo:", empleado[29] if len(empleado) > 29 else "N/A"),
                ("Tipo Personal:", empleado[30] if len(empleado) > 30 else "N/A")
            ]
            
            for i, (label, valor) in enumerate(campos):
                frame = ttk.Frame(scrollable_frame)
                frame.pack(fill=tk.X, padx=20, pady=3)
                
                ttk.Label(frame, text=label, font=('Helvetica', 10, 'bold'), width=20, anchor='w').pack(side=tk.LEFT)
                ttk.Label(frame, text=valor or "N/A", font=('Helvetica', 10)).pack(side=tk.LEFT, padx=(10, 0))
            
            btn_cerrar = tk.Button(scrollable_frame, text="Cerrar", command=detalle_ventana.destroy,
                                  bg="#3498db", fg="white", cursor='hand2')
            btn_cerrar.pack(pady=20)
    
    def exportar_resultados(self):
        """Exporta los resultados actuales a Excel"""
        from ventanas.exportar_datos import ExportarDatos
        
        # Obtener datos del treeview
        datos = []
        for item in self.tree.get_children():
            valores = self.tree.item(item)['values']
            datos.append(valores)
        
        if datos:
            ExportarDatos.exportar_a_excel(datos, self.ventana)
        else:
            messagebox.showwarning("Advertencia", "No hay datos para exportar")