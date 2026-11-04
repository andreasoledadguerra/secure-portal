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
    expire_on_commit=False,  # evita recargar objetos tras commit
    autoflush=False,         # control manual del flush
)
