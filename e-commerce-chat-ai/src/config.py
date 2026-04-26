"""
Módulo de configuración global del proyecto.

Lee las variables de entorno del archivo .env y las expone
como una clase de configuración centralizada.
"""

import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """
    Clase de configuración global de la aplicación.

    Lee las variables de entorno y las provee como atributos de clase.
    Si una variable no está definida, usa valores por defecto seguros.

    Attributes:
        GEMINI_API_KEY (str): Clave de API para Google Gemini AI.
        DATABASE_URL (str): URL de conexión a la base de datos SQLite.
        ENVIRONMENT (str): Entorno de ejecución (development/production).
    """

    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL", "sqlite:///./data/ecommerce_chat.db"
    )
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
