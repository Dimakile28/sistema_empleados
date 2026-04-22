import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from database.conexion import db
from database.queries import Queries
from utils.validaciones import Validaciones

class VentanaRegistro:
    """Ventana para registrar nuevo personal"""
    
    def __init__(self, parent, callback_actualizar):
        self.parent = parent
        self.callback_actualizar = callback_actualizar
        
        self.ventana = tk.Toplevel(parent)
        self.ventana.title("Registrar Personal")
        self.ventana.geometry("750x800")
        self.ventana.resizable(False, False)
        self.ventana.transient(parent)
        self.ventana.grab_set()
        
        # Centrar ventana
        self.centrar_ventana()
        
        # Cargar datos de tablas maestras
        self.cargar_datos_maestros()
        
        # Crear formulario
        self.crear_formulario()
    
    def centrar_ventana(self):
        """Centra la ventana en la pantalla"""
        self.ventana.update_idletasks()
        ancho = 950
        alto = 800
        x = (self.ventana.winfo_screenwidth() // 2) - (ancho // 2)
        y = (self.ventana.winfo_screenheight() // 2) - (alto // 2)
        self.ventana.geometry(f'{ancho}x{alto}+{x}+{y}')
    
    def cargar_datos_maestros(self):
        """Carga los datos de las tablas maestras"""
        self.tipos_personal = Queries.get_tipos_personal() or []
        self.cargos = Queries.get_cargos() or []
        self.tipos_nomina = Queries.get_tipos_nomina() or []
        self.zonas_residencia = Queries.get_zonas_residencia() or []
        self.parroquias = Queries.get_parroquias() or []
        self.bancos = Queries.get_bancos() or []
    
    def crear_formulario(self):
        """Crea el formulario de registro"""
        
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
        
        # Título
        titulo = ttk.Label(scrollable_frame, text="Registro de Personal", 
                          font=('Helvetica', 16, 'bold'))
        titulo.pack(pady=(0, 20))
        
        # Crear frame para dos columnas
        columns_frame = ttk.Frame(scrollable_frame)
        columns_frame.pack(fill=tk.BOTH, expand=True)
        
        col1 = ttk.Frame(columns_frame)
        col1.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        col2 = ttk.Frame(columns_frame)
        col2.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(10, 0))
        
        # Diccionario para almacenar los campos
        self.campos = {}
        
        # === COLUMNA 1 ===
        # Datos personales
        frame_personal = ttk.LabelFrame(col1, text="Datos Personales", padding="10")
        frame_personal.pack(fill=tk.X, pady=(0, 10))
        
        self.crear_campo(frame_personal, "Cédula:", "cedula", 0, placeholder="12345678")
        self.crear_campo(frame_personal, "Nombres y Apellidos:", "nombres", 1)
        self.crear_campo(frame_personal, "Nacionalidad:", "nacionalidad", 2, 
                        valores=["V", "E"], tipo="combobox")
        self.crear_campo(frame_personal, "Fecha de Nacimiento:", "fecha_nac", 3,
                        placeholder="YYYY-MM-DD")
        self.crear_campo(frame_personal, "Sexo:", "sexo", 4,
                        valores=["M", "F"], tipo="combobox")
        self.crear_campo(frame_personal, "Estado Civil:", "estado_civil", 5,
                        valores=["SOLTERO", "CASADO", "DIVORCIADO", "VIUDO", "CONCUBINO"], 
                        tipo="combobox")
        self.crear_campo(frame_personal, "Tipo de Sangre:", "tipo_sangre", 6,
                        valores=["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"], 
                        tipo="combobox")
        
        # Hijos
        frame_hijos = ttk.LabelFrame(col1, text="Hijos", padding="10")
        frame_hijos.pack(fill=tk.X, pady=(0, 10))
        
        self.crear_campo(frame_hijos, "Cantidad de Hijos:", "cant_hijos", 0, tipo="spinbox",
                        from_=0, to=20)
        self.crear_campo(frame_hijos, "Hijos 0-5 años:", "hijos_0_5", 1, tipo="spinbox",
                        from_=0, to=10)
        self.crear_campo(frame_hijos, "Hijos 6-12 años:", "hijos_6_12", 2, tipo="spinbox",
                        from_=0, to=10)
        self.crear_campo(frame_hijos, "Hijos 13-18 años:", "hijos_13_18", 3, tipo="spinbox",
                        from_=0, to=10)
        
        # === COLUMNA 2 ===
        # Datos laborales
        frame_laboral = ttk.LabelFrame(col2, text="Datos Laborales", padding="10")
        frame_laboral.pack(fill=tk.X, pady=(0, 10))
        
        self.crear_campo(frame_laboral, "Estatus:", "estatus", 0,
                        valores=["ACTIVO", "INACTIVO"], tipo="combobox")
        self.crear_campo(frame_laboral, "Tipo de Personal:", "tipo_personal", 1,
                        valores=[f"{tp[1]}" for tp in self.tipos_personal], tipo="combobox")
        self.crear_campo(frame_laboral, "Cargo:", "cargo", 2,
                        valores=[f"{c[1]}" for c in self.cargos], tipo="combobox")
        self.crear_campo(frame_laboral, "Tipo de Nómina:", "tipo_nomina", 3,
                        valores=[f"{tn[1]}" for tn in self.tipos_nomina], tipo="combobox")
        self.crear_campo(frame_laboral, "Área:", "area", 4)
        self.crear_campo(frame_laboral, "Grupo:", "grupo", 5)
        self.crear_campo(frame_laboral, "Nivel Académico:", "nivel_academico", 6,
                        valores=["PRIMARIA", "BACHILLER", "TECNICO MEDIO", "TSU", 
                                "UNIVERSITARIA", "POSTGRADO"], tipo="combobox")
        self.crear_campo(frame_laboral, "Fecha de Ingreso:", "fecha_ingreso", 7,
                        placeholder="YYYY-MM-DD")
        
        # Ubicación
        frame_ubicacion = ttk.LabelFrame(col2, text="Ubicación", padding="10")
        frame_ubicacion.pack(fill=tk.X, pady=(0, 10))
        
        self.crear_campo(frame_ubicacion, "Zona de Residencia:", "zona_residencia", 0,
                        valores=[f"{z[1]}" for z in self.zonas_residencia], tipo="combobox")
        self.crear_campo(frame_ubicacion, "Parroquia:", "parroquia", 1,
                        valores=[f"{p[1]}" for p in self.parroquias], tipo="combobox")
        self.crear_campo(frame_ubicacion, "Sector:", "sector", 2)
        
        # Contacto
        frame_contacto = ttk.LabelFrame(col2, text="Contacto y Datos Bancarios", padding="10")
        frame_contacto.pack(fill=tk.X, pady=(0, 10))
        
        self.crear_campo(frame_contacto, "Teléfono:", "telefono", 0)
        self.crear_campo(frame_contacto, "Correo Electrónico:", "email", 1)
        self.crear_campo(frame_contacto, "Número de Cuenta:", "num_cuenta", 2)
        self.crear_campo(frame_contacto, "Banco:", "banco", 3,
                        valores=[f"{b[2]}" for b in self.bancos], tipo="combobox")
        
        # Tallas
        frame_tallas = ttk.LabelFrame(col2, text="Tallas", padding="10")
        frame_tallas.pack(fill=tk.X, pady=(0, 10))
        
        self.crear_campo(frame_tallas, "Talla de Calzado:", "talla_calzado", 0)
        self.crear_campo(frame_tallas, "Talla de Pantalón:", "talla_pantalon", 1,
                        valores=["XS", "S", "M", "L", "XL", "XXL", "XXXL"], tipo="combobox")
        self.crear_campo(frame_tallas, "Talla de Camisa:", "talla_camisa", 2,
                        valores=["XS", "S", "M", "L", "XL", "XXL", "XXXL"], tipo="combobox")
        
        # Otros
        frame_otros = ttk.LabelFrame(col2, text="Otros", padding="10")
        frame_otros.pack(fill=tk.X, pady=(0, 10))
        
        self.crear_campo(frame_otros, "Condición Médica:", "condicion", 0)
        
        # Checkbox para lentes
        self.campos['usa_lentes'] = tk.BooleanVar()
        chk_lentes = ttk.Checkbutton(frame_otros, text="Usa Lentes", 
                                     variable=self.campos['usa_lentes'])
        chk_lentes.grid(row=1, column=0, columnspan=2, sticky='w', pady=5)
        
        # Botones
        frame_botones = ttk.Frame(scrollable_frame)
        frame_botones.pack(pady=20)
        
        btn_guardar = tk.Button(frame_botones, text="💾 Guardar", command=self.guardar,
                               bg="#2ecc71", fg="white", font=('Helvetica', 11),
                               padx=20, pady=5, cursor='hand2')
        btn_guardar.pack(side=tk.LEFT, padx=5)
        
        btn_cancelar = tk.Button(frame_botones, text="❌ Cancelar", command=self.ventana.destroy,
                                bg="#e74c3c", fg="white", font=('Helvetica', 11),
                                padx=20, pady=5, cursor='hand2')
        btn_cancelar.pack(side=tk.LEFT, padx=5)
    
    def crear_campo(self, parent, label, nombre, fila, tipo="entry", valores=None, 
                   from_=None, to=None, placeholder=""):
        """Crea un campo de formulario"""
        ttk.Label(parent, text=label).grid(row=fila, column=0, sticky='w', pady=5, padx=(0, 10))
        
        if tipo == "entry":
            var = tk.StringVar()
            entry = ttk.Entry(parent, textvariable=var, width=30)
            entry.grid(row=fila, column=1, sticky='w', pady=5)
            self.campos[nombre] = var
            
            if placeholder:
                entry.insert(0, placeholder)
                entry.bind('<FocusIn>', lambda e, entry=entry, ph=placeholder: 
                          self.on_focus_in(entry, ph))
                entry.bind('<FocusOut>', lambda e, entry=entry, ph=placeholder: 
                          self.on_focus_out(entry, ph))
        
        elif tipo == "combobox":
            var = tk.StringVar()
            combo = ttk.Combobox(parent, textvariable=var, values=valores or [], 
                                width=27, state="readonly")
            combo.grid(row=fila, column=1, sticky='w', pady=5)
            if valores and len(valores) > 0:
                combo.current(0)
                var.set(valores[0])
            self.campos[nombre] = var
        
        elif tipo == "spinbox":
            var = tk.StringVar()
            spinbox = ttk.Spinbox(parent, from_=from_, to=to, textvariable=var, width=27)
            spinbox.grid(row=fila, column=1, sticky='w', pady=5)
            self.campos[nombre] = var
    
    def on_focus_in(self, entry, placeholder):
        if entry.get() == placeholder:
            entry.delete(0, tk.END)
    
    def on_focus_out(self, entry, placeholder):
        if entry.get() == "":
            entry.insert(0, placeholder)
    
    def guardar(self):
        """Guarda el nuevo empleado en la base de datos"""
        
        # Recopilar datos del formulario
        datos_formulario = {
            'cedula': self.campos['cedula'].get().strip(),
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
        
        # Validar campos obligatorios
        errores_obligatorios = Validaciones.validar_campos_obligatorios(datos_formulario)
        if errores_obligatorios:
            messagebox.showerror("Error", "Campos obligatorios faltantes:\n- " + "\n- ".join(errores_obligatorios))
            return
        
        # Validar cédula
        val_cedula, msg_cedula = Validaciones.validar_cedula(datos_formulario['cedula'])
        if not val_cedula:
            messagebox.showerror("Error", msg_cedula)
            return
        
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
        val_cuenta, msg_cuenta = Validaciones.validar_numero_cuenta(datos_formulario['num_cuenta'])
        if not val_cuenta:
            messagebox.showerror("Error", msg_cuenta)
            return
        
        # Validar fecha de ingreso
        val_fecha_ingreso, msg_fecha_ingreso = Validaciones.validar_fecha_ingreso(datos_formulario['fecha_ingreso'])
        if not val_fecha_ingreso:
            messagebox.showerror("Error", msg_fecha_ingreso)
            return
        
        # Validar estado civil
        estado_civil_valido = datos_formulario['estado_civil']
        valores_estado_civil = ["SOLTERO", "CASADO", "DIVORCIADO", "VIUDO", "CONCUBINO"]
        if estado_civil_valido and estado_civil_valido not in valores_estado_civil:
            messagebox.showerror("Error", f"'{estado_civil_valido}' no es un estado civil válido")
            return
        
        # Validar tipo de sangre
        tipo_sangre_valido = datos_formulario['tipo_sangre']
        valores_tipo_sangre = ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"]
        if tipo_sangre_valido and tipo_sangre_valido not in valores_tipo_sangre:
            messagebox.showerror("Error", f"'{tipo_sangre_valido}' no es un tipo de sangre válido")
            return
        
        # Validar nivel académico
        nivel_academico_valido = datos_formulario['nivel_academico']
        valores_nivel_academico = ["PRIMARIA", "BACHILLER", "TECNICO MEDIO", "TSU", "UNIVERSITARIA", "POSTGRADO"]
        if nivel_academico_valido and nivel_academico_valido not in valores_nivel_academico:
            messagebox.showerror("Error", f"'{nivel_academico_valido}' no es un nivel académico válido")
            return
        
        # Validar tallas
        valores_tallas = ["XS", "S", "M", "L", "XL", "XXL", "XXXL"]
        talla_pantalon = datos_formulario['talla_pantalon']
        if talla_pantalon and talla_pantalon not in valores_tallas:
            messagebox.showerror("Error", f"'{talla_pantalon}' no es una talla de pantalón válida")
            return
        
        talla_camisa = datos_formulario['talla_camisa']
        if talla_camisa and talla_camisa not in valores_tallas:
            messagebox.showerror("Error", f"'{talla_camisa}' no es una talla de camisa válida")
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
        
        # Validar sexo
        val_sexo, msg_sexo = Validaciones.validar_sexo(datos_formulario['sexo'])
        if not val_sexo and datos_formulario['sexo']:
            messagebox.showerror("Error", msg_sexo)
            return
        
        # Validar cantidad de hijos
        val_hijos, msg_hijos = Validaciones.validar_cantidad_hijos(datos_formulario['cant_hijos'])
        if not val_hijos:
            messagebox.showerror("Error", msg_hijos)
            return
        
        # Validar talla de calzado
        val_talla_cal, msg_talla_cal = Validaciones.validar_talla_calzado(datos_formulario['talla_calzado'])
        if not val_talla_cal and datos_formulario['talla_calzado']:
            messagebox.showerror("Error", msg_talla_cal)
            return
        
        # Obtener IDs
        id_tipo_personal = next((t[0] for t in self.tipos_personal if t[1] == datos_formulario['tipo_personal']), None)
        id_cargo = next((c[0] for c in self.cargos if c[1] == datos_formulario['cargo']), None)
        id_tipo_nomina = next((tn[0] for tn in self.tipos_nomina if tn[1] == datos_formulario['tipo_nomina']), None)
        id_zona = next((z[0] for z in self.zonas_residencia if z[1] == datos_formulario['zona_residencia']), None)
        id_parroquia = next((p[0] for p in self.parroquias if p[1] == datos_formulario['parroquia']), None)
        id_banco = next((b[0] for b in self.bancos if b[2] == datos_formulario['banco']), None)
        
        # Verificar que la cédula no esté duplicada
        cedula = datos_formulario['cedula']
        resultado_existente = Queries.buscar_empleado(cedula=cedula)
        if resultado_existente:
            messagebox.showerror("Error", f"Ya existe un empleado con la cédula {cedula}")
            return
        
        # Preparar datos para inserción
        datos = (
            datos_formulario['estatus'] or 'ACTIVO',
            datos_formulario['nombres'].upper(),
            cedula,
            datos_formulario['nacionalidad'] or 'V',
            datos_formulario['num_cuenta'],
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
            datos_formulario['fecha_ingreso'],
            id_banco
        )
        
        try:
            resultado = Queries.insertar_empleado(datos)
            if resultado:
                messagebox.showinfo("Éxito", "Empleado registrado correctamente")
                self.callback_actualizar()
                self.ventana.destroy()
            else:
                messagebox.showerror("Error", "No se pudo registrar el empleado")
        except Exception as e:
            messagebox.showerror("Error", f"Error al guardar: {str(e)}")