"""
Excepciones específicas del dominio.

Representan errores de negocio (no errores técnicos).
Al usar excepciones propias, el código es más descriptivo y fácil de depurar.
"""


class ProductNotFoundError(Exception):
    """
    Se lanza cuando se busca un producto que no existe en el sistema.

    Attributes:
        message (str): Mensaje descriptivo del error.

    Example:
        >>> raise ProductNotFoundError(product_id=42)
        ProductNotFoundError: Producto con ID 42 no encontrado
    """

    def __init__(self, product_id: int = None):
        """
        Inicializa el error con un mensaje que puede incluir el ID del producto.

        Args:
            product_id (int, optional): ID del producto que no fue encontrado.
                Si se proporciona, el mensaje incluye el ID específico.
        """
        if product_id is not None:
            self.message = f"Producto con ID {product_id} no encontrado"
        else:
            self.message = "Producto no encontrado"
        super().__init__(self.message)


class InvalidProductDataError(Exception):
    """
    Se lanza cuando los datos de un producto son inválidos.

    Por ejemplo, cuando se intenta crear un producto con precio negativo
    o con nombre vacío.

    Attributes:
        message (str): Mensaje descriptivo del error de validación.
    """

    def __init__(self, message: str = "Datos de producto inválidos"):
        """
        Inicializa el error con un mensaje personalizado.

        Args:
            message (str): Descripción del problema de validación.
                Por defecto: "Datos de producto inválidos".
        """
        self.message = message
        super().__init__(self.message)


class ChatServiceError(Exception):
    """
    Se lanza cuando hay un error en el servicio de chat.

    Por ejemplo, cuando la IA no responde o hay un problema de conexión
    con Google Gemini.

    Attributes:
        message (str): Mensaje descriptivo del error del servicio de chat.
    """

    def __init__(self, message: str = "Error en el servicio de chat"):
        """
        Inicializa el error con un mensaje personalizado.

        Args:
            message (str): Descripción del error ocurrido en el chat.
                Por defecto: "Error en el servicio de chat".
        """
        self.message = message
        super().__init__(self.message)
