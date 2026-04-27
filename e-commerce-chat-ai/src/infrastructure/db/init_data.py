"""
Módulo para cargar datos iniciales en la base de datos.

Crea 10 productos de ejemplo (zapatos) si la base de datos está vacía.
Solo se ejecuta una vez: en el arranque de la aplicación.
"""

from .database import SessionLocal
from .models import ProductModel


def load_initial_data():
    """
    Carga productos de ejemplo en la base de datos si está vacía.

    Verifica primero si ya existen productos para evitar duplicar datos
    en cada reinicio de la aplicación. Si la tabla está vacía, inserta
    10 zapatos de distintas marcas, categorías y tallas.

    Note:
        Esta función es idempotente: ejecutarla múltiples veces no
        duplica los datos porque comprueba si ya existen registros.
    """
    db = SessionLocal()
    try:
        # Verificar si ya hay productos cargados
        count = db.query(ProductModel).count()
        if count > 0:
            return  # Ya hay datos, no hacemos nada

        # Crear 10 productos de ejemplo variados
        productos_iniciales = [
            ProductModel(
                name="Air Zoom Pegasus 40",
                brand="Nike",
                category="Running",
                size="42",
                color="Negro/Blanco",
                price=120.0,
                stock=5,
                description="Zapatilla de running con amortiguación Air Zoom para corredores de larga distancia.",
            ),
            ProductModel(
                name="Ultraboost 22",
                brand="Adidas",
                category="Running",
                size="41",
                color="Blanco",
                price=150.0,
                stock=3,
                description="Zapatilla premium con tecnología Boost para máxima energía de retorno.",
            ),
            ProductModel(
                name="Suede Classic",
                brand="Puma",
                category="Casual",
                size="40",
                color="Azul marino",
                price=80.0,
                stock=10,
                description="Zapatilla clásica de cuero gamuza, icónica desde los años 70.",
            ),
            ProductModel(
                name="Chuck Taylor All Star",
                brand="Converse",
                category="Casual",
                size="43",
                color="Rojo",
                price=65.0,
                stock=8,
                description="El clásico de los clásicos. Lona resistente y suela de goma vulcanizada.",
            ),
            ProductModel(
                name="Old Skool",
                brand="Vans",
                category="Casual",
                size="39",
                color="Negro/Blanco",
                price=75.0,
                stock=12,
                description="Zapatilla de skate con la icónica franja lateral de Vans.",
            ),
            ProductModel(
                name="Gel-Nimbus 25",
                brand="Asics",
                category="Running",
                size="44",
                color="Gris/Naranja",
                price=140.0,
                stock=4,
                description="Zapatilla de running de alta amortiguación con tecnología GEL.",
            ),
            ProductModel(
                name="990v5",
                brand="New Balance",
                category="Casual",
                size="42",
                color="Gris",
                price=175.0,
                stock=6,
                description="Zapatilla premium fabricada en USA con cuero y malla de alta calidad.",
            ),
            ProductModel(
                name="Air Force 1 '07",
                brand="Nike",
                category="Casual",
                size="41",
                color="Blanco",
                price=100.0,
                stock=15,
                description="El ícono del basketball reconvertido en zapatilla casual de moda.",
            ),
            ProductModel(
                name="Stan Smith",
                brand="Adidas",
                category="Formal",
                size="40",
                color="Blanco/Verde",
                price=90.0,
                stock=7,
                description="Zapatilla minimalista de cuero, elegante y versátil para cualquier ocasión.",
            ),
            ProductModel(
                name="Speedcat OG",
                brand="Puma",
                category="Casual",
                size="43",
                color="Rojo/Blanco",
                price=110.0,
                stock=9,
                description="Zapatilla retro inspirada en el automovilismo, con perfil bajo y diseño deportivo.",
            ),
        ]

        db.add_all(productos_iniciales)
        db.commit()

    finally:
        db.close()
