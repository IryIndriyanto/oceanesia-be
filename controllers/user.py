from db import db
from flask import jsonify
from flask_smorest import Blueprint
from models.user import UserModel
from schemas.user import UserSchema, UserLoginSchema
from sqlalchemy.exc import IntegrityError
from passlib.hash import pbkdf2_sha256
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt_identity,
)

blp = Blueprint("users", "users", description="data of users", url_prefix="/users")


@blp.route("/", methods=["POST"])
@blp.arguments(UserSchema)
@blp.response(200)
def user_register(user_data):
    try:
        new_user = UserModel(
            username=user_data["username"],
            email=user_data["email"],
            password_hash=pbkdf2_sha256.hash(user_data["password"]),
        )
        db.session.add(new_user)
        db.session.commit()
        return jsonify({"message": "User created"}), 200

    except IntegrityError:
        return jsonify({"Error": "Username or email already exists."}), 400


@blp.route("/login", methods=["POST"])
@blp.arguments(UserLoginSchema)
@blp.response(200)
def user_login(user_data):
    user = UserModel.query.filter_by(username=user_data["username"]).first()
    if user and pbkdf2_sha256.verify(user_data["password"], user.password_hash):
        access_token = create_access_token(identity=user.id, fresh=True)
        refresh_token = create_refresh_token(identity=user.id)
        return (
            jsonify({"access_token": access_token, "refresh_token": refresh_token}),
            200,
        )
    return jsonify({"message": "Invalid credentials"}), 401


@blp.route("/me", methods=["GET"])
@jwt_required()
@blp.response(200)
def get_user_profile():
    user_id = get_jwt_identity()
    user = db.session.get(UserModel, user_id)
    if user:
        return jsonify({"user_id":user.id , "username": user.username, "email": user.email}), 200
    return jsonify({"message": "User not found"}), 404


@blp.route("/me", methods=["PUT"])
@blp.arguments(UserSchema)
@jwt_required()
@blp.response(200)
def edit_user_profile(user_data):
    user_id = get_jwt_identity()
    user = db.session.get(UserModel, user_id)
    if user:
        try:
            updated_data = {
                "username": user_data.get("username", user.username),
                "email": user_data.get("email", user.email),
            }

            if "password" in user_data:
                updated_data["password_hash"] = pbkdf2_sha256.hash(
                    user_data["password"]
                )

            UserModel.query.filter_by(id=user_id).update(updated_data)
            db.session.commit()
            return jsonify({"message": "User updated"}), 200
        except IntegrityError:
            return jsonify({"Error": "Username or email already exists."}), 400
    return jsonify({"message": "User not found"}), 404
