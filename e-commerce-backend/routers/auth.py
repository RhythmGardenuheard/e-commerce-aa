from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from passlib.context import CryptContext
from models import UserCreate, User, Token
from dependencies import create_access_token
from config import settings
from prisma import Prisma
import asyncio

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

async def get_prisma():
    db = Prisma()
    await db.connect()
    try:
        yield db
    finally:
        await db.disconnect()

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

@router.post("/register", response_model=User)
async def register(user: UserCreate, db: Prisma = Depends(get_prisma)):
    db_user = await db.user.find_unique(where={"username": user.username})
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    db_user = await db.user.find_unique(where={"email": user.email})
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_password = get_password_hash(user.password)
    new_user = await db.user.create(data={
        "username": user.username,
        "email": user.email,
        "password": hashed_password
    })
    return new_user

@router.post("/token", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Prisma = Depends(get_prisma)):
    user = await db.user.find_unique(where={"username": form_data.username})
    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}