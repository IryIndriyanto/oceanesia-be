from marshmallow import Schema, fields

class UserUpdateSchema(Schema):
    username = fields.Str()
    password_hash = fields.Str()
    email = fields.Str()