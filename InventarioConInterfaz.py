import sqlite3
import tkinter as tk
from tkinter import messagebox, ttk, simpledialog

# Conexión a la base de datos
conexion = sqlite3.connect("inventario.db")
cursor = conexion.cursor()

# Creación de la tabla "productos"
cursor.execute("""
CREATE TABLE IF NOT EXISTS productos(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    stock INTEGER NOT NULL,
    precio REAL NOT NULL
)
""")
conexion.commit()

def agregar_producto(nombre, stock, precio):
    cursor.execute("INSERT INTO productos (nombre, stock, precio) VALUES (?, ?, ?)", (nombre, stock, precio))
    conexion.commit()
    messagebox.showinfo("Éxito", "Producto agregado con éxito")

def obtener_inventario():
    cursor.execute("SELECT * FROM productos")
    return cursor.fetchall()

def editar_stock(id_producto, nuevo_stock):
    cursor.execute("UPDATE productos SET stock = ? WHERE id = ?", (nuevo_stock, id_producto))
    conexion.commit()

def editar_precio(id_producto, nuevo_precio):
    cursor.execute("UPDATE productos SET precio = ? WHERE id = ?", (nuevo_precio, id_producto))
    conexion.commit()

def eliminar_producto(id_producto):
    cursor.execute("DELETE FROM productos WHERE id = ?", (id_producto,))
    conexion.commit()

def vaciar_inventario():
    cursor.execute("DELETE FROM productos")
    conexion.commit()

def buscar_producto(nombre):
    cursor.execute("SELECT * FROM productos WHERE nombre LIKE ?", (f"%{nombre}%",))
    return cursor.fetchall()

def productos_bajo_stock(limite):
    cursor.execute("SELECT * FROM productos WHERE stock <= ?", (limite,))
    return cursor.fetchall()

