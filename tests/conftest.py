import asyncio
import os

import pytest
import pytest_asyncio
from core.database import db
from httpx import ASGITransport, AsyncClient
from main import app
from models.orm import Base, KeywordORM
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

# Use a test database
TEST_DB_URL = "sqlite+aiosqlite:///./test_rating.db"

@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest_asyncio.fixture(scope="session")
async def test_engine():
    # Ensure we use the test DB
    engine = create_async_engine(TEST_DB_URL, echo=False)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield engine
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await engine.dispose()
    if os.path.exists("./test_rating.db"):
        os.remove("./test_rating.db")

@pytest_asyncio.fixture
async def session(test_engine):
    session_factory = async_sessionmaker(test_engine, class_=AsyncSession, expire_on_commit=False)
    async with session_factory() as session:
        # CLEAN SLATE for every test
        from sqlalchemy import delete
        await session.execute(delete(KeywordORM))
        await session.commit()
        yield session

@pytest_asyncio.fixture
async def client(session, test_engine):
    # USE CLEAN DEPENDENCY OVERRIDES instead of monkeypatching where possible
    async def override_get_session():
        yield session

    app.dependency_overrides[db.get_session] = override_get_session

    # ALSO override the singleton's engine and factory to ensure non-DI methods use test DB
    original_engine = db.engine
    original_factory = db.session_factory

    db.engine = test_engine
    db.session_factory = async_sessionmaker(test_engine, expire_on_commit=False)

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac

    app.dependency_overrides.clear()
    db.engine = original_engine
    db.session_factory = original_factory
