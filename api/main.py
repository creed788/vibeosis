from fastapi import FastAPI, HTTPException, Depends
from database import SessionLocal
from models import Product
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List
from database import Base, engine
from datetime import datetime


app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class ProductCreate(BaseModel):
    name: str
    category: str
    description: str
    product_image: str
    sku: str
    unit_of_measure: str
    lead_time: int

class ProductResponse(ProductCreate):
    id: int
    created_date: datetime
    updated_date: datetime
    
    class Config:
        orm_mode = True
        from_attributes = True

Base.metadata.create_all(bind=engine)

@app.get("/product/list", response_model=List[ProductResponse])
def list_products(page: int = 1, db: Session = Depends(get_db)):
    products = db.query(Product).offset((page - 1) * 10).limit(10).all()
    return products

@app.get("/product/{pid}/info", response_model=ProductResponse)
def get_product(pid: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == pid).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@app.post("/product/add", response_model=ProductResponse)
def add_product(product: ProductCreate, db: Session = Depends(get_db)):
    new_product = Product(**product.dict())
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product

@app.put("/product/{pid}/update", response_model=ProductResponse)
def update_product(pid: int, product: ProductCreate, db: Session = Depends(get_db)):
    existing_product = db.query(Product).filter(Product.id == pid).first()
    if not existing_product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    for key, value in product.dict().items():
        setattr(existing_product, key, value)
    
    db.commit()
    db.refresh(existing_product)
    return existing_product
