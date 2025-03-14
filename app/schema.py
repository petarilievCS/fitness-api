from marshmallow import Schema, fields, validate

from app.models import Goal

class UserSchema(Schema):
    id = fields.Integer(dump_only=True)
    email = fields.Email(required=True)
    password_hash = fields.Str(required=True, load_only=True)
    weight = fields.Float(required=True, validate=validate.Range(min=30, max=500))
    height = fields.Float(required=True, validate=validate.Range(min=100, max=250))
    goal = fields.Function(lambda obj: obj.goal.value, deserialize=lambda val: Goal(val))
    
user_schema = UserSchema()