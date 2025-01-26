# Sistema de inventario en Python con interfaz gráfica

Este es un sistema de gestión de inventario desarrollado en Python, utilizando una interfaz gráfica con Tkinter. El sistema se conecta a una base de datos **MySQL** para almacenar los productos.

## Funcionalidades

- **Agregar productos al inventario**: introduce productos con su nombre, stock y precio.
- **Mostrar inventario completo**: visualiza todos los productos en el inventario.
- **Buscar productos por nombre**: encuentra productos rápidamente a través de su nombre.
- **Editar stock o precio**: actualiza la cantidad o el precio de los productos existentes.
- **Eliminar productos**: borra productos específicos del inventario.
- **Vaciar inventario**: elimina todos los productos del inventario.
- **Generar reportes de productos con bajo stock**: filtra los productos con stock bajo y muestra un reporte.

## Requisitos

- **Python 3.8 o superior**
- **MySQL** (para la base de datos)
- **Biblioteca mysql-connector-python** (para interactuar con MySQL)
- **Tkinter** (incluida con Python)

## Pasos para ejecutar el proyecto:

1. **Clona este repositorio**:
`git clone https://github.com/maveggia/inventario-python-con-interfaz.git'`

2. **Instala las dependencias necesarias**: puedes instalar la biblioteca MySQL directamente ejecutando:
   `pip install mysql-connector-python`

3. **Configura la base de datos MySQL**: crea la base de datos "inventario" en MySQL ejecutando el siguiente comando:
   `CREATE DATABASE inventario;`

4. **Ejecuta el archivo SQL para crear la tabla y agregar productos**: en la carpeta `scripts/`, encontrarás el archivo `inventario.sql`, que contiene la estructura de la base de datos y algunos productos iniciales. Ejecútalo en MySQL para configurarlo:
   `mysql -u root -p inventario < scripts/inventario.sql`

5. **Ejecuta el archivo Python**: una vez configurada la base de datos, puedes ejecutar el archivo `InventarioConInterfaz.py` para iniciar la aplicación:
   `python InventarioConInterfaz.py`

## Autor

Matias Alvarez Veggia  
[LinkedIn](https://www.linkedin.com/in/matias-alvarez-veggia)