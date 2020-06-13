from marshmallow import Schema, fields, validate


class CreationSchema(Schema):
    name = fields.String(required=True, validate=validate.Length(min=4, max=64))
    email = fields.Email(required=True)
    clothes_size = fields.Int(required=True, validate=validate.Range(min=1))


class EditingSchema(CreationSchema):
    pass
