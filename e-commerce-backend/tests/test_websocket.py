import pytest
from fastapi.testclient import TestClient
from fastapi.websockets import WebSocket
import asyncio

@pytest.mark.asyncio
async def test_websocket():
    from app.main import app
    from fastapi.testclient import TestClient
    
    client = TestClient(app)
    
    # Test WebSocket connection
    with client.websocket_connect("/ws/products") as websocket:
        websocket.send_text("Hello")
        data = websocket.receive_text()
        assert data == "Message received: Hello"