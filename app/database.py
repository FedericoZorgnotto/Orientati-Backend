import motor.motor_asyncio
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.config import settings
from app.models.base import Base

SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL
MONGODB_CONNECTION_STRING = settings.MONGODB_CONNECTION_STRING

engine = create_engine(SQLALCHEMY_DATABASE_URL,
                       pool_size=1000,
                       max_overflow=2000,
                       pool_timeout=300
                       )
Base.metadata.create_all(bind=engine)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


client = motor.motor_asyncio.AsyncIOMotorClient(MONGODB_CONNECTION_STRING)
database = client.get_database(settings.MONGODB_DATABASE)


async def setup_database():
    if settings.MONGODB_STATS_COLLECTION not in await database.list_collection_names():
        await database.create_collection(settings.MONGODB_STATS_COLLECTION, timeseries={
            "timeField": "timestamp",
        }, expireAfterSeconds=60 * 60 * 24 * 30)


def get_mongodb():
    return database
