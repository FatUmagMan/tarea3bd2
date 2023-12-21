# Projecto 3 (backend)

## Contexto

Este proyecto implementa una API REST para un sistema de gestión de biblioteca.
Las tecnologías utilizadas son:

- Lenguaje de programación: Python (3.10+)
- Gestor de dependencias: PDM
- Framework web: Litestar
- Base de datos: PostgreSQL
- ORM: SQLAlchemy y Alembic (migraciones)

## ¿Cómo configurar el entorno para el proyecto?

1. Instala las dependencias del proyecto con PDM
   ```shell
   pdm install
   ```
2. Crea el archivo `.env` en la raíz del proyecto desde el ejemplo `env.example`
   ```shell
   cp env.example .env
   ```
   Configura la variable `DATABASE_URL` con la URL de la base de datos que desees utilizar (recordar que debe conservar
   el formato `postgresql+psycopg:///<mi_bd>`).
3. Crea la base de datos en postgresql.
   ```shell
   createdb <mi_bd>
   ```
   **NOTA:** En WSL podría ser necesario iniciar antes el servicio de postgres con `sudo service postgresql start`.
4. Ejecuta las migraciones
   ```shell
   pdm run alembic upgrade head
   ```
5. Ejecuta el servidor de desarrollo
   ```shell
   pdm start
   ```
6. Si no hay errores, la documentación de la API estará disponible en http://127.0.0.1:8000/schema/swagger/.

## ¿Cómo trabajar en el proyecto?

Por regla general el prodedimiento para realizar modificaciones a partir desde el modelo de datos es el siguiente:

1. Crear modificaciones en los modelos (`app/models.py`).
2. Crear una nueva migración con alembic
   ```shell
   pdm shell
   alembic revision --autogenerate -m "Descripción de la modificación"
   ```
3. Revisar la migración creada en `migrations/versions` y verificar que sea correcta.
   Se puede revisar también el código SQL de la migración ejecutando:
    ```shell
    alembic upgrade --sql head
    ```
4. Ejecutar la migración
   ```shell
   alembic upgrade head
   ``` 
5. Crear al menos una DTO para lectura en `app/dtos.py`.
6. Crear un repositorio para el nuevo modelo en `app/repositories.py`.
7. Crear un nuevo controlador en `app/controllers.py`.

Algunas modifaciones más específicas podrían no requerir de todos los pasos anteriores, pero en general es una buen
flujo de trabajo.

## Recomendaciones

- Utilizar el comando `pdm format` para formatear el código antes de hacer un commit.
- Probar las rutas de la API a través de la documentación luego de agregar o hacer modificaciones para verificar que
  todo esté funcionando correctamente.

## En caso de errores...

- Recuerda que en general la última línea de error es la más importante para identificar el problema.
- Si el error impide que parta el servidor de desarrollo, revisa que no haya errores de sintaxis en el código.