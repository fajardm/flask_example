from marshmallow import Schema, fields


class AuthenticationSchema(Schema):
    username = fields.String(required=True)
    password = fields.String(required=True)