# Crear interfaz gráfica con tkinter
class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Inventario")
        self.root.geometry("1024x768")  # Tamaño ajustado a pantalla completa

        # Estilo para la aplicación
        style = ttk.Style()
        style.configure("TButton", font=("Arial", 12), padding=10)
        style.configure("TLabel", font=("Arial", 14))  # Aumento del tamaño de la tipografía
        style.configure("TEntry", font=("Arial", 12), padding=10)
        style.configure("Treeview", font=("Arial", 12))
        style.configure("Treeview.Heading", font=("Arial", 14, "bold"))

        # Sección de agregar producto
        frame_superior = tk.Frame(root)
        frame_superior.grid(row=0, column=0, padx=20, pady=5, sticky="nw")

        # Campos de entrada para nombre, stock y precio
        tk.Label(frame_superior, text="Nombre del Producto:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.nombre_var = tk.StringVar()
        tk.Entry(frame_superior, textvariable=self.nombre_var, width=30, font=("Arial", 12)).grid(row=0, column=1, padx=10, pady=5)

        tk.Label(frame_superior, text="Stock:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.stock_var = tk.StringVar()
        tk.Entry(frame_superior, textvariable=self.stock_var, width=30, font=("Arial", 12)).grid(row=1, column=1, padx=10, pady=5)

        tk.Label(frame_superior, text="Precio:").grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.precio_var = tk.StringVar()
        tk.Entry(frame_superior, textvariable=self.precio_var, width=30, font=("Arial", 12)).grid(row=2, column=1, padx=10, pady=5)

        # Botón de "Agregar Producto", alineado con los campos
        ttk.Button(frame_superior, text="Agregar Producto", command=self.agregar_producto).grid(row=3, column=1, pady=10, sticky="w", padx=10)

        # Botones de acción al lado derecho
        frame_botones = tk.Frame(root)
        frame_botones.grid(row=0, column=1, padx=20, pady=5, sticky="ne")

        boton_ancho = 15
        ttk.Button(frame_botones, text="Editar Stock", command=self.editar_stock, width=boton_ancho).grid(row=0, column=0, padx=5, pady=5)
        ttk.Button(frame_botones, text="Editar Precio", command=self.editar_precio, width=boton_ancho).grid(row=0, column=1, padx=5, pady=5)
        ttk.Button(frame_botones, text="Eliminar Producto", command=self.eliminar_producto, width=boton_ancho).grid(row=0, column=2, padx=5, pady=5)

        # Segunda fila de botones
        ttk.Button(frame_botones, text="Buscar Producto", command=self.buscar_producto, width=boton_ancho).grid(row=1, column=0, padx=5, pady=5)
        ttk.Button(frame_botones, text="Reporte Bajo Stock", command=self.reporte_bajo_stock, width=boton_ancho).grid(row=1, column=1, padx=5, pady=5)
        ttk.Button(frame_botones, text="Vaciar Inventario", command=self.vaciar_inventario, width=boton_ancho).grid(row=1, column=2, padx=5, pady=5)

        # Tabla de inventario
        self.tree = ttk.Treeview(root, columns=("id", "nombre", "stock", "precio"), show="headings")
        self.tree.heading("id", text="ID")
        self.tree.heading("nombre", text="Nombre")
        self.tree.heading("stock", text="Stock")
        self.tree.heading("precio", text="Precio")
        self.tree.grid(row=2, column=0, columnspan=7, pady=20, padx=20, sticky="nsew")

        # Habilitar selección múltiple
        self.tree.config(selectmode="extended")

        # Expansión de la tabla para ocupar el espacio disponible
        root.grid_rowconfigure(2, weight=1)
        root.grid_columnconfigure(1, weight=1)

        # Limpiar resaltado cuando se hace clic fuera
        self.tree.bind("<Button-1>", self.limpiar_resaltado)

        self.mostrar_inventario()

    def agregar_producto(self):
        nombre = self.nombre_var.get()
        stock = self.stock_var.get()
        precio = self.precio_var.get()

        # Validación de stock y precio
        if not stock.isdigit() or not precio.replace('.', '', 1).isdigit():
            messagebox.showerror("Error", "Ingrese un stock y precio válido")
            return

        if not nombre:
            messagebox.showerror("Error", "El nombre del producto no puede estar vacío")
            return

        agregar_producto(nombre, int(stock), float(precio))
        self.nombre_var.set("")
        self.stock_var.set("")
        self.precio_var.set("")
        self.mostrar_inventario()

    def mostrar_inventario(self):
        # Limpiar la tabla actual
        for item in self.tree.get_children():
            self.tree.delete(item)
        productos = obtener_inventario()
        for producto in productos:
            self.tree.insert("", "end", values=producto)

    def editar_stock(self):
        seleccionado = self.tree.selection()
        if seleccionado:
            nuevo_stock = simpledialog.askinteger("Editar Stock", "Nuevo stock:")
            if nuevo_stock is not None:
                for item in seleccionado:
                    id_producto = self.tree.item(item)['values'][0]
                    editar_stock(id_producto, nuevo_stock)
                self.mostrar_inventario()
        else:
            messagebox.showerror("Error", "Seleccione un producto")

    def editar_precio(self):
        seleccionado = self.tree.selection()
        if seleccionado:
            nuevo_precio = simpledialog.askfloat("Editar Precio", "Nuevo precio:")
            if nuevo_precio is not None:
                for item in seleccionado:
                    id_producto = self.tree.item(item)['values'][0]
                    editar_precio(id_producto, nuevo_precio)
                self.mostrar_inventario()
        else:
            messagebox.showerror("Error", "Seleccione un producto")

    def eliminar_producto(self):
        seleccionado = self.tree.selection()
        if seleccionado:
            confirmar = messagebox.askyesno("Confirmar", "¿Desea eliminar el producto seleccionado?")
            if confirmar:
                for item in seleccionado:
                    id_producto = self.tree.item(item)['values'][0]
                    eliminar_producto(id_producto)
                self.mostrar_inventario()
        else:
            messagebox.showerror("Error", "Seleccione un producto")

    def vaciar_inventario(self):
        confirmar = messagebox.askyesno("Confirmar", "¿Desea vaciar el inventario completo?")
        if confirmar:
            vaciar_inventario()
            self.mostrar_inventario()

    def buscar_producto(self):
        nombre = simpledialog.askstring("Buscar Producto", "Ingrese el nombre del producto:")
        if nombre:
            resultados = buscar_producto(nombre)
            if resultados:
                # Resaltar productos encontrados
                for item in self.tree.get_children():
                    self.tree.item(item, tags=())  # Limpiar cualquier resalte previo

                for producto in resultados:
                    # Resaltar los productos encontrados
                    for item in self.tree.get_children():
                        if self.tree.item(item)['values'][1] == producto[1]:
                            self.tree.item(item, tags=('highlight',))

                self.tree.tag_configure('highlight', background='yellow')

                messagebox.showinfo("Resultados", "\n".join([f"ID: {r[0]} - Nombre: {r[1]} - Stock: {r[2]} - Precio: {r[3]}" for r in resultados]))
            else:
                messagebox.showinfo("Sin Resultados", "No se encontraron productos.")

    def reporte_bajo_stock(self):
        limite = simpledialog.askinteger("Reporte Bajo Stock", "Ingrese el límite de stock:")
        if limite is not None:
            productos_bajos = productos_bajo_stock(limite)
            if productos_bajos:
                # Limpiar cualquier resaltado previo
                for item in self.tree.get_children():
                    self.tree.item(item, tags=())  

                # Resaltar los productos con bajo stock
                for producto in productos_bajos:
                    for item in self.tree.get_children():
                        if self.tree.item(item)['values'][0] == producto[0]:
                            self.tree.item(item, tags=('highlight',))

                self.tree.tag_configure('highlight', background='yellow')

                messagebox.showinfo("Productos Bajo Stock", "\n".join([f"ID: {r[0]} - Nombre: {r[1]} - Stock: {r[2]} - Precio: {r[3]}" for r in productos_bajos]))
            else:
                messagebox.showinfo("Sin Productos Bajo Stock", "No hay productos con stock bajo.")

    def limpiar_resaltado(self, event):
        # Limpiar resaltado cuando se hace clic fuera
        for item in self.tree.get_children():
            self.tree.item(item, tags=())

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
