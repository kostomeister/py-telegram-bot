from sqlalchemy.ext.asyncio import AsyncSession

from db_handler.database import SessionLocal


# Створення асинхронної сесії
async def get_db() -> AsyncSession:
    db = SessionLocal()

    try:
        yield db
    finally:
        await db.close()
