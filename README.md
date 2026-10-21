# Gestor-ventas-inventario
Organizador de ventas e inventario para PYMEs locales

---

## Requisitos previos 

Instrucciones de instalación y ejecución local:

1. **Clonar el repositorio:**

- En bash

git clone https://github.com/BsMarih/gestor-ventas-inventario.git
cd gestor-ventas-inventario

2. **Crear y activar entorno virtual:**

- En windows:

python -m venv venv
venv\Scripts\activate

- En macOS/Linux:

python3 -m venv venv
source venv/bin/activate

3. **Instalar necesarios para el proyecto:**

- Instalar dependencias necesarias:

pip install -r requirements.txt

- Migraciones de la base de datos:

python manage.py makemigrations
python manage.py migrate

4. **Iniciar el servidor de desarrollo**

python manage.py runserver

- Acceder a la aplicación ingresando la direccion local.

---


