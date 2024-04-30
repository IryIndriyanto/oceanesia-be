from db import db


class UserModel(db.Model):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    username = db.Column(db.String(255), unique=True, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(
        db.DateTime(timezone=True), default=db.func.now(), nullable=False
    )
    updated_at = db.Column(
        db.DateTime(timezone=True), default=db.func.now(), onupdate=db.func.now()
    )
