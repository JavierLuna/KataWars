from marshmallow import Schema, fields


class PaginationSchema(Schema):
    objects = fields.List(fields.Dict())
    next_page = fields.Integer(allow_none=True)
    prev_page = fields.Integer(allow_none=True)
    pages = fields.Integer()
    total_objects = fields.Integer()
