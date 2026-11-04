from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    AsyncSession,
)
from sqlalchemy.orm import declarative_base

from app.core.config import settings

# async engine for SQLAlchemy
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=False,          
    future=True,         
    pool_pre_ping=True, 
)

# Declarative base for SQLAlchemy models
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,  
    autoflush=False,        
)

Base = declarative_base()


# Dependency to get a database session
async def get_db() -> AsyncSession:
    """
    Entrega una sesión por petición y la cierra al terminar.
    FastAPI ejecuta el código después del 'yield' cuando termina la request.
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()