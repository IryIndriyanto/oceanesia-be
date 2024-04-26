from db import db
from flask import jsonify
from flask_smorest import Blueprint
from schemas.environment_data import EnvironmentDataSchema
from models.environment_data import EnvironmentDataModel
from sqlalchemy.exc import IntegrityError, SQLAlchemyError


blp = Blueprint(
    "environment_data", "environment_data", description="environment data", url_prefix="/environment_data"
)


@blp.route("/", methods=["GET"])
@blp.response(200, EnvironmentDataSchema(many=True))
def get_all_environment_data():
    return EnvironmentDataModel.query.all()
