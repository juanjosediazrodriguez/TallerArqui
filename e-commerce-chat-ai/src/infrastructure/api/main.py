"""
Módulo principal de la API REST con FastAPI.

Define la aplicación FastAPI, configura CORS, registra los eventos
de ciclo de vida y declara todos los endpoints HTTP del sistema.
"""

from datetime import datetime
from typing import List
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from ..db.database import get_db, init_db
from ..repositories.product_repository import SQLProductRepository
from ..repositories.chat_repository import SQLChatRepository
from ..llm_providers.gemini_service import GeminiService
from ...application.product_service import ProductService
from ...application.chat_service import ChatService
from ...application.dtos import (
    ProductDTO,
    ChatMessageRequestDTO,
    ChatMessageResponseDTO,
    ChatHistoryDTO,
)
from ...domain.exceptions import ProductNotFoundError, ChatServiceError

# Instancia principal de la aplicación FastAPI.
# El título y descripción aparecen en la documentación Swagger (/docs).
app = FastAPI(
    title="ZapatoShop - E-commerce con Chat IA",
    description=(
        "API REST de e-commerce de zapatos con asistente de inteligencia artificial. "
        "Permite consultar el catálogo de productos y conversar con un asistente "
        "impulsado por Google Gemini AI para encontrar el zapato perfecto."
    ),
    version="1.0.0",
)

# Configuración de CORS (Cross-Origin Resource Sharing).
# Permite que un frontend en otro dominio pueda llamar a esta API.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especificar dominios concretos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def startup_event():
    """
    Evento que se ejecuta automáticamente al iniciar la aplicación.

    Crea todas las tablas de la base de datos si no existen y carga
    los productos de ejemplo si la base está vacía.
    """
    init_db()


# ─────────────────────────────────────────────
# ENDPOINTS GENERALES
# ─────────────────────────────────────────────

@app.get("/", tags=["General"])
def root():
    """
    Endpoint raíz que retorna información básica de la API.

    Returns:
        dict: Nombre, versión y endpoints principales disponibles.

    Example:
        GET /
        Response: {"nombre": "ZapatoShop API", "version": "1.0.0", ...}
    """
    return {
        "nombre": "ZapatoShop - E-commerce con Chat IA",
        "version": "1.0.0",
        "descripcion": "API de e-commerce de zapatos con asistente de IA",
        "documentacion": "/docs",
        "endpoints_principales": {
            "productos": "/products",
            "chat": "/chat",
            "historial": "/chat/history/{session_id}",
            "salud": "/health",
        },
    }


@app.get("/health", tags=["General"])
def health_check():
    """
    Endpoint de verificación de salud del servicio.

    Usado por Docker y sistemas de monitoreo para confirmar que
    la aplicación está corriendo correctamente.

    Returns:
        dict: Estado del servicio y timestamp actual.

    Example:
        GET /health
        Response: {"status": "ok", "timestamp": "2024-01-15T10:30:00"}
    """
    return {
        "status": "ok",
        "timestamp": datetime.utcnow().isoformat(),
        "servicio": "ZapatoShop API",
    }


# ─────────────────────────────────────────────
# ENDPOINTS DE PRODUCTOS
# ─────────────────────────────────────────────

@app.get("/products", response_model=List[ProductDTO], tags=["Productos"])
def get_products(db: Session = Depends(get_db)):
    """
    Obtiene la lista completa de productos del catálogo.

    Retorna todos los productos registrados en la base de datos,
    incluyendo aquellos sin stock disponible.

    Args:
        db (Session): Sesión de base de datos inyectada por FastAPI.

    Returns:
        List[ProductDTO]: Lista de todos los productos con su información completa.

    Example:
        GET /products
        Response: [
            {"id": 1, "name": "Air Zoom Pegasus 40", "brand": "Nike", "price": 120.0, ...},
            {"id": 2, "name": "Ultraboost 22", "brand": "Adidas", "price": 150.0, ...}
        ]
    """
    repo = SQLProductRepository(db)
    service = ProductService(repo)
    return service.get_all_products()


@app.get("/products/{product_id}", response_model=ProductDTO, tags=["Productos"])
def get_product(product_id: int, db: Session = Depends(get_db)):
    """
    Obtiene un producto específico por su identificador único.

    Args:
        product_id (int): ID numérico del producto a buscar.
        db (Session): Sesión de base de datos inyectada por FastAPI.

    Returns:
        ProductDTO: Datos completos del producto encontrado.

    Raises:
        HTTPException(404): Si no existe ningún producto con ese ID.

    Example:
        GET /products/1
        Response: {"id": 1, "name": "Air Zoom Pegasus 40", "brand": "Nike", ...}
    """
    repo = SQLProductRepository(db)
    service = ProductService(repo)
    try:
        return service.get_product_by_id(product_id)
    except ProductNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))


