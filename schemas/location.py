from marshmallow import Schema, fields

class LocationSchema(Schema):
    id = fields.Integer(dump_only=True)
    latitude = fields.Float(required=True)
    longitude = fields.Float(required=True)
    name = fields.String(required=True, validate=lambda s: len(s) <= 100)
    description = fields.String()