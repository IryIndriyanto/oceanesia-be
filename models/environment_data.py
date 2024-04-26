from db import db


class EnvironmentDataModel(db.Model):
    __tablename__ = "environment_data"

    id = db.Column(db.Integer, primary_key=True)
    location_id = db.Column(db.Integer, db.ForeignKey("location.id"))
    temperature = db.Column(db.Float)
    ph_level = db.Column(db.Float)
    measured_time = db.Column(db.DateTime)
