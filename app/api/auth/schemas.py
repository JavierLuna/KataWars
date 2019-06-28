from marshmallow import fields

from app import ma


class LoginUserSchema(ma.Schema):
    username = fields.Str(required=True)
    password = fields.Str(required=True)
