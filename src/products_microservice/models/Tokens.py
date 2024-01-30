from datetime import datetime, timedelta

from .base import Base
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship


class Tokens(Base):
    __tablename__ = "tokens"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    token = Column(String, unique=True, index=True)
    expires_at = Column(DateTime)

    user = relationship("User", back_populates="tokens")

    @property
    def is_expired(self):
        return datetime.now() > self.expires_at

    @staticmethod
    def generate_token(user_id: int, token: str, expires_in_minutes: int):
        expires_at = datetime.utcnow() + timedelta(minutes=expires_in_minutes)
        return Tokens(user_id=user_id, token=token, expires_at=expires_at)