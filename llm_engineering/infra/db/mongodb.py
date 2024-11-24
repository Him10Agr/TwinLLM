from loguru import logger
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

from llm_engineering.settings import settings

class MongoDatabaseConnector:

    __slots__ = "_instance"
    _instance: MongoClient | None = None

    def __new__(cls, *args, **kwargs) -> MongoClient:

        if cls._instance is None:
            try:
                cls._instance = MongoClient(settings.DATABASE_HOST)
            except ConnectionFailure as e:
                logger.error(
                    f"Failed to connect to MongoDB database: {e}"
                )

                raise
            logger.info(f"Connection to MongoDB with URI successful: {settings.DATABASE_HOST}")

if __name__ != "__main__":

    connection = MongoDatabaseConnector()
