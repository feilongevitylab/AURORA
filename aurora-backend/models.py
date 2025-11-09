from datetime import datetime
from sqlalchemy import Column, String, DateTime, Boolean, JSON
from sqlalchemy.orm import validates
from uuid import uuid4

from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, default=lambda: str(uuid4()))
    email = Column(String, unique=True, nullable=False, index=True)
    password_hash = Column(String, nullable=False)
    nickname = Column(String, nullable=False)
    gender = Column(String, nullable=False, default="unspecified")
    topics = Column(JSON, default=list)
    other_topic = Column(String, nullable=True)
    wearable_preference = Column(String, nullable=False, default="none")
    model_tier = Column(String, nullable=False, default="premium")
    is_registered = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_sign_in_at = Column(DateTime, nullable=True)

    @validates("email")
    def validate_email(self, key, value):
        return value.lower().strip()

    def to_dict(self):
        return {
            "id": self.id,
            "email": self.email,
            "nickname": self.nickname,
            "gender": self.gender,
            "topics": self.topics or [],
            "other_topic": self.other_topic,
            "wearable_preference": self.wearable_preference,
            "model_tier": self.model_tier,
            "is_registered": self.is_registered,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "last_sign_in_at": self.last_sign_in_at.isoformat() if self.last_sign_in_at else None,
        }