# ─────────────────────────────────────────────
# ENDPOINTS DE CHAT CON IA
# ─────────────────────────────────────────────

@app.post("/chat", response_model=ChatMessageResponseDTO, tags=["Chat IA"])
async def chat(request: ChatMessageRequestDTO, db: Session = Depends(get_db)):
    """
    Procesa un mensaje del usuario y genera una respuesta con IA.

    Este es el endpoint principal del sistema. Recibe el mensaje del usuario,
    consulta el catálogo de productos, recupera el historial de conversación
    y genera una respuesta contextual usando Google Gemini AI.

    Args:
        request (ChatMessageRequestDTO): Cuerpo del request con session_id y message.
        db (Session): Sesión de base de datos inyectada por FastAPI.

    Returns:
        ChatMessageResponseDTO: Respuesta de la IA con el mensaje original y timestamp.

    Raises:
        HTTPException(500): Si ocurre un error al procesar el mensaje o
            al comunicarse con el servicio de IA.

    Example:
        POST /chat
        Body: {"session_id": "usuario_001", "message": "Busco zapatos Nike para correr"}
        Response: {
            "session_id": "usuario_001",
            "user_message": "Busco zapatos Nike para correr",
            "assistant_message": "¡Hola! Tengo el Nike Air Zoom Pegasus en talla 42...",
            "timestamp": "2024-01-15T10:30:00"
        }
    """
    product_repo = SQLProductRepository(db)
    chat_repo = SQLChatRepository(db)

    try:
        ai_service = GeminiService()
    except ChatServiceError as e:
        raise HTTPException(status_code=500, detail=str(e))

    service = ChatService(product_repo, chat_repo, ai_service)

    try:
        return await service.process_message(request)
    except ChatServiceError as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get(
    "/chat/history/{session_id}",
    response_model=List[ChatHistoryDTO],
    tags=["Chat IA"],
)
def get_chat_history(
    session_id: str, limit: int = 10, db: Session = Depends(get_db)
):
    """
    Obtiene el historial de mensajes de una sesión de chat.

    Retorna los mensajes en orden cronológico (más antiguos primero)
    para que el usuario pueda ver la conversación completa.

    Args:
        session_id (str): Identificador de la sesión de conversación.
        limit (int): Número máximo de mensajes a retornar. Por defecto 10.
        db (Session): Sesión de base de datos inyectada por FastAPI.

    Returns:
        List[ChatHistoryDTO]: Lista de mensajes del historial.

    Example:
        GET /chat/history/usuario_001?limit=5
        Response: [
            {"id": 1, "role": "user", "message": "Hola", "timestamp": "..."},
            {"id": 2, "role": "assistant", "message": "¡Hola!", "timestamp": "..."}
        ]
    """
    product_repo = SQLProductRepository(db)
    chat_repo = SQLChatRepository(db)
    ai_service = None  # No se necesita IA para leer historial
    service = ChatService(product_repo, chat_repo, ai_service)
    return service.get_session_history(session_id, limit)


@app.delete("/chat/history/{session_id}", tags=["Chat IA"])
def delete_chat_history(session_id: str, db: Session = Depends(get_db)):
    """
    Elimina todo el historial de mensajes de una sesión de chat.

    Útil para reiniciar una conversación sin necesidad de cambiar
    el session_id. La IA perderá la memoria de esa sesión.

    Args:
        session_id (str): Identificador de la sesión a limpiar.
        db (Session): Sesión de base de datos inyectada por FastAPI.

    Returns:
        dict: Mensaje de confirmación con la cantidad de mensajes eliminados.

    Example:
        DELETE /chat/history/usuario_001
        Response: {"mensaje": "Historial eliminado", "mensajes_eliminados": 4}
    """
    product_repo = SQLProductRepository(db)
    chat_repo = SQLChatRepository(db)
    service = ChatService(product_repo, chat_repo, None)
    deleted = service.clear_session_history(session_id)
    return {
        "mensaje": "Historial eliminado correctamente",
        "session_id": session_id,
        "mensajes_eliminados": deleted,
    }
