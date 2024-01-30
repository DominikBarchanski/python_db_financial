from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from core.config import settings
from models.Expenses import Expense
from schema.Expense import ExpenseCreate
from models.User import User as UserModel
from models.UserGroupMembership import UserGroupMembership
from models.UsersGroups import UserGroups

router = APIRouter()


def get_db():
    engine = create_engine(settings.SQLALCHEMY_DATABASE_URI)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/add_expense", status_code=201)
def add_expense(expense: ExpenseCreate, db: Session = Depends(get_db)):
    print(expense)
    db_group = db.query(UserGroups).filter(UserGroups.id == expense.group_id).first()
    db_user = db.query(UserModel).filter(UserModel.id == expense.user_id).first()
    db_expense = Expense(user_id=db_user.id,name=expense.name, group_id=db_group.id, price=expense.price,
                         amount=expense.amount,
                         date=expense.datetime)
    db.add(db_expense)
    db.commit()
    db.refresh(db_expense)
    return db_expense


@router.get("/get_user_expenses/{user_id}", status_code=200)
def get_user_expenses(user_id: int, db: Session = Depends(get_db)):
    print(user_id)
    expenses = db.query(Expense).filter(Expense.user_id == user_id).all()
    return expenses


@router.get("/get_expenses/{group_id}", status_code=200)
def get_expenses(group_id: int, db: Session = Depends(get_db)):
    print(group_id)
    expenses = db.query(Expense).filter(Expense.group_id == group_id).all()
    return expenses


@router.delete("/delete_expense/{expense_id}", status_code=200)
def delete_expense(expense_id: int, db: Session = Depends(get_db)):
    expense = db.query(Expense).filter(Expense.id == expense_id).first()
    db.delete(expense)
    db.commit()
    return expense


@router.put("/edit_expense/{expense_id}", status_code=200)
def edit_expense(expense_id: int, expense: ExpenseCreate, db: Session = Depends(get_db)):
    db_expense = db.query(Expense).filter(Expense.id == expense_id).first()
    db_expense.user_id = expense.user_id
    db_expense.group_id = expense.group_id
    db_expense.amount = expense.amount
    db_expense.datetime = expense.datetime
    db.commit()
    db.refresh(db_expense)
    return db_expense
