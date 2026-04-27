"""
Módulo del repositorio concreto de productos con SQLAlchemy.

Implementa la interfaz IProductRepository usando SQLite como
motor de base de datos a través de SQLAlchemy ORM.
"""

from typing import List, Optional
from sqlalchemy.orm import Session
from ...domain.entities import Product
from ...domain.repositories import IProductRepository
from ..db.models import ProductModel


class SQLProductRepository(IProductRepository):
    """
    Implementación concreta del repositorio de productos usando SQLAlchemy.

    Traduce entre entidades del dominio (Product) y modelos ORM (ProductModel).
    Esta separación permite que el dominio permanezca independiente de
    la tecnología de base de datos utilizada.

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

    def get_all(self) -> List[Product]:
        """
        Obtiene todos los productos de la base de datos.

        Returns:
            List[Product]: Lista de entidades Product. Lista vacía si no hay.
        """
        models = self.db.query(ProductModel).all()
        return [self._model_to_entity(m) for m in models]

    def get_by_id(self, product_id: int) -> Optional[Product]:
        """
        Busca un producto por su ID en la base de datos.

        Args:
            product_id (int): ID del producto a buscar.

        Returns:
            Optional[Product]: La entidad Product si existe, None si no.
        """
        model = self.db.query(ProductModel).filter(
            ProductModel.id == product_id
        ).first()
        return self._model_to_entity(model) if model else None

    def get_by_brand(self, brand: str) -> List[Product]:
        """
        Busca todos los productos de una marca específica.

        La búsqueda es insensible a mayúsculas/minúsculas usando ilike.

        Args:
            brand (str): Nombre de la marca a filtrar.

        Returns:
            List[Product]: Lista de productos de esa marca.
        """
        models = self.db.query(ProductModel).filter(
            ProductModel.brand.ilike(f"%{brand}%")
        ).all()
        return [self._model_to_entity(m) for m in models]

    def get_by_category(self, category: str) -> List[Product]:
        """
        Busca todos los productos de una categoría específica.

        Args:
            category (str): Nombre de la categoría a filtrar.

        Returns:
            List[Product]: Lista de productos de esa categoría.
        """
        models = self.db.query(ProductModel).filter(
            ProductModel.category.ilike(f"%{category}%")
        ).all()
        return [self._model_to_entity(m) for m in models]

    def save(self, product: Product) -> Product:
        """
        Guarda o actualiza un producto en la base de datos.

        Si el producto tiene ID, lo actualiza. Si no tiene ID (es nuevo),
        lo inserta y SQLAlchemy le asigna un ID automáticamente.

        Args:
            product (Product): Entidad de dominio a persistir.

        Returns:
            Product: La entidad guardada con su ID asignado.
        """
        if product.id:
            # Actualizar producto existente
            model = self.db.query(ProductModel).filter(
                ProductModel.id == product.id
            ).first()
            if model:
                model.name = product.name
                model.brand = product.brand
                model.category = product.category
                model.size = product.size
                model.color = product.color
                model.price = product.price
                model.stock = product.stock
                model.description = product.description
        else:
            # Crear nuevo producto
            model = self._entity_to_model(product)
            self.db.add(model)

        self.db.commit()
        self.db.refresh(model)  # Recarga el objeto para obtener el ID generado
        return self._model_to_entity(model)

    def delete(self, product_id: int) -> bool:
        """
        Elimina un producto de la base de datos por su ID.

        Args:
            product_id (int): ID del producto a eliminar.

        Returns:
            bool: True si se eliminó, False si no existía.
        """
        model = self.db.query(ProductModel).filter(
            ProductModel.id == product_id
        ).first()
        if not model:
            return False
        self.db.delete(model)
        self.db.commit()
        return True

    def _model_to_entity(self, model: ProductModel) -> Product:
        """
        Convierte un modelo ORM de SQLAlchemy a una entidad del dominio.

        Este método de conversión garantiza que el dominio nunca trabaje
        directamente con objetos de SQLAlchemy.

        Args:
            model (ProductModel): Modelo ORM de la base de datos.

        Returns:
            Product: Entidad de dominio equivalente.
        """
        return Product(
            id=model.id,
            name=model.name,
            brand=model.brand,
            category=model.category,
            size=model.size,
            color=model.color,
            price=model.price,
            stock=model.stock,
            description=model.description,
        )

    def _entity_to_model(self, product: Product) -> ProductModel:
        """
        Convierte una entidad del dominio a un modelo ORM de SQLAlchemy.

        Args:
            product (Product): Entidad de dominio a convertir.

        Returns:
            ProductModel: Modelo ORM listo para persistir en la base de datos.
        """
        return ProductModel(
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
