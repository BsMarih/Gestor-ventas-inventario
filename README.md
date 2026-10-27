# Gestor-ventas-inventario
Organizador de ventas e inventario para PYMEs locales

---

## Requisitos previos 

Instrucciones de instalación y ejecución local:

1. **Clonar el repositorio:**

En la Terminal:

```bash 
git clone https://github.com/BsMarih/gestor-ventas-inventario.git
cd gestor-ventas-inventario
```

2. **Crear y activar entorno virtual:**

En windows:

```bash
python -m venv venv
venv\Scripts\activate
```

En macOS/Linux:

```bash
python3 -m venv venv
source venv/bin/activate
```

3. **Instalar necesarios para el proyecto:**

- Instalar dependencias necesarias:

```bash
pip install -r requirements.txt
```

- Migraciones de la base de datos:

```bash
python manage.py makemigrations
python manage.py migrate
```

4. **Iniciar el servidor de desarrollo**

```bash
python manage.py runserver
```
Acceder a la aplicación ingresando la direccion local.

---


