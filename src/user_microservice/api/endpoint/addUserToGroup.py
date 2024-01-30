from fastapi import APIRouter, Depends, HTTPException
from models.UserGroupMembership import UserGroupMembership
from schema.UserGroupMembership import UserGroupMembershipCreate
from sqlalchemy import create_engine
from core.config import settings
from sqlalchemy.orm import sessionmaker, Session

router = APIRouter()


def get_db():
    engine = create_engine(settings.SQLALCHEMY_DATABASE_URI)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/add_user_to_groups", status_code=201)
def add_user_to_group(user_group: UserGroupMembershipCreate, db: Session = Depends(get_db)):
    db_user_group = db.query(UserGroupMembership).filter(UserGroupMembership.user_id == user_group.user_id,
                                                         UserGroupMembership.group_id == user_group.group_id).first()
    if db_user_group:
        raise HTTPException(status_code=400, detail="User already in group")
    db_user_group = UserGroupMembership(user_id=user_group.user_id, group_id=user_group.group_id)
    db.add(db_user_group)
    db.commit()
    db.refresh(db_user_group)
    return db_user_group

@router.get("/get_users_in_group/{user_id}", status_code=200)
def get_users_in_group(user_id: int, db: Session = Depends(get_db)):
    users_in_group = db.query(UserGroupMembership).filter(UserGroupMembership.user_id == user_id).all()
    return users_in_group
