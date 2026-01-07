import time
from functools import lru_cache
from typing import Literal, Optional

from pydantic_settings import BaseSettings
from sqlalchemy.exc import OperationalError
from sqlmodel import SQLModel, create_engine, Session


class DatabaseSettings(BaseSettings):
    """Database configuration settings"""

    driver: Literal["sqlite", "mysql", "postgresql"] = "sqlite"

    username: Optional[str] = "root"
    password: Optional[str] = ""
    host: Optional[str] = "localhost"
    port: Optional[int] = 3306
    name: Optional[str] = "api_db"

    max_retries: int = 10
    retry_delay: int = 3

    class Config:
        env_prefix = "DATABASE_"
        env_file = ".env"
        case_sensitive = False
        extra = "ignore"


def get_connection_string() -> str:
    settings = get_database_settings()
    if settings.driver == "sqlite":
        return f"sqlite:///{settings.name}.db"
    elif settings.driver == "mysql":
        return f"mysql+pymysql://{settings.username}:{settings.password}@{settings.host}:{settings.port}/{settings.name}"
    elif settings.driver == "postgresql":
        return f"postgresql+psycopg2://{settings.username}:{settings.password}@{settings.host}:{settings.port}/{settings.name}"
    else:
        raise ValueError(f"Unsupported database driver: {settings.driver}")

@lru_cache()
def get_database_settings() -> DatabaseSettings:
    """Get singleton database settings instance"""
    return DatabaseSettings()

@lru_cache()
def get_engine():
    engine = None
    settings = get_database_settings()
    for attempt in range(settings.max_retries):
        try:
            engine = create_engine(get_connection_string(), echo=True)
            # Teste la connexion
            with engine.connect() as conn:
                print("Connexion à la base de données réussie !")
            break
        except OperationalError:
            print(
                f"Connexion échouée (tentative {attempt + 1}/{settings.max_retries}), nouvelle tentative dans {settings.retry_delay}s...")
            time.sleep(settings.retry_delay)
    else:
        raise Exception("Impossible de se connecter à la base de données après plusieurs tentatives.")
    return engine

def create_db_and_tables():
    """Create database tables"""
    SQLModel.metadata.create_all(get_engine())

def get_session():
    """Dependency function that provides a database session per request"""
    with Session(get_engine()) as session:
        yield session