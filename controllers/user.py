from flask_smorest import abort, Blueprint
from flask.views import MethodView
from supabase_py import create_client
from passlib.hash import pbkdf2_sha256
from schemas import UserSchema, UserUpdateSchema
from flask_jwt_extended import jwt_required, create_access_token, create_refresh_token, get_jwt_identity, get_jwt
from datetime import datetime

supabase_url = 'YOUR_SUPABASE_URL'
supabase_key = 'YOUR_SUPABASE_KEY'
supabase = create_client(supabase_url, supabase_key)

user_blp = Blueprint("users", "users", description="Operations on users", url_prefix="/users")

@user_blp.route("/register")
class UserRegister(MethodView):
    @user_blp.arguments(UserSchema)
    @user_blp.response(200, UserSchema)
    def post(self, user_data):
        password_hash = pbkdf2_sha256.hash(user_data["password_hash"])
        user_data["password_hash"] = password_hash
        user_data["role"] = "user"
        
        # Insert user data into Supabase
        response = supabase.table('users').insert(user_data).execute()
        
        if response['status'] == 201:
            return response['data']
        else:
            abort(response['status'], message=response['error']['message'])
    
@user_blp.route("/login")
class UserLogin(MethodView):
    @user_blp.arguments(UserSchema)
    def post(self, user_data):
        response = supabase.table('users').select().eq('username', user_data["username"]).execute()
        user = response['data'][0] if response['data'] else None
        
        if user and pbkdf2_sha256.verify(user_data["password_hash"], user["password_hash"]):
            access_token = create_access_token(identity={"id": user['id'], "role": user['role']}, fresh=True)
            refresh_token = create_refresh_token(identity={"id": user['id'], "role": user['role']})
            return {"access_token": access_token, "refresh_token": refresh_token}, 200

        abort(401, message="Invalid credentials.")

@user_blp.route('/me')
class UserProfile(MethodView):
    @staticmethod
    @jwt_required()
    @user_blp.response(200, UserSchema)
    def get():
        user_id = get_jwt_identity()["id"]
        response = supabase.table('users').select().eq('id', user_id).execute()
        user = response['data'][0] if response['data'] else None
        return user

    @user_blp.arguments(UserUpdateSchema)
    @jwt_required()
    @user_blp.response(200, UserUpdateSchema)
    def put(self, user_data):
        user_id = get_jwt_identity()["id"]
        response = supabase.table('users').update(user_data).eq('id', user_id).execute()
        
        if response['status'] == 200:
            return user_data
        else:
            abort(response['status'], message=response['error']['message'])
