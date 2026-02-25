from fastapi import FastAPI, HTTPException, Depends, status, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from typing import List, Optional
from jose import JWTError, jwt
import datetime
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# In-memory storage for demo
users_db = {}
products_db = {}
next_user_id = 1
next_product_id = 1

# Pydantic models
class UserCreate(BaseModel):
    email: str
    password: str

class UserLogin(BaseModel):
    email: str
    password: str

class ProductCreate(BaseModel):
    name: str
    description: str
    price: float
    stock: int

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    stock: Optional[int] = None

class Product(BaseModel):
    id: int
    name: str
    description: str
    price: float
    stock: int
    created_at: str

# JWT setup
SECRET_KEY = os.getenv("SECRET_KEY", "demo-secret-key")
ALGORITHM = "HS256"

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.datetime.utcnow() + datetime.timedelta(hours=24)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

# Dependency
def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer())):
    token = credentials.credentials
    payload = verify_token(token)
    return payload["sub"]

# FastAPI app
app = FastAPI(title="E-commerce Dashboard API", version="1.0.0")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# WebSocket connection manager
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

manager = ConnectionManager()

# Routes
@app.post("/auth/register")
async def register(user: UserCreate):
    global next_user_id
    # Check if user exists
    for u in users_db.values():
        if u["email"] == user.email:
            raise HTTPException(status_code=400, detail="Email already registered")

    user_id = next_user_id
    next_user_id += 1
    users_db[user_id] = {
        "id": user_id,
        "email": user.email,
        "password": user.password  # In real app, hash this
    }
    return {"message": "User registered successfully"}

@app.post("/auth/login")
async def login(user: UserLogin):
    for u in users_db.values():
        if u["email"] == user.email and u["password"] == user.password:
            access_token = create_access_token({"sub": str(u["id"])})
            return {"access_token": access_token, "token_type": "bearer"}

    raise HTTPException(status_code=401, detail="Invalid credentials")

@app.get("/api/products")
async def get_products(skip: int = 0, limit: int = 10):
    products = list(products_db.values())[skip:skip + limit]
    return products

@app.post("/api/products")
async def create_product(product: ProductCreate, current_user: str = Depends(get_current_user)):
    global next_product_id
    product_id = next_product_id
    next_product_id += 1

    new_product = {
        "id": product_id,
        "name": product.name,
        "description": product.description,
        "price": product.price,
        "stock": product.stock,
        "created_at": datetime.datetime.utcnow().isoformat()
    }

    products_db[product_id] = new_product
    await manager.broadcast(f"New product created: {product.name}")
    return {"id": product_id, "message": "Product created"}

@app.put("/api/products/{product_id}")
async def update_product(product_id: int, product: ProductUpdate, current_user: str = Depends(get_current_user)):
    if product_id not in products_db:
        raise HTTPException(status_code=404, detail="Product not found")

    update_data = {k: v for k, v in product.dict().items() if v is not None}
    if not update_data:
        raise HTTPException(status_code=400, detail="No fields to update")

    products_db[product_id].update(update_data)
    await manager.broadcast(f"Product {product_id} updated")
    return {"message": "Product updated"}

@app.delete("/api/products/{product_id}")
async def delete_product(product_id: int, current_user: str = Depends(get_current_user)):
    if product_id not in products_db:
        raise HTTPException(status_code=404, detail="Product not found")

    del products_db[product_id]
    await manager.broadcast(f"Product {product_id} deleted")
    return {"message": "Product deleted"}

@app.websocket("/ws/products")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.broadcast(f"Client says: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)

@app.get("/")
async def root():
    return {"message": "E-commerce Dashboard API", "status": "running"}

# Add some demo data
@app.post("/demo/setup")
async def setup_demo_data():
    # Create demo user
    users_db[1] = {"id": 1, "email": "demo@example.com", "password": "demo123"}

    # Create demo products
    products_db[1] = {
        "id": 1,
        "name": "Wireless Headphones",
        "description": "High-quality wireless headphones with noise cancellation",
        "price": 199.99,
        "stock": 50,
        "created_at": datetime.datetime.utcnow().isoformat()
    }
    products_db[2] = {
        "id": 2,
        "name": "Smart Watch",
        "description": "Fitness tracking smart watch with heart rate monitor",
        "price": 299.99,
        "stock": 30,
        "created_at": datetime.datetime.utcnow().isoformat()
    }

    return {"message": "Demo data created", "login": {"email": "demo@example.com", "password": "demo123"}}