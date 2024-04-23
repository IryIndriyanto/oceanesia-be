from marshmallow import Schema, fields

class UserSchema(Schema):
    id = fields.UUID(dump_only=True)
    username = fields.Str(required=True)
    email = fields.Str()
    password_hash = fields.Str(required=True)

class UserUpdateSchema(Schema):
    username = fields.Str()
    password_hash = fields.Str()
    email = fields.Str()
