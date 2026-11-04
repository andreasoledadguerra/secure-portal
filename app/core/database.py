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

