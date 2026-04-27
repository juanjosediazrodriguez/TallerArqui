"""
Módulo de configuración de la base de datos.

Configura SQLAlchemy para usar SQLite como motor de base de datos.
Provee la sesión de base de datos como dependencia de FastAPI.
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from ...config import Config

# Motor de conexión a la base de datos SQLite.
# check_same_thread=False es necesario para SQLite en entornos multi-hilo como FastAPI.
engine = create_engine(
    Config.DATABASE_URL,
    connect_args={"check_same_thread": False},
)

# Fábrica de sesiones de base de datos.
# autocommit=False: los cambios se guardan solo al llamar session.commit()
# autoflush=False: los cambios no se envían automáticamente a la BD
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Clase base de la que heredan todos los modelos ORM.
# SQLAlchemy usa esta clase para conocer todas las tablas a crear.
Base = declarative_base()


def get_db():
    """
    Dependencia de FastAPI para obtener una sesión de base de datos.

    Usa el patrón 'yield' para garantizar que la sesión siempre se cierre
    al finalizar el request, incluso si ocurre una excepción.

    Yields:
        Session: Sesión de SQLAlchemy lista para usar.

    Example:
        En FastAPI se usa como dependencia:
        >>> def get_products(db: Session = Depends(get_db)):
        ...     return db.query(ProductModel).all()
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """
    Inicializa la base de datos creando todas las tablas definidas en los modelos.

    Esta función debe llamarse al iniciar la aplicación. Crea las tablas
    si no existen y carga los datos iniciales si la base está vacía.

    Note:
        Esta función importa los modelos dentro del cuerpo para asegurar
        que estén registrados en Base antes de create_all().
    """
    from .models import ProductModel, ChatMemoryModel  # noqa: F401
    from .init_data import load_initial_data

    Base.metadata.create_all(bind=engine)
    load_initial_data()
