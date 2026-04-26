"""
Módulo de entidades del dominio.

Contiene las entidades principales del negocio: Product, ChatMessage y ChatContext.
Estas clases son independientes de cualquier framework o base de datos.
"""

from dataclasses import dataclass
from typing import Optional
from datetime import datetime


@dataclass
class Product:
    """
    Entidad que representa un producto (zapato) en el e-commerce.

    Encapsula la lógica de negocio relacionada con productos, incluyendo
    validaciones de precio, stock y disponibilidad.

    Attributes:
        id (Optional[int]): Identificador único del producto. None si es nuevo.
        name (str): Nombre del producto.
        brand (str): Marca del producto (Nike, Adidas, Puma, etc.).
        category (str): Categoría del producto (Running, Casual, Formal).
        size (str): Talla del zapato.
        color (str): Color del producto.
        price (float): Precio en dólares. Debe ser mayor a 0.
        stock (int): Cantidad disponible en inventario. No puede ser negativo.
        description (str): Descripción detallada del producto.
    """

    id: Optional[int]
    name: str
    brand: str
    category: str
    size: str
    color: str
    price: float
    stock: int
    description: str

    def __post_init__(self):
        """
        Ejecuta validaciones de negocio al crear el objeto Product.

        Este método se llama automáticamente después del __init__ generado
        por @dataclass. Valida que los datos sean coherentes con las
        reglas de negocio.

        Raises:
            ValueError: Si el precio es menor o igual a 0.
            ValueError: Si el stock es negativo.
            ValueError: Si el nombre está vacío.
        """
        if self.price <= 0:
            raise ValueError("El precio debe ser mayor a 0")
        if self.stock < 0:
            raise ValueError("El stock no puede ser negativo")
        if not self.name or not self.name.strip():
            raise ValueError("El nombre del producto no puede estar vacío")

    def is_available(self) -> bool:
        """
        Verifica si el producto tiene stock disponible para venta.

        Returns:
            bool: True si el stock es mayor a 0, False en caso contrario.

        Example:
            >>> product = Product(id=1, name="Nike Air", brand="Nike",
            ...     category="Running", size="42", color="Negro",
            ...     price=120.0, stock=5, description="Zapato running")
            >>> product.is_available()
            True
        """
        return self.stock > 0

    def reduce_stock(self, quantity: int) -> None:
        """
        Reduce el stock del producto en la cantidad especificada.

        Se usa cuando se realiza una venta del producto.

        Args:
            quantity (int): Cantidad a reducir del stock. Debe ser positiva.

        Raises:
            ValueError: Si quantity es menor o igual a 0.
            ValueError: Si la cantidad supera el stock disponible.

        Example:
            >>> product.reduce_stock(3)
            >>> print(product.stock)  # Si tenía 5, ahora tiene 2
            2
        """
        if quantity <= 0:
            raise ValueError("La cantidad a reducir debe ser positiva")
        if quantity > self.stock:
            raise ValueError(
                f"No hay suficiente stock. Disponible: {self.stock}, solicitado: {quantity}"
            )
        self.stock -= quantity

    def increase_stock(self, quantity: int) -> None:
        """
        Aumenta el stock del producto en la cantidad especificada.

        Se usa cuando llega nuevo inventario al almacén.

        Args:
            quantity (int): Cantidad a aumentar en el stock. Debe ser positiva.

        Raises:
            ValueError: Si quantity es menor o igual a 0.

        Example:
            >>> product.increase_stock(10)
            >>> print(product.stock)  # Si tenía 2, ahora tiene 12
            12
        """
        if quantity <= 0:
            raise ValueError("La cantidad a aumentar debe ser positiva")
        self.stock += quantity


@dataclass
class ChatMessage:
    """
    Entidad que representa un mensaje dentro de una conversación de chat.

    Cada mensaje pertenece a una sesión y tiene un rol que indica si fue
    enviado por el usuario o por el asistente de IA.

    Attributes:
        id (Optional[int]): Identificador único del mensaje. None si es nuevo.
        session_id (str): Identificador único de la sesión de conversación.
        role (str): Rol del emisor. Solo acepta 'user' o 'assistant'.
        message (str): Contenido del mensaje.
        timestamp (datetime): Fecha y hora en que se creó el mensaje.
    """

    id: Optional[int]
    session_id: str
    role: str
    message: str
    timestamp: datetime

    def __post_init__(self):
        """
        Ejecuta validaciones de negocio al crear el mensaje.

        Raises:
            ValueError: Si el rol no es 'user' ni 'assistant'.
            ValueError: Si el mensaje está vacío.
            ValueError: Si el session_id está vacío.
        """
        if self.role not in ("user", "assistant"):
            raise ValueError(
                f"El rol debe ser 'user' o 'assistant', se recibió: '{self.role}'"
            )
        if not self.message or not self.message.strip():
            raise ValueError("El mensaje no puede estar vacío")
        if not self.session_id or not self.session_id.strip():
            raise ValueError("El session_id no puede estar vacío")

    def is_from_user(self) -> bool:
        """
        Verifica si el mensaje fue enviado por el usuario.

        Returns:
            bool: True si el rol es 'user', False en caso contrario.
        """
        return self.role == "user"

    def is_from_assistant(self) -> bool:
        """
        Verifica si el mensaje fue enviado por el asistente de IA.

        Returns:
            bool: True si el rol es 'assistant', False en caso contrario.
        """
        return self.role == "assistant"


@dataclass
class ChatContext:
    """
    Value Object que encapsula el contexto de una conversación.

    Mantiene los mensajes más recientes de la sesión para proporcionar
    memoria conversacional al asistente de IA, permitiendo respuestas
    coherentes entre turnos de conversación.

    Attributes:
        messages (list): Lista de objetos ChatMessage de la conversación.
        max_messages (int): Número máximo de mensajes a retener. Por defecto 6.
    """

    messages: list
    max_messages: int = 6

    def get_recent_messages(self) -> list:
        """
        Retorna los últimos N mensajes de la conversación.

        Limita el historial para evitar prompts demasiado largos
        al enviar contexto a la IA.

        Returns:
            list: Los últimos max_messages mensajes en orden cronológico.

        Example:
            >>> context = ChatContext(messages=[msg1, msg2, msg3], max_messages=2)
            >>> context.get_recent_messages()
            [msg2, msg3]
        """
        return self.messages[-self.max_messages:]

    def format_for_prompt(self) -> str:
        """
        Formatea el historial de conversación para incluirlo en un prompt de IA.

        Crea un string legible con el historial, indicando quién envió cada
        mensaje. Este formato es enviado a Google Gemini para que tenga
        memoria de la conversación.

        Returns:
            str: Historial formateado como texto plano.

        Example:
            >>> context.format_for_prompt()
            'Usuario: Busco zapatos Nike\\nAsistente: Tenemos varios modelos...'
        """
        lines = []
        for msg in self.get_recent_messages():
            if msg.is_from_user():
                lines.append(f"Usuario: {msg.message}")
            else:
                lines.append(f"Asistente: {msg.message}")
        return "\n".join(lines)
