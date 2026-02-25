from fastapi import APIRouter, Depends, HTTPException
from models import Product, ProductCreate
from dependencies import get_current_user
from routers.auth import get_prisma
from prisma import Prisma

router = APIRouter(dependencies=[Depends(get_current_user)])

@router.get("/products", response_model=list[Product])
async def read_products(skip: int = 0, limit: int = 100, db: Prisma = Depends(get_prisma)):
    products = await db.product.find_many(skip=skip, take=limit)
    return products

@router.get("/products/{product_id}", response_model=Product)
async def read_product(product_id: int, db: Prisma = Depends(get_prisma)):
    product = await db.product.find_unique(where={"id": product_id})
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.post("/products", response_model=Product)
async def create_product(product: ProductCreate, db: Prisma = Depends(get_prisma)):
    return await db.product.create(data=product.dict())

@router.put("/products/{product_id}", response_model=Product)
async def update_product(product_id: int, product: ProductCreate, db: Prisma = Depends(get_prisma)):
    existing_product = await db.product.find_unique(where={"id": product_id})
    if existing_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return await db.product.update(where={"id": product_id}, data=product.dict())

@router.delete("/products/{product_id}")
async def delete_product(product_id: int, db: Prisma = Depends(get_prisma)):
    existing_product = await db.product.find_unique(where={"id": product_id})
    if existing_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    await db.product.delete(where={"id": product_id})
    return {"message": "Product deleted"}