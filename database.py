"""Este archivo configura la conexión a PostgreSQL con SQLAlchemy y 
define cómo cada request obtiene su propia sesión de base de datos"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from app.config import settings

"""es la conexión real a la base de datos, creada 
usando la URL que definimos en config.py"""
engine = create_engine(settings.database_url)

"""""fábrica" de sesiones. Cada sesión es como una 
transacción/conversación con la base de datos."""
"""autocommit=False significa que tú controlas 
    explícitamente cuándo hacer commit()"""
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

#la clase base de la que van a heredar todos tus modelos (tablas).
#Es el equivalente a usar @Entity
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

"""get_db() → esta es la parte más importante y la que más difiere de Spring Boot. FastAPI usa un 
sistema de "dependency injection" explícito vía funciones generador (yield). Cada vez que un endpoint 
necesite acceso a la base de datos, va a "pedir" get_db como dependencia, y FastAPI se encarga de:
-Crear una sesión nueva (db = SessionLocal()) 
-Entregársela al endpoint (yield db)
-Cerrarla automáticamente al terminar el request (db.close() en el finally), incluso si hubo una excepción"""