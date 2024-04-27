from flask_smorest import abort, Blueprint
from flask.views import MethodView
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from db import db
from passlib.hash import pbkdf2_sha256
from models.user import UserModel
from schemas.user import UserSchema, UserUpdateSchema
from flask_jwt_extended import jwt_required, create_access_token, create_refresh_token, get_jwt_identity, get_jwt
from sqlalchemy import select
from datetime import datetime

user_blp = Blueprint("users", "users", description="Operations on users", url_prefix="/users")

@user_blp.route("/register")
class UserRegister(MethodView):
    @user_blp.arguments(UserSchema)
    @user_blp.response(200, UserSchema)
    def post(self, user_data):
        try:
            user = UserModel(
                username=user_data["username"],
                email=user_data["email"],
                password_hash=pbkdf2_sha256.hash(user_data["password_hash"]),
                role="user"
            )
            db.session.add(user)
            db.session.commit()
            # user.add_item()
        except IntegrityError:
            abort(400, message="A user with that username already exists.")
        except SQLAlchemyError:
            abort(500, message="An error occurred while adding the user.")

        return user
    
@user_blp.route("/login")
class UserLogin(MethodView):
    @user_blp.arguments(UserSchema)
    def post(self, user_data):
        user = db.session.execute(select(UserModel).where(UserModel.username == user_data["username"])).first()[0]
        if user and pbkdf2_sha256.verify(user_data["password_hash"], user.password_hash):
            access_token = create_access_token(identity={"id": user.id, "role": user.role}, fresh=True)
            refresh_token = create_refresh_token(identity={"id": user.id, "role": user.role})
            return {"access_token": access_token, "refresh_token": refresh_token}, 200

        abort(401, message="Invalid credentials.")

@user_blp.route('/me')
class UserProfile(MethodView):
    @staticmethod
    @jwt_required()
    @user_blp.response(200, UserSchema)
    def get():
        user_id = get_jwt_identity()["id"]
        user = UserModel.query.get(user_id)
        return user

    @user_blp.arguments(UserUpdateSchema)
    @jwt_required()
    @user_blp.response(200, UserUpdateSchema)
    def put(self, user_data):
        user = UserModel.query.get(get_jwt_identity()["id"])
        if user:
            user.username = user_data["username"]
            user.email = user_data["email"]
            user.password_hash = user_data["password_hash"]
            user.updated_at = datetime.now()
        else: 
            user = UserModel(id=get_jwt_identity()["id"], **user_data)

        # db.session.add(user)
        # db.session.commit()
        user.add_item()

        return user

def get_user_id():
    jwt = get_jwt()
    return jwt.get("sub").get("id")