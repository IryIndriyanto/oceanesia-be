from marshmallow import Schema, fields

class EnvironmentDataSchema(Schema):
    id = fields.Integer(dump_only=True)
    location_id = fields.Integer(required=True)
    temperature = fields.Float()
    ph_level = fields.Float()
    measured_time = fields.DateTime()