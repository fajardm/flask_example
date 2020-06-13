from marshmallow import Schema, fields, validate


class CreationSchema(Schema):
    first_name = fields.String(required=True, validate=validate.Length(min=1, max=32))
    last_name = fields.String(required=True, validate=validate.Length(min=1, max=32))
    birth_of_date = fields.Date(required=True, format='%Y-%m-%d')
    picture = fields.Raw()


class EditingSchema(CreationSchema):
    pass
