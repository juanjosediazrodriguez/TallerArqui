# Imagen base: Python 3.11 en versión slim (más liviana, sin extras innecesarios)
FROM python:3.11-slim

# Directorio de trabajo dentro del contenedor
WORKDIR /app

# Primero copiamos solo requirements.txt para aprovechar el cache de capas de Docker.
# Si el código cambia pero las dependencias no, Docker no reinstala todo.
COPY requirements.txt .

# Instalar dependencias sin guardar cache de pip (reduce tamaño de imagen)
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto del código fuente al contenedor
COPY . .

# Crear el directorio de datos para la base de datos SQLite
RUN mkdir -p /app/data

# Exponer el puerto 8000 (donde correrá FastAPI)
EXPOSE 8000

# Comando por defecto al iniciar el contenedor
# --host 0.0.0.0 hace que la app sea accesible desde fuera del contenedor
CMD ["uvicorn", "src.infrastructure.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
