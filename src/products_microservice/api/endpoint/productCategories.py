from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from core.config import settings
from models.ProductCategory import ProductCategory

router = APIRouter()


def get_db():
    engine = create_engine(settings.SQLALCHEMY_DATABASE_URI)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/category", status_code=200)
def get_category(db: Session = Depends(get_db)):
    category = db.query(ProductCategory).all()
    return category
