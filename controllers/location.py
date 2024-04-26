from db import db
from flask import jsonify
from flask_smorest import Blueprint
from schemas.location import LocationSchema
from models.location import LocationModel
from sqlalchemy.exc import IntegrityError, SQLAlchemyError


blp = Blueprint(
    "locations", "locations", description="data of locations", url_prefix="/locations"
)


@blp.route("/", methods=["GET"])
@blp.response(200, LocationSchema(many=True))
def get_all_locations():
    return LocationModel.query.all()


@blp.route("/search", methods=["GET"])
@blp.arguments(LocationSchema(partial=True), location="query")
@blp.response(200, LocationSchema(many=True))
def get_locations_by_name(location_data):
    locations = LocationModel.query

    if location_data:
        locations = locations.filter(LocationModel.name.ilike(f"%{location_data}%"))

    return locations.all()


@blp.route("/search", methods=["GET"])
@blp.arguments(LocationSchema(partial=True), location="query")
@blp.response(200, LocationSchema(many=True))
def search_locations_by_lat_lng(location_data):
    min_lat = location_data.get("min_latitude")
    max_lat = location_data.get("max_latitude")
    min_lng = location_data.get("min_longitude")
    max_lng = location_data.get("max_longitude")

    if not (min_lat and max_lat and min_lng and max_lng):
        return (
            jsonify({"message": "Missing latitude or longitude range parameters"}),
            400,
        )

    return LocationModel.query.filter(
        LocationModel.latitude >= min_lat,
        LocationModel.latitude <= max_lat,
        LocationModel.longitude >= min_lng,
        LocationModel.longitude <= max_lng,
    ).all()


@blp.route("/", methods=["POST"])
@blp.arguments(LocationSchema)
@blp.response(200)
def create_location(location_data):
    location = LocationModel(**location_data)

    try:
        db.session.add(location)
        db.session.commit()
    except IntegrityError as e:
        db.session.rollback()
        error_info = str(e.orig)
        return jsonify({"message": f"IntegrityError: {error_info}"}), 400
    except SQLAlchemyError as e:
        db.session.rollback()
        error_info = str(e)
        return jsonify({"message": f"SQLAlchemyError: {error_info}"}), 500


@blp.route("/<int:location_id>", methods=["DELETE"])
@blp.response(204)
def delete_location(location_id):
    location = LocationModel.query.get(location_id)

    if location:
        db.session.delete(location)
        db.session.commit()
        return None
    else:
        return jsonify({"message": "Location not found"}), 404


@blp.route("/<int:location_id>", methods=["PUT"])
@blp.arguments(LocationSchema)
@blp.response(200)
def edit_location(location_data, location_id):
    location = LocationModel.query.get(location_id)

    if location:
        location.name = location_data.get("name")
        location.address = location_data.get("address")
        db.session.commit()
        return None
    else:
        return jsonify({"message": "Location not found"}), 404
