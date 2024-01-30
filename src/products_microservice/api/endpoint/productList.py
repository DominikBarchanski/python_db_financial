from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from core.config import settings
from models.ProductsList import ProductsList
from schema.ProductsList import ProductsListCreate

router = APIRouter()


def get_db():
    engine = create_engine(settings.SQLALCHEMY_DATABASE_URI)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/create_product", status_code=201)
def create_product(product: ProductsListCreate, db: Session = Depends(get_db)):
    db_product = ProductsList(name=product.name, quantity=product.quantity, user_id=product.user_id,
                              group_id=product.group_id,category_id=product.category_id)
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


@router.get("/get_products", status_code=200)
def get_products(db: Session = Depends(get_db)):
    products = db.query(ProductsList).all()
    return products


@router.get("/get_user_product/{user_id}", status_code=200)
def get_user_product(user_id: int, db: Session = Depends(get_db)):
    user_product = db.query(ProductsList).filter(ProductsList.user_id == user_id).all()
    return user_product


