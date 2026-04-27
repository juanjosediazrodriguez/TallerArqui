"""
Módulo del servicio de aplicación para productos.

Implementa los casos de uso relacionados con productos del e-commerce.
Orquesta el acceso a datos a través del repositorio inyectado.
"""

from typing import List, Optional
from ..domain.entities import Product
from ..domain.repositories import IProductRepository
from ..domain.exceptions import ProductNotFoundError, InvalidProductDataError
from .dtos import ProductDTO


class ProductService:
    """
    Servicio de aplicación para gestionar productos del e-commerce.

    Implementa los casos de uso de productos: listar, buscar, crear,
    actualizar y eliminar. Recibe el repositorio por inyección de
    dependencias, lo que facilita las pruebas unitarias con mocks.

    Attributes:
        product_repo (IProductRepository): Repositorio de acceso a productos.
    """

    def __init__(self, product_repo: IProductRepository):
        """
        Inicializa el servicio con el repositorio de productos.

        Args:
            product_repo (IProductRepository): Implementación del repositorio
                de productos a usar (SQLite, memoria, etc.).
        """
        self.product_repo = product_repo

    def get_all_products(self) -> List[ProductDTO]:
        """
        Obtiene la lista completa de todos los productos del catálogo.

        Returns:
            List[ProductDTO]: Lista de todos los productos disponibles.
                Puede ser una lista vacía si no hay productos.
        """
        products = self.product_repo.get_all()
        return [self._entity_to_dto(p) for p in products]

    def get_product_by_id(self, product_id: int) -> ProductDTO:
        """
        Busca y retorna un producto por su identificador único.

        Args:
            product_id (int): ID del producto a buscar.

        Returns:
            ProductDTO: Datos del producto encontrado.

        Raises:
            ProductNotFoundError: Si no existe ningún producto con ese ID.
        """
        product = self.product_repo.get_by_id(product_id)
        if not product:
            raise ProductNotFoundError(product_id)
        return self._entity_to_dto(product)

    def get_available_products(self) -> List[ProductDTO]:
        """
        Obtiene únicamente los productos que tienen stock disponible.

        Returns:
            List[ProductDTO]: Lista de productos con stock mayor a 0.
        """
        products = self.product_repo.get_all()
        available = [p for p in products if p.is_available()]
        return [self._entity_to_dto(p) for p in available]

    def search_products(
        self, brand: Optional[str] = None, category: Optional[str] = None
    ) -> List[ProductDTO]:
        """
        Filtra productos por marca y/o categoría.

        Si se proporcionan ambos filtros, retorna productos que coincidan
        con los dos. Si no se pasa ningún filtro, retorna todos.

        Args:
            brand (Optional[str]): Marca por la que filtrar (ej: "Nike").
            category (Optional[str]): Categoría por la que filtrar (ej: "Running").

        Returns:
            List[ProductDTO]: Lista de productos que coinciden con los filtros.
        """
        if brand:
            products = self.product_repo.get_by_brand(brand)
        elif category:
            products = self.product_repo.get_by_category(category)
        else:
            products = self.product_repo.get_all()

        if brand and category:
            products = [p for p in products if p.category.lower() == category.lower()]

        return [self._entity_to_dto(p) for p in products]

    def create_product(self, product_dto: ProductDTO) -> ProductDTO:
        """
        Crea un nuevo producto en el catálogo.

        Convierte el DTO a una entidad de dominio, que valida las reglas
        de negocio, y luego lo guarda usando el repositorio.

        Args:
            product_dto (ProductDTO): Datos del producto a crear.

        Returns:
            ProductDTO: El producto creado con su ID asignado.

        Raises:
            InvalidProductDataError: Si los datos del producto son inválidos.
        """
        try:
            product = Product(
                id=None,
                name=product_dto.name,
                brand=product_dto.brand,
                category=product_dto.category,
                size=product_dto.size,
                color=product_dto.color,
                price=product_dto.price,
                stock=product_dto.stock,
                description=product_dto.description,
            )
        except ValueError as e:
            raise InvalidProductDataError(str(e))

        saved = self.product_repo.save(product)
        return self._entity_to_dto(saved)

    def update_product(self, product_id: int, product_dto: ProductDTO) -> ProductDTO:
        """
        Actualiza los datos de un producto existente.

        Args:
            product_id (int): ID del producto a actualizar.
            product_dto (ProductDTO): Nuevos datos del producto.

        Returns:
            ProductDTO: El producto con los datos actualizados.

        Raises:
            ProductNotFoundError: Si no existe el producto con ese ID.
            InvalidProductDataError: Si los nuevos datos son inválidos.
        """
        existing = self.product_repo.get_by_id(product_id)
        if not existing:
            raise ProductNotFoundError(product_id)

        try:
            updated = Product(
                id=product_id,
                name=product_dto.name,
                brand=product_dto.brand,
                category=product_dto.category,
                size=product_dto.size,
                color=product_dto.color,
                price=product_dto.price,
                stock=product_dto.stock,
                description=product_dto.description,
            )
        except ValueError as e:
            raise InvalidProductDataError(str(e))

        saved = self.product_repo.save(updated)
        return self._entity_to_dto(saved)

    def delete_product(self, product_id: int) -> bool:
        """
        Elimina un producto del catálogo.

        Args:
            product_id (int): ID del producto a eliminar.

        Returns:
            bool: True si se eliminó correctamente.

        Raises:
            ProductNotFoundError: Si no existe el producto con ese ID.
        """
        existing = self.product_repo.get_by_id(product_id)
        if not existing:
            raise ProductNotFoundError(product_id)
        return self.product_repo.delete(product_id)

    def _entity_to_dto(self, product: Product) -> ProductDTO:
        """
        Convierte una entidad de dominio Product a un ProductDTO.

        Método auxiliar privado para evitar repetición de código.

        Args:
            product (Product): Entidad de dominio a convertir.

        Returns:
            ProductDTO: DTO con los mismos datos del producto.
        """
        return ProductDTO(
            id=product.id,
            name=product.name,
            brand=product.brand,
            category=product.category,
            size=product.size,
            color=product.color,
            price=product.price,
            stock=product.stock,
            description=product.description,
        )
