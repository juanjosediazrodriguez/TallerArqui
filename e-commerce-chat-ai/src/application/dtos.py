"""
Módulo de DTOs (Data Transfer Objects) de la capa de aplicación.

Los DTOs son objetos intermedios que validan y transportan datos entre
la API (infraestructura) y los servicios de aplicación. Usan Pydantic
para validación automática de tipos y valores.
"""

from pydantic import BaseModel, validator
from typing import Optional
from datetime import datetime


class ProductDTO(BaseModel):
    """
    DTO para transferir datos de productos entre capas.

    Pydantic valida automáticamente que los tipos sean correctos
    y ejecuta los validadores personalizados al crear una instancia.

    Attributes:
        id (Optional[int]): ID del producto. None si es nuevo.
        name (str): Nombre del producto.
        brand (str): Marca del producto.
        category (str): Categoría del producto.
        size (str): Talla del zapato.
        color (str): Color del producto.
        price (float): Precio. Debe ser mayor a 0.
        stock (int): Stock disponible. No puede ser negativo.
        description (str): Descripción del producto.
    """

    id: Optional[int] = None
    name: str
    brand: str
    category: str
    size: str
    color: str
    price: float
    stock: int
    description: str

    @validator("price")
    def price_must_be_positive(cls, v):
        """
        Valida que el precio del producto sea mayor a 0.

        Args:
            v (float): Valor del precio a validar.

        Returns:
            float: El precio si es válido.

        Raises:
            ValueError: Si el precio es menor o igual a 0.
        """
        if v <= 0:
            raise ValueError("El precio debe ser mayor a 0")
        return v

    @validator("stock")
    def stock_must_be_non_negative(cls, v):
        """
        Valida que el stock no sea negativo.

        Args:
            v (int): Valor del stock a validar.

        Returns:
            int: El stock si es válido.

        Raises:
            ValueError: Si el stock es negativo.
        """
        if v < 0:
            raise ValueError("El stock no puede ser negativo")
        return v

    class Config:
        """Configuración de Pydantic para este DTO."""
        from_attributes = True  # Permite crear el DTO directamente desde un ORM model


class ChatMessageRequestDTO(BaseModel):
    """
    DTO para recibir mensajes del usuario en el endpoint POST /chat.

    Representa la petición que hace el frontend cuando el usuario
    escribe un mensaje en el chat.

    Attributes:
        session_id (str): Identificador único de la sesión del usuario.
        message (str): Texto del mensaje enviado por el usuario.
    """

    session_id: str
    message: str

    @validator("message")
    def message_not_empty(cls, v):
        """
        Valida que el mensaje no esté vacío ni contenga solo espacios.

        Args:
            v (str): Texto del mensaje a validar.

        Returns:
            str: El mensaje si es válido.

        Raises:
            ValueError: Si el mensaje está vacío.
        """
        if not v or not v.strip():
            raise ValueError("El mensaje no puede estar vacío")
        return v

    @validator("session_id")
    def session_id_not_empty(cls, v):
        """
        Valida que el session_id no esté vacío.

        Args:
            v (str): El session_id a validar.

        Returns:
            str: El session_id si es válido.

        Raises:
            ValueError: Si el session_id está vacío.
        """
        if not v or not v.strip():
            raise ValueError("El session_id no puede estar vacío")
        return v


class ChatMessageResponseDTO(BaseModel):
    """
    DTO para enviar la respuesta del chat al cliente.

    Contiene tanto el mensaje original del usuario como la respuesta
    generada por la IA, junto con metadatos de la sesión.

    Attributes:
        session_id (str): Identificador de la sesión de conversación.
        user_message (str): Mensaje original enviado por el usuario.
        assistant_message (str): Respuesta generada por la IA.
        timestamp (datetime): Fecha y hora de la respuesta.
    """

    session_id: str
    user_message: str
    assistant_message: str
    timestamp: datetime


class ChatHistoryDTO(BaseModel):
    """
    DTO para mostrar un mensaje individual del historial de chat.

    Se usa en el endpoint GET /chat/history/{session_id} para
    retornar la lista de mensajes de una sesión.

    Attributes:
        id (int): Identificador único del mensaje.
        role (str): Rol del emisor ('user' o 'assistant').
        message (str): Contenido del mensaje.
        timestamp (datetime): Fecha y hora del mensaje.
    """

    id: int
    role: str
    message: str
    timestamp: datetime

    class Config:
        """Configuración de Pydantic para este DTO."""
        from_attributes = True
