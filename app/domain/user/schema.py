from marshmallow import Schema, fields, validate


class CreationSchema(Schema):
    username = fields.String(required=True, validate=validate.Length(min=4, max=64))
    email = fields.Email(required=True)
    password = fields.String(required=True, validate=validate.Length(min=4, max=16))


class EditingSchema(Schema):
    username = fields.String()
    email = fields.Email(required=True)
    password = fields.String(required=True, validate=validate.Length(min=4, max=16))
