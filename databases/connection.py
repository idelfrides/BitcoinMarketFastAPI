
from os import getenv
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

database_url = getenv("DATABASE_URL")

engine = create_async_engine(database_url)
async_session = sessionmaker(engine, class_=AsyncSession)