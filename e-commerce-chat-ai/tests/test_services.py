"""
Pruebas unitarias para los servicios de la capa de aplicación.

Usa mocks (objetos falsos) en lugar de una base de datos real para
aislar la lógica del servicio de las dependencias externas.
"""

import pytest
from unittest.mock import MagicMock
from src.application.product_service import ProductService
from src.domain.entities import Product
from src.domain.exceptions import ProductNotFoundError
from src.application.dtos import ProductDTO


def crear_producto_ejemplo(id=1, stock=5, price=100.0):
    """
    Crea una entidad Product de ejemplo para usar en tests.

    Args:
        id: ID del producto.
        stock: Cantidad en stock.
        price: Precio del producto.

    Returns:
        Product: Producto de ejemplo con los valores dados.
    """
    return Product(
        id=id,
        name="Zapato Test",
        brand="Nike",
        category="Running",
        size="42",
        color="Negro",
        price=price,
        stock=stock,
        description="Descripción de prueba.",
    )


class TestProductService:
    """Pruebas para el servicio de productos."""

    def test_get_all_products_retorna_lista(self):
        """Verifica que get_all_products retorna todos los productos del repositorio."""
        # Crear un repositorio falso (mock) que retorna 2 productos
        mock_repo = MagicMock()
        mock_repo.get_all.return_value = [
            crear_producto_ejemplo(id=1),
            crear_producto_ejemplo(id=2),
        ]

        service = ProductService(mock_repo)
        result = service.get_all_products()

        assert len(result) == 2
        mock_repo.get_all.assert_called_once()

    def test_get_product_by_id_existente(self):
        """Verifica que get_product_by_id retorna el producto correcto."""
        producto = crear_producto_ejemplo(id=5)
        mock_repo = MagicMock()
        mock_repo.get_by_id.return_value = producto

        service = ProductService(mock_repo)
        result = service.get_product_by_id(5)

        assert result.id == 5
        mock_repo.get_by_id.assert_called_once_with(5)

    def test_get_product_by_id_no_existente_lanza_error(self):
        """Verifica que se lanza ProductNotFoundError si el ID no existe."""
        mock_repo = MagicMock()
        mock_repo.get_by_id.return_value = None  # Simula que no encontró nada

        service = ProductService(mock_repo)

        with pytest.raises(ProductNotFoundError):
            service.get_product_by_id(999)

    def test_get_available_products_filtra_sin_stock(self):
        """Verifica que get_available_products excluye productos sin stock."""
        mock_repo = MagicMock()
        mock_repo.get_all.return_value = [
            crear_producto_ejemplo(id=1, stock=5),   # Disponible
            crear_producto_ejemplo(id=2, stock=0),   # Agotado
            crear_producto_ejemplo(id=3, stock=3),   # Disponible
        ]

        service = ProductService(mock_repo)
        result = service.get_available_products()

        assert len(result) == 2  # Solo los disponibles

    def test_delete_product_existente(self):
        """Verifica que delete_product elimina el producto correctamente."""
        mock_repo = MagicMock()
        mock_repo.get_by_id.return_value = crear_producto_ejemplo(id=1)
        mock_repo.delete.return_value = True

        service = ProductService(mock_repo)
        result = service.delete_product(1)

        assert result is True
        mock_repo.delete.assert_called_once_with(1)

    def test_delete_product_no_existente_lanza_error(self):
        """Verifica error al intentar eliminar un producto que no existe."""
        mock_repo = MagicMock()
        mock_repo.get_by_id.return_value = None

        service = ProductService(mock_repo)

        with pytest.raises(ProductNotFoundError):
            service.delete_product(999)
