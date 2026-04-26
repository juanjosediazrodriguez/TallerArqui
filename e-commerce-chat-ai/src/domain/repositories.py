"""
Módulo de interfaces de repositorios del dominio.

Define los contratos abstractos para el acceso a datos.
Las implementaciones concretas viven en la capa de infraestructura,
lo que permite cambiar la base de datos sin modificar el dominio.
"""

from abc import ABC, abstractmethod
from typing import List, Optional
from .entities import Product, ChatMessage


class IProductRepository(ABC):
    """
    Interfaz abstracta que define el contrato para acceder a productos.

    Cualquier repositorio concreto de productos (SQLite, PostgreSQL, memoria)
    debe implementar todos estos métodos. Esto garantiza que el dominio
    y la aplicación no dependan de ninguna tecnología de base de datos específica.
    """

    @abstractmethod
    def get_all(self) -> List[Product]:
        """
        Obtiene todos los productos del sistema.

        Returns:
            List[Product]: Lista con todos los productos. Lista vacía si no hay.
        """
        pass

    @abstractmethod
    def get_by_id(self, product_id: int) -> Optional[Product]:
        """
        Busca un producto por su identificador único.

        Args:
            product_id (int): ID del producto a buscar.

        Returns:
            Optional[Product]: El producto encontrado, o None si no existe.
        """
        pass

    @abstractmethod
    def get_by_brand(self, brand: str) -> List[Product]:
        """
        Obtiene todos los productos de una marca específica.

        Args:
            brand (str): Nombre de la marca (ej: "Nike", "Adidas").

        Returns:
            List[Product]: Lista de productos de esa marca.
        """
        pass

    @abstractmethod
    def get_by_category(self, category: str) -> List[Product]:
        """
        Obtiene todos los productos de una categoría específica.

        Args:
            category (str): Nombre de la categoría (ej: "Running", "Casual").

        Returns:
            List[Product]: Lista de productos de esa categoría.
        """
        pass

    @abstractmethod
    def save(self, product: Product) -> Product:
        """
        Guarda o actualiza un producto en el sistema.

        Si el producto tiene ID, lo actualiza. Si no tiene ID (es nuevo),
        lo crea y le asigna un ID automáticamente.

        Args:
            product (Product): Entidad producto a guardar.

        Returns:
            Product: El producto guardado, con ID asignado si era nuevo.
        """
        pass

    @abstractmethod
    def delete(self, product_id: int) -> bool:
        """
        Elimina un producto por su ID.

        Args:
            product_id (int): ID del producto a eliminar.

        Returns:
            bool: True si se eliminó correctamente, False si no existía.
        """
        pass


class IChatRepository(ABC):
    """
    Interfaz abstracta que define el contrato para gestionar el historial de chat.

    Permite guardar mensajes y recuperar el historial de conversaciones.
    La implementación concreta utiliza SQLAlchemy con SQLite.
    """

    @abstractmethod
    def save_message(self, message: ChatMessage) -> ChatMessage:
        """
        Guarda un mensaje en el historial de conversación.

        Args:
            message (ChatMessage): Mensaje a persistir en la base de datos.

        Returns:
            ChatMessage: El mensaje guardado con su ID asignado.
        """
        pass

    @abstractmethod
    def get_session_history(
        self, session_id: str, limit: Optional[int] = None
    ) -> List[ChatMessage]:
        """
        Obtiene el historial completo (o parcial) de una sesión de chat.

        Args:
            session_id (str): Identificador único de la sesión.
            limit (Optional[int]): Si se especifica, retorna solo los últimos
                N mensajes. Si es None, retorna todos.

        Returns:
            List[ChatMessage]: Mensajes en orden cronológico (más antiguos primero).
        """
        pass

    @abstractmethod
    def delete_session_history(self, session_id: str) -> int:
        """
        Elimina todo el historial de una sesión de chat.

        Args:
            session_id (str): Identificador de la sesión a limpiar.

        Returns:
            int: Número de mensajes eliminados.
        """
        pass

    @abstractmethod
    def get_recent_messages(self, session_id: str, count: int) -> List[ChatMessage]:
        """
        Obtiene los últimos N mensajes de una sesión.

        Este método es crucial para mantener el contexto conversacional:
        se usan los últimos mensajes para que la IA recuerde de qué se habló.

        Args:
            session_id (str): Identificador de la sesión.
            count (int): Cantidad de mensajes recientes a recuperar.

        Returns:
            List[ChatMessage]: Los últimos N mensajes en orden cronológico.
        """
        pass
