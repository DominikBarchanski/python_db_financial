from sqlalchemy import create_engine

from sqlalchemy.orm import sessionmaker

from core.config import settings

engine = create_engine(settings.SQLALCHEMY_DATABASE_URI)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)



def create_database_tables():
    from models.base import Base
    from models.UserGroupMembership import UserGroupMembership
    from models.User import User
    from models.UsersGroups import UserGroups
    from models.Expenses import Expense
    from models.Balance import Balance
    from models.ProductsList import ProductsList
    from models.ProductCategory import ProductCategory
    from models.Tokens import Tokens
    Base.metadata.create_all(bind=engine)

create_database_tables()