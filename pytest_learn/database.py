"""
Engine + сессия для настоящего Postgres (docker-compose: postgres_test).
Это "бэкенд"-слой — то, что на реальном проекте тебе дали бы готовым.
Твои тестовые фикстуры (dependency_overrides) будут строиться СВЕРХУ этого,
не трогая этот файл.
"""

from config import Settings
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

settings = Settings(_env_file=".env.local")


class Base(DeclarativeBase):
    pass


engine = create_engine(settings.database_url)
SessionLocal = sessionmaker(bind=engine)


def get_db():
    db = SessionLocal()
    db.rollback()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()
