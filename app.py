import os
from db import db
from flask import Flask
from dotenv import load_dotenv
from flask_smorest import Api
from flask_jwt_extended import JWTManager


def create_app(is_test_active=False):
    app = Flask(__name__)
    load_dotenv()

    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config["API_TITLE"] = "Banking Application REST API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/"
    app.config["OPENAPI_SWAGGER_UI_URL"] = (
        "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    )
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")

    app.config["JWT_SECRET_KEY"] = "REVOU_MILESTONE_4"
    jwt = JWTManager(app)

    db.init_app(app)
    with app.app_context():
        db.create_all()

    api = Api(app)

    api.register_blueprint()

    // Apaan tuh

    return app
