from datetime import datetime, timedelta
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status, Header
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from passlib.context import CryptContext
from pydantic import ValidationError
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from core.config import settings
from models.User import User
from models.Tokens import Tokens
from schema.User import UserCreate, UserBase, UserLogin
from schema.Tokens import TokensCreate, TokensBase

router = APIRouter()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")


def get_db():
    engine = create_engine(settings.SQLALCHEMY_DATABASE_URI)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_access_token(db_user, expires_delta: timedelta):
    expires_at = datetime.utcnow() + expires_delta
    print(db_user)
    to_encode = {"id": str(db_user.id), "username": str(db_user.username)}
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
    return encoded_jwt, expires_at


@router.post("/register", status_code=201)
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    # Sprawdź, czy użytkownik o takiej nazwie użytkownika już istnieje
    db_user = db.query(User).filter(User.username == user_data.username).first()
    if user_data.password == "":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Password cannot be empty")
    if user_data.username == "":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username cannot be empty")
    if len(user_data.username) < 3:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username too short")
    if user_data.email == "":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email cannot be empty")
    if db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already taken")

    hashed_password = pwd_context.hash(user_data.password)  # Zaszyfruj hasło
    new_user = User(username=user_data.username, hashed_password=hashed_password, email=user_data.email)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    expires_delta = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    token, expires_at = create_access_token(new_user, expires_delta)
    db_token = Tokens(token=token, expires_at=expires_at, user_id=new_user.id)
    db.add(db_token)
    db.commit()
    db.refresh(db_token)

    return {"bearerToken": db_token.token}


@router.post("/login")
def login(user_data: Optional[dict] = None, authorization: str = Header(None), db: Session = Depends(get_db)):
    print(authorization)
    if authorization and authorization.startswith("Bearer "):
        # Logowanie za pomocą tokenu Bearer
        token = authorization[7:]  # Pobierz token bez prefiksu "Bearer "
        print(token)
        decoded_token = None
        try:
            decoded_token = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        except jwt.JWTError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

        user_id = int(decoded_token["id"])
        db_user = db.query(User).filter(User.id == user_id).first()
        if not db_user:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid user")

        db_token = db.query(Tokens).filter(Tokens.user_id == db_user.id, Tokens.token == token).first()
        if not db_token:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid token")

        if db_token.is_expired:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Token has expired")

        # Przedłuż ważność istniejącego tokenu o 1 dzień
        expires_delta = timedelta(days=7)
        db_token.expires_at = datetime.now() + expires_delta
        db.commit()

        return {"bearerToken": db_token.token}

    else:
        # Logowanie za pomocą loginu i hasła
        print(user_data)
        if user_data is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No credentials provided")

        try:
            user_data_model = UserLogin(**user_data)
        except ValidationError:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid credentials format")

        db_user = db.query(User).filter(User.username == user_data_model.username).first()
        if not db_user:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid credentials")
        if not pwd_context.verify(user_data_model.password, db_user.hashed_password):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect password")
        token = db.query(Tokens).filter(Tokens.user_id == db_user.id).first()
        if token:
            # Przedłuż ważność istniejącego tokenu o 1 dzień
            expires_delta = timedelta(days=7)
            token.expires_at = datetime.now() + expires_delta
            db.commit()
            token = token.token

        else:
            # Tworzenie nowego tokenu
            expires_delta = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
            token, expires_at = create_access_token(db_user, expires_delta)
            db_token = Tokens(token=token, expires_at=expires_at, user_id=db_user.id)
            db.add(db_token)
            db.commit()
            db.refresh(db_token)
            token = db_token.token

        return {"bearerToken": token}


@router.get("/protected")
def protected_route(token: str = Depends(oauth2_scheme)):
    # Sprawdzanie tokenu Bearer w nagłówku Authorization
    try:
        decoded_token = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        user_id = int(decoded_token["sub"])
        # Sprawdzanie czy użytkownik istnieje w bazie danych
        # ... kod sprawdzający użytkownika ...
        return {"message": "Protected route"}

    except jwt.JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
