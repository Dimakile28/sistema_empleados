import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import pandas as pd
import re
from datetime import datetime
from database.conexion import db
from database.queries import Queries
from utils.validaciones import Validaciones

class VentanaCargaMasiva:
    """Ventana para carga masiva de empleados desde Excel"""
    
    def __init__(self, parent, callback_actualizar):
        self.parent = parent
        self.callback_actualizar = callback_actualizar
        
        self.ventana = tk.Toplevel(parent)
        self.ventana.title("Carga Masiva de Personal")
        self.ventana.geometry("900x700")
        self.ventana.transient(parent)
        self.ventana.grab_set()
        
        self.centrar_ventana()
        self.crear_interfaz()
        self.cargar_datos_maestros()
    
    def centrar_ventana(self):
        self.ventana.update_idletasks()
        ancho = 900
        alto = 700
        x = (self.ventana.winfo_screenwidth() // 2) - (ancho // 2)
        y = (self.ventana.winfo_screenheight() // 2) - (alto // 2)
        self.ventana.geometry(f'{ancho}x{alto}+{x}+{y}')
    
    def cargar_datos_maestros(self):
        """Carga los datos de las tablas maestras para mapeo"""
        self.tipos_personal = {t[1]: t[0] for t in (Queries.get_tipos_personal() or [])}
        self.cargos = {c[1]: c[0] for c in (Queries.get_cargos() or [])}
        self.tipos_nomina = {tn[1]: tn[0] for tn in (Queries.get_tipos_nomina() or [])}
        self.zonas_residencia = {n[1]: n[0] for n in (Queries.get_zonas_residencia() or [])}
        self.parroquias = {p[1]: p[0] for p in (Queries.get_parroquias() or [])}
    
    def crear_interfaz(self):
        # Frame principal
        main_frame = ttk.Frame(self.ventana, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Título
        titulo = ttk.Label(main_frame, text="Carga Masiva de Personal", 
                          font=('Helvetica', 16, 'bold'))
        titulo.pack(pady=(0, 10))
        
        subtitulo = ttk.Label(main_frame, text="Importar empleados desde archivo Excel",
                             font=('Helvetica', 10), foreground='gray')
        subtitulo.pack(pady=(0, 20))
        
        # Frame para selección de archivo
        archivo_frame = ttk.LabelFrame(main_frame, text="Seleccionar Archivo", padding="10")
        archivo_frame.pack(fill=tk.X, pady=(0, 15))
        
        self.ruta_archivo = tk.StringVar()
        entry_archivo = ttk.Entry(archivo_frame, textvariable=self.ruta_archivo, width=60)
        entry_archivo.pack(side=tk.LEFT, padx=(0, 10))
        
        btn_examinar = tk.Button(archivo_frame, text="📂 Examinar", command=self.seleccionar_archivo,
                                bg="#3498db", fg="white", cursor='hand2')
        btn_examinar.pack(side=tk.LEFT)
        
        btn_plantilla = tk.Button(archivo_frame, text="📄 Generar Plantilla", command=self.generar_plantilla,
                                 bg="#1abc9c", fg="white", cursor='hand2')
        btn_plantilla.pack(side=tk.LEFT, padx=(10, 0))
        
        # Frame para opciones
        opciones_frame = ttk.LabelFrame(main_frame, text="Opciones de Importación", padding="10")
        opciones_frame.pack(fill=tk.X, pady=(0, 15))
        
        self.validar_duplicados = tk.BooleanVar(value=True)
        chk_validar = ttk.Checkbutton(opciones_frame, text="Validar cédulas duplicadas (no importar repetidos)",
                                     variable=self.validar_duplicados)
        chk_validar.pack(anchor='w')
        
        self.actualizar_existentes = tk.BooleanVar(value=False)
        chk_actualizar = ttk.Checkbutton(opciones_frame, text="Actualizar datos de empleados existentes",
                                        variable=self.actualizar_existentes)
        chk_actualizar.pack(anchor='w')
        
        # Botones de acción
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(pady=10)
        
        btn_preview = tk.Button(btn_frame, text="👁️ Previsualizar", command=self.previsualizar,
                               bg="#f39c12", fg="white", font=('Helvetica', 10),
                               padx=15, pady=5, cursor='hand2')
        btn_preview.pack(side=tk.LEFT, padx=5)
        
        btn_importar = tk.Button(btn_frame, text="📥 Importar", command=self.importar,
                                bg="#2ecc71", fg="white", font=('Helvetica', 10),
                                padx=15, pady=5, cursor='hand2')
        btn_importar.pack(side=tk.LEFT, padx=5)
        
        btn_limpiar = tk.Button(btn_frame, text="🗑️ Limpiar", command=self.limpiar,
                               bg="#95a5a6", fg="white", font=('Helvetica', 10),
                               padx=15, pady=5, cursor='hand2')
        btn_limpiar.pack(side=tk.LEFT, padx=5)
        
        # Frame para resultados
        resultados_frame = ttk.LabelFrame(main_frame, text="Resultados de Importación", padding="10")
        resultados_frame.pack(fill=tk.BOTH, expand=True)
        
        # Treeview para resultados
        scroll_y = ttk.Scrollbar(resultados_frame, orient="vertical")
        scroll_x = ttk.Scrollbar(resultados_frame, orient="horizontal")
        
        columnas = ("Estado", "Cédula", "Nombres", "Mensaje")
        
        self.tree_resultados = ttk.Treeview(resultados_frame, columns=columnas, show="headings",
                                           yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)
        
        scroll_y.config(command=self.tree_resultados.yview)
        scroll_x.config(command=self.tree_resultados.xview)
        
        scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
        scroll_x.pack(side=tk.BOTTOM, fill=tk.X)
        self.tree_resultados.pack(fill=tk.BOTH, expand=True)
        
        # Configurar columnas
        self.tree_resultados.heading("Estado", text="Estado")
        self.tree_resultados.heading("Cédula", text="Cédula")
        self.tree_resultados.heading("Nombres", text="Nombres")
        self.tree_resultados.heading("Mensaje", text="Mensaje")
        
        self.tree_resultados.column("Estado", width=80)
        self.tree_resultados.column("Cédula", width=100)
        self.tree_resultados.column("Nombres", width=250)
        self.tree_resultados.column("Mensaje", width=350)
        
        # Configurar tags para colores
        self.tree_resultados.tag_configure('exito', background='#d4edda')
        self.tree_resultados.tag_configure('error', background='#f8d7da')
        self.tree_resultados.tag_configure('advertencia', background='#fff3cd')
        
        # Barra de progreso
        self.progress = ttk.Progressbar(main_frame, mode='indeterminate')
        self.progress.pack(fill=tk.X, pady=(10, 0))
        
        # Footer
        footer = ttk.Label(main_frame, text="Formato requerido: Excel con columnas: CEDULA, NOMBRES Y APELLIDOS, CARGO, etc.",
                          font=('Helvetica', 8), foreground='gray')
        footer.pack(pady=(10, 0))
    
    def seleccionar_archivo(self):
        """Selecciona el archivo Excel a importar"""
        archivo = filedialog.askopenfilename(
            title="Seleccionar archivo Excel",
            filetypes=[("Excel files", "*.xlsx *.xls"), ("All files", "*.*")]
        )
        if archivo:
            self.ruta_archivo.set(archivo)
    
    def generar_plantilla(self):
        """Genera una plantilla de Excel para carga masiva"""
        from ventanas.carga_masiva import GenerarPlantilla
        GenerarPlantilla.generar()
    
    def previsualizar(self):
        """Previsualiza los datos del archivo Excel"""
        ruta = self.ruta_archivo.get().strip()
        if not ruta:
            messagebox.showwarning("Advertencia", "Seleccione un archivo Excel primero")
            return
        
        try:
            df = pd.read_excel(ruta)
            
            # Limpiar nombres de columnas
            df.columns = [str(col).replace('\n', ' ').strip().upper() for col in df.columns]
            
            # Ventana de previsualización
            preview_win = tk.Toplevel(self.ventana)
            preview_win.title("Previsualización de Datos")
            preview_win.geometry("800x500")
            preview_win.transient(self.ventana)
            preview_win.grab_set()
            
            # Centrar ventana
            preview_win.update_idletasks()
            x = (preview_win.winfo_screenwidth() // 2) - 400
            y = (preview_win.winfo_screenheight() // 2) - 250
            preview_win.geometry(f'800x500+{x}+{y}')
            
            # Frame principal
            main_frame = ttk.Frame(preview_win, padding="10")
            main_frame.pack(fill=tk.BOTH, expand=True)
            
            ttk.Label(main_frame, text=f"Vista previa - {len(df)} registros encontrados",
                     font=('Helvetica', 12, 'bold')).pack(pady=(0, 10))
            
            # Treeview
            scroll_y = ttk.Scrollbar(main_frame, orient="vertical")
            scroll_x = ttk.Scrollbar(main_frame, orient="horizontal")
            
            columnas = list(df.columns[:8])  # Mostrar primeras 8 columnas
            tree = ttk.Treeview(main_frame, columns=columnas, show="headings",
                               yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)
            
            scroll_y.config(command=tree.yview)
            scroll_x.config(command=tree.xview)
            
            scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
            scroll_x.pack(side=tk.BOTTOM, fill=tk.X)
            tree.pack(fill=tk.BOTH, expand=True)
            
            for col in columnas:
                tree.heading(col, text=col)
                tree.column(col, width=100)
            
            # Mostrar primeras 20 filas
            for idx, row in df.head(20).iterrows():
                tree.insert("", tk.END, values=[str(row[col]) for col in columnas])
            
            ttk.Label(main_frame, text=f"Mostrando 20 de {len(df)} registros",
                     font=('Helvetica', 9), foreground='gray').pack(pady=(10, 0))
            
            btn_cerrar = tk.Button(main_frame, text="Cerrar", command=preview_win.destroy,
                                  bg="#3498db", fg="white", cursor='hand2')
            btn_cerrar.pack(pady=10)
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al leer el archivo: {str(e)}")
    
    def limpiar(self):
        """Limpia los resultados"""
        for item in self.tree_resultados.get_children():
            self.tree_resultados.delete(item)
        self.ruta_archivo.set("")
    
    def normalizar_texto(self, valor):
        """Normaliza texto para comparación"""
        if pd.isna(valor):
            return None
        return str(valor).upper().strip()
    
    def limpiar_cedula(self, cedula):
        """Limpia el formato de cédula"""
        if pd.isna(cedula):
            return None
        cedula_str = str(cedula).strip()
        cedula_str = cedula_str.replace('.', '')
        return re.sub(r'[^0-9]', '', cedula_str)
    
    def limpiar_telefono(self, telefono):
        """Limpia el formato de teléfono"""
        if pd.isna(telefono):
            return None
        telefono_str = str(telefono).strip()
        digitos = re.sub(r'[^0-9]', '', telefono_str)
        
        if len(digitos) == 11 and digitos.startswith('0'):
            return digitos
        if len(digitos) == 10 and not digitos.startswith('0'):
            if digitos.startswith('4'):
                return '0' + digitos
        if len(digitos) == 10 and digitos.startswith('0'):
            return digitos
        return digitos if len(digitos) >= 7 else None
    
    def limpiar_fecha(self, fecha):
        """Limpia y convierte fecha"""
        if pd.isna(fecha):
            return None
        try:
            if isinstance(fecha, str):
                # Intentar diferentes formatos
                for fmt in ['%Y-%m-%d', '%d/%m/%Y', '%d-%m-%Y']:
                    try:
                        return datetime.strptime(fecha, fmt).date()
                    except:
                        continue
            elif isinstance(fecha, datetime):
                return fecha.date()
            elif isinstance(fecha, pd.Timestamp):
                return fecha.date()
        except:
            pass
        return None
    
    def mapear_valor(self, valor, mapa, nombre_campo):
        """Mapea un valor a su ID usando el diccionario de mapeo"""
        if pd.isna(valor) or not str(valor).strip():
            return None
        
        valor_norm = self.normalizar_texto(valor)
        
        # Buscar coincidencia exacta
        if valor_norm in mapa:
            return mapa[valor_norm]
        
        # Buscar coincidencia parcial
        for key, value in mapa.items():
            if valor_norm in key or key in valor_norm:
                return value
        
        return None
    
    def importar(self):
        """Importa los datos del archivo Excel"""
        ruta = self.ruta_archivo.get().strip()
        if not ruta:
            messagebox.showwarning("Advertencia", "Seleccione un archivo Excel primero")
            return
        
        # Limpiar resultados anteriores
        self.limpiar()
        
        # Iniciar barra de progreso
        self.progress.start()
        
        try:
            # Leer Excel
            df = pd.read_excel(ruta)
            df.columns = [str(col).replace('\n', ' ').strip().upper() for col in df.columns]
            
            # Mapeo de columnas esperadas
            col_cedula = next((c for c in df.columns if 'CEDULA' in c), None)
            col_nombres = next((c for c in df.columns if 'NOMBRES' in c or 'APELLIDOS' in c), None)
            col_cargo = next((c for c in df.columns if 'CARGO' in c and 'TIPO' not in c), None)
            col_tipo_personal = next((c for c in df.columns if 'TIPO DE PERSONAL' in c or 'TIPO_PERSONAL' in c), None)
            col_nomina = next((c for c in df.columns if 'NOMINA' in c), None)
            col_nucleo = next((c for c in df.columns if 'NUCLEO' in c or 'SEDE' in c), None)
            col_parroquia = next((c for c in df.columns if 'PARROQUIA' in c), None)
            col_telefono = next((c for c in df.columns if 'TELEFONO' in c), None)
            col_email = next((c for c in df.columns if 'EMAIL' in c or 'CORREO' in c), None)
            col_fecha_nac = next((c for c in df.columns if 'FECHA DE NACIMIENTO' in c or 'FECHA_NAC' in c), None)
            col_fecha_ingreso = next((c for c in df.columns if 'FECHA DE INGRESO' in c or 'FECHA_INGRESO' in c), None)
            col_cuenta = next((c for c in df.columns if 'CUENTA' in c or 'NUMERO_CUENTA' in c), None)
            
            if not col_cedula or not col_nombres:
                messagebox.showerror("Error", "El archivo debe contener al menos las columnas: CEDULA y NOMBRES")
                self.progress.stop()
                return
            
            # Estadísticas
            total = len(df)
            exitosos = 0
            errores = 0
            actualizados = 0
            
            # Procesar cada fila
            for idx, row in df.iterrows():
                try:
                    cedula = self.limpiar_cedula(row[col_cedula])
                    if not cedula:
                        self.agregar_resultado("❌ Error", "N/A", "Sin cédula", "Cédula inválida o vacía", 'error')
                        errores += 1
                        continue
                    
                    nombres = self.normalizar_texto(row[col_nombres]) if pd.notna(row[col_nombres]) else None
                    if not nombres:
                        self.agregar_resultado("❌ Error", cedula, "N/A", "Nombres vacíos", 'error')
                        errores += 1
                        continue
                    
                    # Verificar si ya existe
                    existente = Queries.buscar_empleado(cedula=cedula)
                    
                    if existente and not self.actualizar_existentes.get():
                        self.agregar_resultado("⚠️ Omitido", cedula, nombres, "Cédula ya existe (omitido)", 'advertencia')
                        errores += 1
                        continue
                    
                    # Obtener IDs de mapeo
                    id_cargo = self.mapear_valor(row[col_cargo] if col_cargo else None, self.cargos, "cargo")
                    id_tipo_personal = self.mapear_valor(row[col_tipo_personal] if col_tipo_personal else None, self.tipos_personal, "tipo personal")
                    id_tipo_nomina = self.mapear_valor(row[col_nomina] if col_nomina else None, self.tipos_nomina, "tipo nómina")
                    id_nucleo = self.mapear_valor(row[col_nucleo] if col_nucleo else None, self.zonas_residencia, "núcleo")
                    id_parroquia = self.mapear_valor(row[col_parroquia] if col_parroquia else None, self.parroquias, "parroquia")
                    
                    # Limpiar datos
                    telefono = self.limpiar_telefono(row[col_telefono] if col_telefono else None)
                    email = self.normalizar_texto(row[col_email] if col_email else None)
                    fecha_nac = self.limpiar_fecha(row[col_fecha_nac] if col_fecha_nac else None)
                    fecha_ingreso = self.limpiar_fecha(row[col_fecha_ingreso] if col_fecha_ingreso else None)
                    numero_cuenta = self.limpiar_cedula(row[col_cuenta] if col_cuenta else None)
                    
                    # Calcular edad
                    edad = None
                    if fecha_nac:
                        hoy = datetime.now().date()
                        edad = hoy.year - fecha_nac.year
                        if hoy.month < fecha_nac.month or (hoy.month == fecha_nac.month and hoy.day < fecha_nac.day):
                            edad -= 1
                    
                    # Preparar datos
                    datos = (
                        'ACTIVO',                           # estatus
                        nombres,                            # nombres_apellidos
                        cedula,                             # cedula
                        'V',                                # nacionalidad
                        numero_cuenta,                      # numero_cuenta
                        id_tipo_nomina,                     # id_tipo_nomina
                        fecha_nac,                          # fecha_nacimiento
                        edad,                               # edad
                        None,                               # sexo
                        None,                               # estado_civil
                        None,                               # tipo_sangre
                        0, 0, 0, 0,                        # hijos
                        None,                               # nivel_academico
                        id_nucleo,                          # id_nucleo
                        None,                               # sector
                        telefono,                           # telefono
                        email,                              # correo_electronico
                        None,                               # condicion
                        False,                              # usa_lentes
                        None, None, None,                   # tallas
                        id_cargo,                           # id_cargo
                        None, None,                         # area, grupo
                        id_tipo_personal,                   # id_tipo_personal
                        id_parroquia,                       # id_parroquia
                        fecha_ingreso                       # fecha_ingreso
                    )
                    
                    if existente and self.actualizar_existentes.get():
                        # Actualizar empleado existente
                        empleado_id = existente[0][0]
                        Queries.actualizar_empleado(empleado_id, datos)
                        self.agregar_resultado("✅ Actualizado", cedula, nombres, "Datos actualizados correctamente", 'exito')
                        actualizados += 1
                    else:
                        # Insertar nuevo empleado
                        Queries.insertar_empleado(datos)
                        self.agregar_resultado("✅ Éxito", cedula, nombres, "Importado correctamente", 'exito')
                    
                    exitosos += 1
                    
                except Exception as e:
                    self.agregar_resultado("❌ Error", cedula if 'cedula' in locals() else "N/A", 
                                          nombres if 'nombres' in locals() else "N/A", 
                                          str(e)[:100], 'error')
                    errores += 1
            
            # Mostrar resumen
            self.progress.stop()
            
            resumen = f"""
            ========== RESUMEN DE IMPORTACIÓN ==========
            📊 Total registros procesados: {total}
            ✅ Importados exitosamente: {exitosos}
            🔄 Actualizados: {actualizados}
            ❌ Errores: {errores}
            ==========================================
            """
            
            messagebox.showinfo("Importación Completada", resumen)
            
            # Actualizar estadísticas en la ventana principal
            if self.callback_actualizar:
                self.callback_actualizar()
            
        except Exception as e:
            self.progress.stop()
            messagebox.showerror("Error", f"Error durante la importación: {str(e)}")
    
    def agregar_resultado(self, estado, cedula, nombres, mensaje, tag):
        """Agrega un resultado al treeview"""
        self.tree_resultados.insert("", tk.END, values=(estado, cedula, nombres, mensaje), tags=(tag,))
        self.tree_resultados.yview_moveto(1)  # Auto-scroll al final
        self.ventana.update_idletasks()


# Clase para generar plantilla de Excel
class GenerarPlantilla:
    """Genera una plantilla de Excel para carga masiva"""
    
    @staticmethod
    def generar():
        archivo = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")],
            initialfile="plantilla_carga_personal.xlsx"
        )
        
        if archivo:
            # Crear DataFrame con columnas de ejemplo
            plantilla = pd.DataFrame({
                'CEDULA': ['12345678', '87654321'],
                'NOMBRES Y APELLIDOS': ['JUAN PEREZ', 'MARIA GONZALEZ'],
                'CARGO': ['ADMINISTRATIVO', 'CHOFER'],
                'TIPO DE PERSONAL': ['ADMINISTRATIVO', 'OPERATIVO'],
                'TIPO DE NOMINA': ['SUPRA - ACTIVOS', 'FORANEOS SEDE'],
                'NUCLEO': ['SANFELIX', 'PUERTOORDAZ'],
                'PARROQUIA': ['DALLA COSTA', 'SIMON BOLIVAR'],
                'TELEFONO': ['04123456789', '04129876543'],
                'EMAIL': ['juan@example.com', 'maria@example.com'],
                'FECHA DE NACIMIENTO': ['1990-01-01', '1985-05-15'],
                'FECHA DE INGRESO': ['2020-01-01', '2021-06-01'],
                'NUMERO DE CUENTA': ['01020012345678901234', '01020098765432109876']
            })
            
            # Crear una segunda hoja con instrucciones
            instrucciones = pd.DataFrame({
                'Instrucción': [
                    '1. Complete los datos en la hoja "Datos"',
                    '2. No modifique los nombres de las columnas',
                    '3. La cédula es obligatoria y debe ser única',
                    '4. Los nombres son obligatorios',
                    '5. El número de cuenta debe tener 20 dígitos',
                    '6. Las fechas deben tener formato YYYY-MM-DD',
                    '7. Los valores de CARGO, TIPO DE PERSONAL, etc., deben coincidir con los existentes en el sistema',
                    '8. Puede eliminar las filas de ejemplo'
                ],
                'Valores válidos': [
                    '-',
                    '-',
                    'Solo números, 6-8 dígitos',
                    '-',
                    'Exactamente 20 dígitos numéricos',
                    'Ejemplo: 1990-05-15',
                    'Verificar en la configuración del sistema',
                    '-'
                ]
            })
            
            with pd.ExcelWriter(archivo, engine='openpyxl') as writer:
                plantilla.to_excel(writer, sheet_name="Datos", index=False)
                instrucciones.to_excel(writer, sheet_name="Instrucciones", index=False)
            
            messagebox.showinfo("Éxito", f"Plantilla generada correctamente en:\n{archivo}")