"""
Módulo de modelos ORM de SQLAlchemy.

Define la estructura de las tablas de la base de datos como clases Python.
SQLAlchemy traduce estas clases a instrucciones SQL automáticamente.
"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, Text, DateTime, Index
from .database import Base


class ProductModel(Base):
    """
    Modelo ORM que representa la tabla 'products' en la base de datos.

    Cada instancia de esta clase corresponde a una fila en la tabla.
    SQLAlchemy se encarga de la traducción entre Python y SQL.

    Attributes:
        id (int): Clave primaria, se asigna automáticamente.
        name (str): Nombre del producto. Obligatorio.
        brand (str): Marca del producto.
        category (str): Categoría del producto.
        size (str): Talla del zapato.
        color (str): Color del producto.
        price (float): Precio del producto.
        stock (int): Unidades disponibles en inventario.
        description (str): Descripción detallada del producto.
    """

    __tablename__ = "products"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(200), nullable=False)
    brand = Column(String(100))
    category = Column(String(100))
    size = Column(String(20))
    color = Column(String(50))
    price = Column(Float)
    stock = Column(Integer)
    description = Column(Text)


class ChatMemoryModel(Base):
    """
    Modelo ORM que representa la tabla 'chat_memory' en la base de datos.

    Almacena el historial de mensajes de todas las sesiones de chat.
    El campo session_id agrupa los mensajes de cada usuario/conversación.

    Attributes:
        id (int): Clave primaria, se asigna automáticamente.
        session_id (str): Identificador de la sesión de conversación.
            Indexado para búsquedas rápidas por sesión.
        role (str): Rol del emisor: 'user' o 'assistant'.
        message (str): Contenido del mensaje.
        timestamp (datetime): Fecha y hora del mensaje. Por defecto: ahora.
    """

    __tablename__ = "chat_memory"

    id = Column(Integer, primary_key=True, autoincrement=True)
    session_id = Column(String(100), nullable=False, index=True)
    role = Column(String(20), nullable=False)
    message = Column(Text, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)

    # Índice explícito en session_id para optimizar consultas por sesión
    __table_args__ = (
        Index("idx_chat_memory_session_id", "session_id"),
    )
