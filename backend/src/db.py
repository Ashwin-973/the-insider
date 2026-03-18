from collections.abc import AsyncGenerator
import uuid
from dotenv import load_dotenv
import os

from sqlalchemy import Column,String,Text,DateTime,ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.asyncio import AsyncSession,create_async_engine,async_sessionmaker
from sqlalchemy.orm import DeclarativeBase,relationship

from fastapi_users.db import SQLAlchemyUserDatabase,SQLAlchemyBaseUserTableUUID
from fastapi import Depends

from datetime import datetime

load_dotenv()

DEFAULT_SQLITE_URL="sqlite+aiosqlite:///./test.db"


def is_truthy(value:str|None)->bool:
    return value is not None and value.lower() in {"1","true","yes","on"}

def normalize_database_url(raw_url:str|None)->str:
    if not raw_url:
        return DEFAULT_SQLITE_URL

    if raw_url.startswith("postgresql+"):
        return raw_url

    if raw_url.startswith("postgres://"):
        return raw_url.replace("postgres://","postgresql+psycopg://",1)

    if raw_url.startswith("postgresql://"):
        return raw_url.replace("postgresql://","postgresql+psycopg://",1)

    return raw_url


def should_use_production_database()->bool:
    return (
        is_truthy(os.getenv("RENDER"))  #* render sets it when app is running on render
        or os.getenv("APP_ENV","").lower()=="production"
        or os.getenv("ENVIRONMENT","").lower()=="production"
        or is_truthy(os.getenv("USE_PRODUCTION_DB"))
    )


def get_database_url()->str:
    raw_database_url=os.getenv("DATABASE_URL")

    if raw_database_url and should_use_production_database():
        return normalize_database_url(raw_database_url)

    return DEFAULT_SQLITE_URL


DATABASE_URL=get_database_url()
IS_SQLITE=DATABASE_URL.startswith("sqlite")


class Base(DeclarativeBase): 
    pass

class User(SQLAlchemyBaseUserTableUUID,Base):
    posts=relationship("Post",back_populates="user")

class Post(Base): #?why can't I directly inherit from DeclarativeBase?
    __tablename__="posts"

    id=Column(UUID(as_uuid=True),primary_key=True,default=uuid.uuid4)
    user_id=Column(UUID(as_uuid=True),ForeignKey("user.id"),nullable=False)
    caption=Column(Text)
    url=Column(String,nullable=False)
    file_type=Column(String,nullable=False)
    file_name=Column(String,nullable=False)
    created_at=Column(DateTime,default=datetime.utcnow)

    user=relationship("User",back_populates="posts")


engine=create_async_engine(DATABASE_URL,pool_pre_ping=True)
async_session_maker=async_sessionmaker(engine,expire_on_commit=False)

async def create_db_and_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

        if IS_SQLITE:
            columns_result=await conn.exec_driver_sql("PRAGMA table_info(posts)") 
            columns={row[1] for row in columns_result.fetchall()}

        if "user_id" not in columns:
            await conn.exec_driver_sql("ALTER TABLE posts ADD COLUMN user_id UUID")

async def get_async_session()->AsyncGenerator[AsyncSession,None]:
    async with async_session_maker() as session:
        yield session

async def get_user_db(session:AsyncSession=Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session,User)
