from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from src.core.settings import settings

engine = create_async_engine(
    settings.async_db_url,
    echo=False,
    pool_size=20,  # Increased pool size
    max_overflow=0,  # Disable overflow to prevent timeout issues
    pool_timeout=30,  # Connection timeout
    pool_pre_ping=True,  # Enable connection health checks
    pool_recycle=3600,  # Recycle connections after 1 hour
)


async_session_factory = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
)


async def get_db():
    async with async_session_factory() as session:
        yield session
