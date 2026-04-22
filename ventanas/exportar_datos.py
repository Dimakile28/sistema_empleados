import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import pandas as pd
from datetime import datetime
from database.conexion import db
from database.queries import Queries

class VentanaExportar:
    """Ventana para exportar datos con orden personalizado"""
    
    def __init__(self, parent):
        self.parent = parent
        
        self.ventana = tk.Toplevel(parent)
        self.ventana.title("Exportar Datos")
        self.ventana.geometry("800x650")
        self.ventana.transient(parent)
        self.ventana.grab_set()
        
        self.centrar_ventana()
        self.crear_interfaz()
    
    def centrar_ventana(self):
        self.ventana.update_idletasks()
        ancho = 800
        alto = 650
        x = (self.ventana.winfo_screenwidth() // 2) - (ancho // 2)
        y = (self.ventana.winfo_screenheight() // 2) - (alto // 2)
        self.ventana.geometry(f'{ancho}x{alto}+{x}+{y}')
    
    def crear_interfaz(self):
        main_frame = ttk.Frame(self.ventana, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        titulo = ttk.Label(main_frame, text="Exportar Datos del Personal",
                          font=('Helvetica', 14, 'bold'))
        titulo.pack(pady=(0, 10))
        
        subtitulo = ttk.Label(main_frame, text="Seleccione los campos y ordénelos según prefiera",
                             font=('Helvetica', 10), foreground='gray')
        subtitulo.pack(pady=(0, 20))
        
        # Frame para opciones de formato
        options_frame = ttk.LabelFrame(main_frame, text="Formato de Exportación", padding="10")
        options_frame.pack(fill=tk.X, pady=(0, 15))
        
        self.formato = tk.StringVar(value="excel")
        rb_excel = ttk.Radiobutton(options_frame, text="Excel (.xlsx)", 
                                   variable=self.formato, value="excel")
        rb_excel.pack(anchor='w', pady=5)
        
        rb_csv = ttk.Radiobutton(options_frame, text="CSV (.csv)", 
                                 variable=self.formato, value="csv")
        rb_csv.pack(anchor='w', pady=5)
        
        # Frame para orden de campos
        orden_frame = ttk.LabelFrame(main_frame, text="Orden de Columnas", padding="10")
        orden_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 15))
        
        # Frame para lista de campos disponibles
        campos_disponibles_frame = ttk.Frame(orden_frame)
        campos_disponibles_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        ttk.Label(campos_disponibles_frame, text="Campos Disponibles:", 
                 font=('Helvetica', 10, 'bold')).pack(anchor='w')
        
        # Lista de campos disponibles
        scroll_disponibles = ttk.Scrollbar(campos_disponibles_frame)
        self.lista_disponibles = tk.Listbox(campos_disponibles_frame, 
                                            yscrollcommand=scroll_disponibles.set,
                                            selectmode=tk.EXTENDED, height=15)
        scroll_disponibles.config(command=self.lista_disponibles.yview)
        scroll_disponibles.pack(side=tk.RIGHT, fill=tk.Y)
        self.lista_disponibles.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Botones de movimiento
        botones_frame = ttk.Frame(orden_frame)
        botones_frame.pack(side=tk.LEFT, padx=10)
        
        btn_derecha = tk.Button(botones_frame, text="→", command=self.mover_a_seleccionados,
                               width=5, bg="#3498db", fg="white", font=('Helvetica', 12),
                               cursor='hand2')
        btn_derecha.pack(pady=5)
        
        btn_derecha_todos = tk.Button(botones_frame, text="→→", command=self.mover_todos_a_seleccionados,
                                     width=5, bg="#3498db", fg="white", font=('Helvetica', 12),
                                     cursor='hand2')
        btn_derecha_todos.pack(pady=5)
        
        btn_izquierda = tk.Button(botones_frame, text="←", command=self.mover_a_disponibles,
                                 width=5, bg="#e74c3c", fg="white", font=('Helvetica', 12),
                                 cursor='hand2')
        btn_izquierda.pack(pady=5)
        
        btn_izquierda_todos = tk.Button(botones_frame, text="←←", command=self.mover_todos_a_disponibles,
                                       width=5, bg="#e74c3c", fg="white", font=('Helvetica', 12),
                                       cursor='hand2')
        btn_izquierda_todos.pack(pady=5)
        
        # Botones de orden
        btn_subir = tk.Button(botones_frame, text="↑", command=self.subir_seleccionado,
                             width=5, bg="#f39c12", fg="white", font=('Helvetica', 12),
                             cursor='hand2')
        btn_subir.pack(pady=5)
        
        btn_bajar = tk.Button(botones_frame, text="↓", command=self.bajar_seleccionado,
                             width=5, bg="#f39c12", fg="white", font=('Helvetica', 12),
                             cursor='hand2')
        btn_bajar.pack(pady=5)
        
        # Frame para lista de campos seleccionados
        campos_seleccionados_frame = ttk.Frame(orden_frame)
        campos_seleccionados_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        ttk.Label(campos_seleccionados_frame, text="Campos Seleccionados (orden de aparición):", 
                 font=('Helvetica', 10, 'bold')).pack(anchor='w')
        
        # Lista de campos seleccionados
        scroll_seleccionados = ttk.Scrollbar(campos_seleccionados_frame)
        self.lista_seleccionados = tk.Listbox(campos_seleccionados_frame, 
                                              yscrollcommand=scroll_seleccionados.set,
                                              selectmode=tk.SINGLE, height=15)
        scroll_seleccionados.config(command=self.lista_seleccionados.yview)
        scroll_seleccionados.pack(side=tk.RIGHT, fill=tk.Y)
        self.lista_seleccionados.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Cargar campos disponibles
        self.cargar_campos_disponibles()
        
        # Seleccionar todos por defecto
        self.mover_todos_a_seleccionados()
        
        # Botones de acción
        action_frame = ttk.Frame(main_frame)
        action_frame.pack(fill=tk.X, pady=10)
        
        btn_exportar = tk.Button(action_frame, text="📊 Exportar", command=self.exportar,
                                bg="#9b59b6", fg="white", font=('Helvetica', 11),
                                padx=20, pady=5, cursor='hand2')
        btn_exportar.pack(side=tk.LEFT, padx=5)
        
        btn_cancelar = tk.Button(action_frame, text="❌ Cancelar", command=self.ventana.destroy,
                                bg="#e74c3c", fg="white", cursor='hand2')
        btn_cancelar.pack(side=tk.RIGHT, padx=5)
    
    def cargar_campos_disponibles(self):
        """Carga la lista de campos disponibles para exportar"""
        self.campos_disponibles = [
            "Cédula", "Nombres", "Estatus", "Cargo", "Tipo Personal", "Nómina",
            "Núcleo", "Parroquia", "Teléfono", "Email", "Número de Cuenta",
            "Fecha Nacimiento", "Edad", "Sexo", "Estado Civil", "Tipo Sangre", 
            "Cantidad Hijos", "Nivel Académico", "Sector", "Condición Médica", 
            "Usa Lentes", "Talla Calzado", "Talla Pantalón", "Talla Camisa", 
            "Área", "Grupo", "Fecha Ingreso"
        ]
        
        for campo in self.campos_disponibles:
            self.lista_disponibles.insert(tk.END, campo)
    
    def mover_a_seleccionados(self):
        """Mueve los campos seleccionados de disponibles a seleccionados"""
        seleccionados = self.lista_disponibles.curselection()
        # Mover en orden inverso para no afectar índices
        for idx in reversed(seleccionados):
            campo = self.lista_disponibles.get(idx)
            self.lista_disponibles.delete(idx)
            self.lista_seleccionados.insert(tk.END, campo)
    
    def mover_todos_a_seleccionados(self):
        """Mueve todos los campos disponibles a seleccionados"""
        while self.lista_disponibles.size() > 0:
            campo = self.lista_disponibles.get(0)
            self.lista_disponibles.delete(0)
            self.lista_seleccionados.insert(tk.END, campo)
    
    def mover_a_disponibles(self):
        """Mueve los campos seleccionados de seleccionados a disponibles"""
        seleccionados = self.lista_seleccionados.curselection()
        for idx in reversed(seleccionados):
            campo = self.lista_seleccionados.get(idx)
            self.lista_seleccionados.delete(idx)
            # Insertar en orden alfabético en disponibles
            pos = 0
            while pos < self.lista_disponibles.size() and self.lista_disponibles.get(pos) < campo:
                pos += 1
            self.lista_disponibles.insert(pos, campo)
    
    def mover_todos_a_disponibles(self):
        """Mueve todos los campos seleccionados a disponibles"""
        while self.lista_seleccionados.size() > 0:
            campo = self.lista_seleccionados.get(0)
            self.lista_seleccionados.delete(0)
            # Insertar en orden alfabético en disponibles
            pos = 0
            while pos < self.lista_disponibles.size() and self.lista_disponibles.get(pos) < campo:
                pos += 1
            self.lista_disponibles.insert(pos, campo)
    
    def subir_seleccionado(self):
        """Sube de posición el campo seleccionado en la lista de seleccionados"""
        seleccion = self.lista_seleccionados.curselection()
        if seleccion and seleccion[0] > 0:
            idx = seleccion[0]
            campo = self.lista_seleccionados.get(idx)
            self.lista_seleccionados.delete(idx)
            self.lista_seleccionados.insert(idx - 1, campo)
            self.lista_seleccionados.selection_set(idx - 1)
    
    def bajar_seleccionado(self):
        """Baja de posición el campo seleccionado en la lista de seleccionados"""
        seleccion = self.lista_seleccionados.curselection()
        if seleccion and seleccion[0] < self.lista_seleccionados.size() - 1:
            idx = seleccion[0]
            campo = self.lista_seleccionados.get(idx)
            self.lista_seleccionados.delete(idx)
            self.lista_seleccionados.insert(idx + 1, campo)
            self.lista_seleccionados.selection_set(idx + 1)
    
    def exportar(self):
        """Exporta los datos según las opciones seleccionadas"""
        
        # Verificar que haya al menos un campo seleccionado
        if self.lista_seleccionados.size() == 0:
            messagebox.showwarning("Advertencia", "Seleccione al menos un campo para exportar")
            return
        
        # Obtener el orden de los campos seleccionados
        columnas_seleccionadas = []
        for i in range(self.lista_seleccionados.size()):
            columnas_seleccionadas.append(self.lista_seleccionados.get(i))
        
        # Obtener datos
        datos = Queries.obtener_todos_empleados()
        
        if not datos:
            messagebox.showwarning("Advertencia", "No hay datos para exportar")
            return
        
        # Mapeo de campos con índices
        mapeo_campos = {
            "Cédula": 0,
            "Nombres": 1,
            "Estatus": 2,
            "Cargo": 3,
            "Tipo Personal": 4,
            "Nómina": 5,
            "Núcleo": 6,
            "Parroquia": 7,
            "Teléfono": 8,
            "Email": 9,
            "Número de Cuenta": 25,
            "Fecha Nacimiento": 10,
            "Edad": 11,
            "Sexo": 12,
            "Estado Civil": 13,
            "Tipo Sangre": 14,
            "Cantidad Hijos": 15,
            "Nivel Académico": 16,
            "Sector": 17,
            "Condición Médica": 18,
            "Usa Lentes": 19,
            "Talla Calzado": 20,
            "Talla Pantalón": 21,
            "Talla Camisa": 22,
            "Área": 23,
            "Grupo": 24,
            "Fecha Ingreso": 26
        }
        
        # Crear DataFrame con campos seleccionados en el orden elegido
        indices_seleccionados = [mapeo_campos[campo] for campo in columnas_seleccionadas if campo in mapeo_campos]
        
        data_filtrada = []
        for row in datos:
            data_filtrada.append([row[i] if i < len(row) else "" for i in indices_seleccionados])
        
        df = pd.DataFrame(data_filtrada, columns=columnas_seleccionadas)
        
        # Seleccionar archivo de destino
        formato = self.formato.get()
        fecha_actual = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        if formato == "excel":
            archivo = filedialog.asksaveasfilename(
                defaultextension=".xlsx",
                filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")],
                initialfile=f"reporte_personal_{fecha_actual}.xlsx"
            )
            if archivo:
                with pd.ExcelWriter(archivo, engine='openpyxl') as writer:
                    df.to_excel(writer, sheet_name="Personal", index=False)
                    
                    # Hoja de resumen
                    resumen = pd.DataFrame({
                        'Métrica': ['Total Empleados', 'Fecha Exportación', 'Campos Exportados', 'Orden de Campos'],
                        'Valor': [len(df), fecha_actual, len(columnas_seleccionadas), ' → '.join(columnas_seleccionadas)]
                    })
                    resumen.to_excel(writer, sheet_name="Resumen", index=False)
                
                messagebox.showinfo("Éxito", f"Datos exportados correctamente a:\n{archivo}")
                self.ventana.destroy()
        else:
            archivo = filedialog.asksaveasfilename(
                defaultextension=".csv",
                filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
                initialfile=f"reporte_personal_{fecha_actual}.csv"
            )
            if archivo:
                df.to_csv(archivo, index=False, encoding='utf-8-sig')
                messagebox.showinfo("Éxito", f"Datos exportados correctamente a:\n{archivo}")
                self.ventana.destroy()


# Clase adicional para exportación rápida
class ExportarDatos:
    """Clase estática para exportar datos desde cualquier ventana"""
    
    @staticmethod
    def exportar_a_excel(datos, parent_ventana):
        """Exporta una lista de datos a Excel"""
        if not datos:
            messagebox.showwarning("Advertencia", "No hay datos para exportar", parent=parent_ventana)
            return
        
        archivo = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")],
            initialfile=f"reporte_personal_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
        )
        
        if archivo:
            df = pd.DataFrame(datos)
            df.to_excel(archivo, index=False)
            messagebox.showinfo("Éxito", f"Datos exportados a:\n{archivo}", parent=parent_ventana)