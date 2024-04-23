from db import db
from sqlalchemy import Column, String, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

class UserModel(db.Model):
    __tablename__ = "users"  

    id = Column(UUID(as_uuid=True), primary_key=True, server_default=db.text("uuid_generate_v4()"))
    username = Column(String(80), unique=True, nullable=False)
    email = Column(String(255), unique=True)
    password_hash = Column(String(256), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
