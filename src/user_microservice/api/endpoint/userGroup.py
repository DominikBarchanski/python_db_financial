from typing import List

from models.User import User as UserModel
from models.UserGroupMembership import UserGroupMembership
from models.UsersGroups import UserGroups
from schema.UserGroupMembership import UserGroupMembershipSchema, \
    UserGroupMembershipAddSchema
from schema.UsersGroups import UsersGroupsCreate
from core.config import settings
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, joinedload
from sqlalchemy.orm import sessionmaker

router = APIRouter()


def get_db():
    engine = create_engine(settings.SQLALCHEMY_DATABASE_URI)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/create_group", status_code=201)
def create_group(group: UsersGroupsCreate, db: Session = Depends(get_db)):
    db_group = db.query(UserGroups).filter(UserGroups.name == group.name).first()
    if db_group:
        raise HTTPException(status_code=400, detail="Group already exists")
    db_group = UserGroups(name=group.name, owner_id=group.owner_id)
    db.add(db_group)
    db.commit()
    db.refresh(db_group)
    db_group_membership = UserGroupMembership(name=group.name, user_id=group.owner_id, group_id=db_group.id)
    db.add(db_group_membership)
    db.commit()
    db.refresh(db_group)
    return db_group


@router.post("/add_user_to_group", status_code=201)
def add_user_to_group(user_group: UserGroupMembershipAddSchema, db: Session = Depends(get_db)):
    print(user_group)
    db_find_by_email = db.query(UserModel).filter(UserModel.email == user_group.email).first()
    print(db_find_by_email)
    if db_find_by_email:
        db_user_group = db.query(UserGroupMembership).filter(UserGroupMembership.user_id == db_find_by_email.id,
                                                             UserGroupMembership.group_id == user_group.group_id).first()
        print(db_user_group)
        if db_user_group:
            raise HTTPException(status_code=400, detail="User already in group")
    else:
        raise HTTPException(status_code=400, detail="User does not exist")

    db_user_group = db.query(UserGroupMembership).filter(UserGroupMembership.group_id == user_group.group_id).first()
    print(db_user_group)
    if not db_user_group:
        raise HTTPException(status_code=400, detail="Group does not exist")
    db_user_group = UserGroupMembership(user_id=db_find_by_email.id, group_id=user_group.group_id, name=db_user_group.name)
    print(db_user_group)
    db.add(db_user_group)
    db.commit()
    db.refresh(db_user_group)
    return db_user_group


@router.get("/get_groups/{user_id}", response_model=List[UserGroupMembershipSchema], status_code=200)
def get_groups(user_id: int, db: Session = Depends(get_db)):
    print(user_id)
    groups = db.query(UserGroupMembership).filter(UserGroupMembership.user_id == user_id).all()
    return groups


@router.get("/get_user_group/{group_id}", status_code=200)
def get_user_group(group_id: int, db: Session = Depends(get_db)):
    group_memberships = (
        db.query(UserGroupMembership)
        .join(UserModel, UserModel.id == UserGroupMembership.user_id)
        .join(UserGroups, UserGroups.id == UserGroupMembership.group_id)
        .options(joinedload(UserGroupMembership.user))
        .filter(UserGroupMembership.group_id == group_id)
        .all()
    )
    print(group_memberships)
    group_memberships_dict = {
            "group_id": group_id,
            "group_owner": group_memberships[0].group.owner_id,
            "user": [{
                "name": membership.user.username,
                "email": membership.user.email,
                "id": membership.user.id
                # Add other fields from the User model as needed
            }for membership in group_memberships
            ]
        }

    return group_memberships_dict

@router.post("/delete_user_from_group", status_code=201)
def delete_user_from_group(user_group: UserGroupMembershipAddSchema, db: Session = Depends(get_db)):
    db_find_by_email = db.query(UserModel).filter(UserModel.email == user_group.email).first()
    if db_find_by_email:
        db_user_group = db.query(UserGroupMembership).filter(UserGroupMembership.user_id == db_find_by_email.id,
                                                             UserGroupMembership.group_id == user_group.group_id).first()
        if not db_user_group:
            raise HTTPException(status_code=400, detail="User not in group")
    else:
        raise HTTPException(status_code=400, detail="User does not exist")

    db_user_group = db.query(UserGroupMembership).filter(UserGroupMembership.group_id == user_group.group_id).first()
    if not db_user_group:
        raise HTTPException(status_code=400, detail="Group does not exist")
    db.delete(db_user_group)
    db.commit()
    return db_user_group