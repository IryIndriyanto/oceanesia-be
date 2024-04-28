import os
from db import db
from flask import Flask
from dotenv import load_dotenv
from flask_smorest import Api
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate

# from controllers.user import user_blp
from controllers.location import blp as location_blueprint
# from controllers.issue import blp as issue_blueprint
from controllers.environment_data import blp as environment_data_blueprint


def create_app():
    app = Flask(__name__)
    load_dotenv()

    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config["API_TITLE"] = "Oceanesia REST API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/"
    app.config["OPENAPI_SWAGGER_UI_URL"] = (
        "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    )
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")

    app.config["JWT_SECRET_KEY"] = "REVOUTEAMFOCEANESIA"
    jwt = JWTManager(app)

    db.init_app(app)
    with app.app_context():
        db.create_all()

    migrate = Migrate(app, db)

    api = Api(app)

    # api.register_blueprint(user_blp)
    api.register_blueprint(location_blueprint)
    # api.register_blueprint(issue_blueprint)
    api.register_blueprint(environment_data_blueprint)

    return app
