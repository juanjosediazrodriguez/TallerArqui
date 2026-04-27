"""
Módulo del servicio de aplicación para el chat con IA.

Implementa el caso de uso principal del sistema: procesar mensajes
del usuario y generar respuestas contextuales usando Google Gemini AI.
"""

from datetime import datetime
from typing import List, Optional
from ..domain.entities import ChatMessage, ChatContext
from ..domain.repositories import IProductRepository, IChatRepository
from ..domain.exceptions import ChatServiceError
from .dtos import ChatMessageRequestDTO, ChatMessageResponseDTO, ChatHistoryDTO


class ChatService:
    """
    Servicio de aplicación para gestionar el chat con IA.

    Orquesta la interacción entre el repositorio de productos, el repositorio
    de chat y el servicio de IA de Gemini para proporcionar respuestas
    contextuales y coherentes a los usuarios.

    El flujo completo de process_message:
    1. Obtiene productos disponibles para dárselos como contexto a la IA
    2. Recupera el historial reciente de la sesión
    3. Genera respuesta usando Gemini con ese contexto
    4. Guarda el mensaje del usuario y la respuesta en la base de datos
    5. Retorna la respuesta al cliente

    Attributes:
        product_repo (IProductRepository): Repositorio para obtener productos.
        chat_repo (IChatRepository): Repositorio para guardar/leer mensajes.
        ai_service: Servicio de IA (GeminiService) para generar respuestas.
    """

    def __init__(
        self,
        product_repo: IProductRepository,
        chat_repo: IChatRepository,
        ai_service,
    ):
        """
        Inicializa el servicio con sus dependencias inyectadas.

        Args:
            product_repo (IProductRepository): Repositorio de productos.
            chat_repo (IChatRepository): Repositorio de mensajes de chat.
            ai_service: Instancia del servicio de IA (GeminiService).
        """
        self.product_repo = product_repo
        self.chat_repo = chat_repo
        self.ai_service = ai_service

    async def process_message(
        self, request: ChatMessageRequestDTO
    ) -> ChatMessageResponseDTO:
        """
        Procesa un mensaje del usuario y genera una respuesta con IA.

        Este es el método central del sistema. Coordina todos los componentes
        para generar una respuesta coherente con contexto del catálogo y
        memoria de la conversación.

        Args:
            request (ChatMessageRequestDTO): Mensaje del usuario con su session_id.

        Returns:
            ChatMessageResponseDTO: Respuesta de la IA con metadata de la sesión.

        Raises:
            ChatServiceError: Si ocurre un error al generar la respuesta o
                al comunicarse con el servicio de IA.

        Example:
            >>> request = ChatMessageRequestDTO(
            ...     session_id="usuario_001",
            ...     message="Busco zapatos Nike para correr"
            ... )
            >>> response = await chat_service.process_message(request)
            >>> print(response.assistant_message)
            "Tenemos el Nike Air Zoom Pegasus en talla 42 por $120..."
        """
        try:
            # 1. Obtener todos los productos del catálogo para dar contexto a la IA
            products = self.product_repo.get_all()

            # 2. Recuperar los últimos 6 mensajes de esta sesión (memoria conversacional)
            recent_messages = self.chat_repo.get_recent_messages(
                session_id=request.session_id, count=6
            )

            # 3. Crear el contexto conversacional con el historial
            context = ChatContext(messages=recent_messages)

            # 4. Llamar a la IA con el mensaje, los productos y el historial
            assistant_response = await self.ai_service.generate_response(
                user_message=request.message,
                products=products,
                context=context,
            )

            now = datetime.utcnow()

            # 5. Guardar el mensaje del usuario en la base de datos
            user_message = ChatMessage(
                id=None,
                session_id=request.session_id,
                role="user",
                message=request.message,
                timestamp=now,
            )
            self.chat_repo.save_message(user_message)

            # 6. Guardar la respuesta del asistente en la base de datos
            assistant_message = ChatMessage(
                id=None,
                session_id=request.session_id,
                role="assistant",
                message=assistant_response,
                timestamp=now,
            )
            self.chat_repo.save_message(assistant_message)

            # 7. Retornar la respuesta al cliente
            return ChatMessageResponseDTO(
                session_id=request.session_id,
                user_message=request.message,
                assistant_message=assistant_response,
                timestamp=now,
            )

        except Exception as e:
            raise ChatServiceError(f"Error al procesar el mensaje: {str(e)}")

    def get_session_history(
        self, session_id: str, limit: int = 10
    ) -> List[ChatHistoryDTO]:
        """
        Obtiene el historial de mensajes de una sesión de chat.

        Args:
            session_id (str): Identificador de la sesión de conversación.
            limit (int): Número máximo de mensajes a retornar. Por defecto 10.

        Returns:
            List[ChatHistoryDTO]: Lista de mensajes en orden cronológico.
        """
        messages = self.chat_repo.get_session_history(
            session_id=session_id, limit=limit
        )
        return [
            ChatHistoryDTO(
                id=msg.id,
                role=msg.role,
                message=msg.message,
                timestamp=msg.timestamp,
            )
            for msg in messages
        ]

    def clear_session_history(self, session_id: str) -> int:
        """
        Elimina todo el historial de mensajes de una sesión.

        Útil para reiniciar una conversación sin crear una nueva sesión.

        Args:
            session_id (str): Identificador de la sesión a limpiar.

        Returns:
            int: Número de mensajes eliminados.
        """
        return self.chat_repo.delete_session_history(session_id)
