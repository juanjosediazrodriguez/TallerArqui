"""
Pruebas unitarias para las entidades del dominio.

Verifica que las entidades Product, ChatMessage y ChatContext
cumplan correctamente con las reglas de negocio definidas.
"""

import pytest
from datetime import datetime
from src.domain.entities import Product, ChatMessage, ChatContext


class TestProduct:
    """Pruebas para la entidad Product."""

    def test_crear_producto_valido(self):
        """Verifica que se puede crear un producto con datos correctos."""
        product = Product(
            id=1,
            name="Nike Air",
            brand="Nike",
            category="Running",
            size="42",
            color="Negro",
            price=120.0,
            stock=5,
            description="Zapatilla de running.",
        )
        assert product.name == "Nike Air"
        assert product.price == 120.0
        assert product.stock == 5

    def test_precio_negativo_lanza_error(self):
        """Verifica que un precio negativo lanza ValueError."""
        with pytest.raises(ValueError, match="precio"):
            Product(
                id=None,
                name="Zapato",
                brand="Nike",
                category="Running",
                size="42",
                color="Negro",
                price=-10.0,
                stock=5,
                description="Desc.",
            )

    def test_precio_cero_lanza_error(self):
        """Verifica que un precio de 0 lanza ValueError."""
        with pytest.raises(ValueError, match="precio"):
            Product(
                id=None,
                name="Zapato",
                brand="Nike",
                category="Running",
                size="42",
                color="Negro",
                price=0,
                stock=5,
                description="Desc.",
            )

    def test_stock_negativo_lanza_error(self):
        """Verifica que un stock negativo lanza ValueError."""
        with pytest.raises(ValueError, match="stock"):
            Product(
                id=None,
                name="Zapato",
                brand="Nike",
                category="Running",
                size="42",
                color="Negro",
                price=100.0,
                stock=-1,
                description="Desc.",
            )

    def test_nombre_vacio_lanza_error(self):
        """Verifica que un nombre vacío lanza ValueError."""
        with pytest.raises(ValueError, match="nombre"):
            Product(
                id=None,
                name="",
                brand="Nike",
                category="Running",
                size="42",
                color="Negro",
                price=100.0,
                stock=5,
                description="Desc.",
            )

    def test_is_available_con_stock(self, sample_product):
        """Verifica que is_available retorna True cuando hay stock."""
        assert sample_product.is_available() is True

    def test_is_available_sin_stock(self, sample_product):
        """Verifica que is_available retorna False cuando stock es 0."""
        sample_product.stock = 0
        assert sample_product.is_available() is False

    def test_reduce_stock_exitoso(self, sample_product):
        """Verifica que reduce_stock reduce correctamente el stock."""
        stock_inicial = sample_product.stock
        sample_product.reduce_stock(3)
        assert sample_product.stock == stock_inicial - 3

    def test_reduce_stock_insuficiente_lanza_error(self, sample_product):
        """Verifica error al intentar reducir más stock del disponible."""
        with pytest.raises(ValueError):
            sample_product.reduce_stock(100)

    def test_reduce_stock_cantidad_negativa_lanza_error(self, sample_product):
        """Verifica error al intentar reducir con cantidad negativa."""
        with pytest.raises(ValueError):
            sample_product.reduce_stock(-1)

    def test_increase_stock(self, sample_product):
        """Verifica que increase_stock aumenta correctamente el stock."""
        stock_inicial = sample_product.stock
        sample_product.increase_stock(10)
        assert sample_product.stock == stock_inicial + 10

    def test_increase_stock_negativo_lanza_error(self, sample_product):
        """Verifica error al intentar aumentar con cantidad negativa."""
        with pytest.raises(ValueError):
            sample_product.increase_stock(-5)


class TestChatMessage:
    """Pruebas para la entidad ChatMessage."""

    def test_crear_mensaje_usuario_valido(self):
        """Verifica que se puede crear un mensaje de usuario válido."""
        msg = ChatMessage(
            id=1,
            session_id="sesion_001",
            role="user",
            message="Hola",
            timestamp=datetime.utcnow(),
        )
        assert msg.is_from_user() is True
        assert msg.is_from_assistant() is False

    def test_crear_mensaje_asistente_valido(self):
        """Verifica que se puede crear un mensaje del asistente válido."""
        msg = ChatMessage(
            id=2,
            session_id="sesion_001",
            role="assistant",
            message="Hola, ¿en qué puedo ayudarte?",
            timestamp=datetime.utcnow(),
        )
        assert msg.is_from_assistant() is True
        assert msg.is_from_user() is False

    def test_rol_invalido_lanza_error(self):
        """Verifica que un rol inválido lanza ValueError."""
        with pytest.raises(ValueError, match="rol"):
            ChatMessage(
                id=None,
                session_id="sesion_001",
                role="admin",
                message="Mensaje",
                timestamp=datetime.utcnow(),
            )

    def test_mensaje_vacio_lanza_error(self):
        """Verifica que un mensaje vacío lanza ValueError."""
        with pytest.raises(ValueError, match="mensaje"):
            ChatMessage(
                id=None,
                session_id="sesion_001",
                role="user",
                message="",
                timestamp=datetime.utcnow(),
            )

    def test_session_id_vacio_lanza_error(self):
        """Verifica que un session_id vacío lanza ValueError."""
        with pytest.raises(ValueError, match="session_id"):
            ChatMessage(
                id=None,
                session_id="",
                role="user",
                message="Hola",
                timestamp=datetime.utcnow(),
            )


class TestChatContext:
    """Pruebas para el Value Object ChatContext."""

    def test_get_recent_messages_retorna_ultimos_n(self):
        """Verifica que get_recent_messages retorna solo los últimos N mensajes."""
        mensajes = [
            ChatMessage(
                id=i,
                session_id="s",
                role="user",
                message=f"Mensaje {i}",
                timestamp=datetime.utcnow(),
            )
            for i in range(1, 10)
        ]
        context = ChatContext(messages=mensajes, max_messages=3)
        recientes = context.get_recent_messages()
        assert len(recientes) == 3
        assert recientes[-1].message == "Mensaje 9"

    def test_format_for_prompt_formato_correcto(self, sample_chat_context):
        """Verifica que format_for_prompt genera el formato correcto."""
        texto = sample_chat_context.format_for_prompt()
        assert "Usuario:" in texto
        assert "Busco zapatos Nike para correr" in texto

    def test_format_for_prompt_contexto_vacio(self):
        """Verifica que format_for_prompt retorna string vacío si no hay mensajes."""
        context = ChatContext(messages=[], max_messages=6)
        assert context.format_for_prompt() == ""
