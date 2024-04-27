from db import db
from models.common import CommonModel
from sqlalchemy import Column, Integer, String, DateTime, Enum
# from sqlalchemy.orm import relationship
from sqlalchemy.sql import func


class UserModel(CommonModel):
    __tablename__ = "users"  

    id = Column(Integer, primary_key=True)
    username = Column(String(80), unique=True, nullable=False)
    email = Column(String(255), unique=True)
    password_hash = Column(String(256), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
