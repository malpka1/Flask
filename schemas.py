from marshmallow import Schema, fields


class IdeaSchema(Schema):
    activity = fields.Str(required=True, validate=fields.Length(100))
    type = fields.Str(required=True)
    participants = fields.Str(required=True)
    user_id = fields.Int(required=True)
