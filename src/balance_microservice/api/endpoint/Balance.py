from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from core.config import settings
from models.Balance import Balance
from schema.Balance import BalanceCreate

router = APIRouter()


def get_db():
    engine = create_engine(settings.SQLALCHEMY_DATABASE_URI)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/add_balance", status_code=201)
def add_balance(balance: BalanceCreate, db: Session = Depends(get_db)):
    db_balance = Balance(group_id=balance.group_id, balance=balance.balance, datetime=balance.datetime)
    db.add(db_balance)
    db.commit()
    db.refresh(db_balance)
    return db_balance

@router.get("/get_balance/{group_id}", status_code=200)
def get_balance(group_id: int, db: Session = Depends(get_db)):
    balance = db.query(Balance).filter(Balance.group_id == group_id).all()
    return balance


