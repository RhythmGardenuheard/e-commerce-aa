from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from app.routers import auth, products
from app.config import settings
import json

app = FastAPI(title="E-commerce Dashboard API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/auth", tags=["authentication"])
app.include_router(products.router, prefix="/api", tags=["products"])

# WebSocket for real-time updates
@app.websocket("/ws/products")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            # Here you can handle incoming messages, e.g., broadcast updates
            # For simplicity, echo back
            await websocket.send_text(f"Message received: {data}")
    except WebSocketDisconnect:
        pass

@app.get("/")
async def root():
    return {"message": "E-commerce Dashboard API"}