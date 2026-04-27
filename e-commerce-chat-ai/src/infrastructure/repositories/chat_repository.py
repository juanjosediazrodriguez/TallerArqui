"""
Módulo del repositorio concreto de chat con SQLAlchemy.

Implementa la interfaz IChatRepository para persistir y recuperar
mensajes del historial de conversaciones usando SQLite.
"""

from typing import List, Optional
from datetime import datetime
from sqlalchemy.orm import Session
from ...domain.entities import ChatMessage
from ...domain.repositories import IChatRepository
from ..db.models import ChatMemoryModel


class SQLChatRepository(IChatRepository):
    """
    Implementación concreta del repositorio de chat usando SQLAlchemy.

    Gestiona la persistencia del historial de conversaciones. Los mensajes
    se ordenan cronológicamente para que la IA tenga el contexto correcto.

    Attributes:
        db (Session): Sesión activa de SQLAlchemy para ejecutar queries.
    """

    def __init__(self, db: Session):
        """
        Inicializa el repositorio con una sesión de base de datos.

        Args:
            db (Session): Sesión de SQLAlchemy inyectada por FastAPI.
        """
        self.db = db

    def save_message(self, message: ChatMessage) -> ChatMessage:
        """
        Guarda un mensaje de chat en la base de datos.

        Args:
            message (ChatMessage): Mensaje a persistir.

        Returns:
            ChatMessage: El mensaje guardado con su ID asignado por la BD.
        """
        model = self._entity_to_model(message)
        self.db.add(model)
        self.db.commit()
        self.db.refresh(model)
        return self._model_to_entity(model)

    def get_session_history(
        self, session_id: str, limit: Optional[int] = None
    ) -> List[ChatMessage]:
        """
        Obtiene el historial de una sesión, opcionalmente limitado.

        Los mensajes se retornan en orden cronológico (más antiguos primero)
        para que el historial sea coherente al mostrarlo al usuario.

        Args:
            session_id (str): Identificador de la sesión de conversación.
            limit (Optional[int]): Número máximo de mensajes a retornar.
                Si es None, retorna todos los mensajes de la sesión.

        Returns:
            List[ChatMessage]: Mensajes en orden cronológico.
        """
        query = (
            self.db.query(ChatMemoryModel)
            .filter(ChatMemoryModel.session_id == session_id)
            .order_by(ChatMemoryModel.timestamp.asc())
        )

        if limit:
            # Para obtener los últimos N, ordenamos DESC, tomamos N y revertimos
            query = (
                self.db.query(ChatMemoryModel)
                .filter(ChatMemoryModel.session_id == session_id)
                .order_by(ChatMemoryModel.timestamp.desc())
                .limit(limit)
            )
            models = query.all()
            models.reverse()  # Revertir para orden cronológico ascendente
        else:
            models = query.all()

        return [self._model_to_entity(m) for m in models]

    def delete_session_history(self, session_id: str) -> int:
        """
        Elimina todos los mensajes de una sesión de chat.

        Args:
            session_id (str): Identificador de la sesión a limpiar.

        Returns:
            int: Número de mensajes eliminados.
        """
        deleted = (
            self.db.query(ChatMemoryModel)
            .filter(ChatMemoryModel.session_id == session_id)
            .delete()
        )
        self.db.commit()
        return deleted

    def get_recent_messages(self, session_id: str, count: int) -> List[ChatMessage]:
        """
        Obtiene los últimos N mensajes de una sesión en orden cronológico.

        Este método es clave para mantener el contexto conversacional:
        se recuperan los mensajes más recientes para incluirlos en el
        prompt que se envía a Google Gemini.

        Args:
            session_id (str): Identificador de la sesión.
            count (int): Número de mensajes recientes a recuperar.

        Returns:
            List[ChatMessage]: Los últimos N mensajes en orden cronológico
                (más antiguos primero, para que la IA los lea en secuencia).
        """
        models = (
            self.db.query(ChatMemoryModel)
            .filter(ChatMemoryModel.session_id == session_id)
            .order_by(ChatMemoryModel.timestamp.desc())
            .limit(count)
            .all()
        )
        models.reverse()  # Revertir para orden cronológico
        return [self._model_to_entity(m) for m in models]

    def _model_to_entity(self, model: ChatMemoryModel) -> ChatMessage:
        """
        Convierte un modelo ORM a una entidad de dominio ChatMessage.

        Args:
            model (ChatMemoryModel): Modelo ORM de la base de datos.

        Returns:
            ChatMessage: Entidad de dominio equivalente.
        """
        return ChatMessage(
            id=model.id,
            session_id=model.session_id,
            role=model.role,
            message=model.message,
            timestamp=model.timestamp or datetime.utcnow(),
        )

    def _entity_to_model(self, message: ChatMessage) -> ChatMemoryModel:
        """
        Convierte una entidad de dominio ChatMessage a un modelo ORM.

        Args:
            message (ChatMessage): Entidad de dominio a convertir.

        Returns:
            ChatMemoryModel: Modelo ORM listo para persistir.
        """
        return ChatMemoryModel(
            session_id=message.session_id,
            role=message.role,
            message=message.message,
            timestamp=message.timestamp,
        )
