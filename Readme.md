# Django Project

Este proyecto utiliza el framework Django para construir aplicaciones web robustas y escalables.

## Requisitos

- Python 3.x
- Django
- Virtualenv (opcional pero recomendado)
- PostgreSQL
- Redis (necesariamente debe estar corriendo)

## Instalación

1. Clona este repositorio:
    ```bash
    git clone https://github.com/BauGuden/django-redis
    ```

2. Crea y activa un entorno virtual:
    ```bash
    python -m venv venv
    source venv/bin/activate  # En Windows: venv\Scripts\activate
    ```

3. Instala las dependencias:
    ```bash
    python.exe -m pip install --upgrade pip
    pip install -r requirements.txt
    ```

4. Asegúrate de que Redis esté corriendo en tu sistema.

5. Crea la base de datos en PostgreSQL:
    ```sql
    CREATE DATABASE BDREDIS;
    ```

6. Realiza las migraciones:
    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

7. Inicia el servidor de desarrollo:
    ```bash
    python manage.py runserver
    ```

## Uso

Accede a la aplicación en tu navegador en [http://127.0.0.1:8000](http://127.0.0.1:8000).

## Estructura del Proyecto

- **app/**: Contiene las aplicaciones de Django.
- **templates/**: Archivos HTML para las vistas.
- **static/**: Archivos estáticos como CSS, JavaScript e imágenes.

## Contribuciones

¡Las contribuciones son bienvenidas! Por favor, abre un issue o envía un pull request.

## Licencia

Este proyecto está bajo la licencia [MIT](LICENSE).
