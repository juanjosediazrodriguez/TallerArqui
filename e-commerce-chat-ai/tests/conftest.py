"""
Módulo de configuración y fixtures compartidos para las pruebas.

Los fixtures de pytest son funciones que preparan datos o estados
reutilizables en múltiples tests, evitando repetición de código.
"""

import pytest
from datetime import datetime
from src.domain.entities import Product, ChatMessage, ChatContext


@pytest.fixture
def sample_product():
    """
    Fixture que retorna un producto de ejemplo válido para usar en tests.

    Returns:
        Product: Producto Nike de ejemplo con todos los campos válidos.
    """
    return Product(
        id=1,
        name="Air Zoom Pegasus 40",
        brand="Nike",
        category="Running",
        size="42",
        color="Negro",
        price=120.0,
        stock=5,
        description="Zapatilla de running con amortiguación Air Zoom.",
    )


@pytest.fixture
def sample_chat_message():
    """
    Fixture que retorna un mensaje de chat de ejemplo para usar en tests.

    Returns:
        ChatMessage: Mensaje del usuario de ejemplo.
    """
    return ChatMessage(
        id=1,
        session_id="test_session",
        role="user",
        message="Busco zapatos Nike para correr",
        timestamp=datetime.utcnow(),
    )


@pytest.fixture
def sample_chat_context(sample_chat_message):
    """
    Fixture que retorna un contexto de conversación con un mensaje de ejemplo.

    Args:
        sample_chat_message: Fixture del mensaje de ejemplo.

    Returns:
        ChatContext: Contexto con un mensaje y límite de 6 mensajes.
    """
    return ChatContext(messages=[sample_chat_message], max_messages=6)
