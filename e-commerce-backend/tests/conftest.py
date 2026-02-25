import pytest
from fastapi.testclient import TestClient
from app.main import app
from prisma import Prisma
import asyncio

@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture(scope="session")
async def db():
    db = Prisma()
    await db.connect()
    yield db
    await db.disconnect()

@pytest.fixture
def client():
    return TestClient(app)