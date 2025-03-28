from marshmallow import Schema, fields, validate

from app.models import Goal

class UserSchema(Schema):
    id = fields.Integer(dump_only=True)
    email = fields.Email(required=True)
    password = fields.Str(required=True, load_only=True)
    weight = fields.Float(required=True, validate=validate.Range(min=30, max=500))
    height = fields.Float(required=True, validate=validate.Range(min=100, max=250))
    goal = fields.Function(lambda obj: obj.goal.value, deserialize=lambda val: Goal(val))

class WorkoutSchema(Schema):
    id = fields.Integer(dump_only=True)
    user_id = fields.Integer(dump_only=True, required=True)
    duration = fields.Integer(required=True)
    type = fields.String(required=True)
    calories = fields.Integer(required=True, dump_only=True)
    timestamp = fields.DateTime(required=False)

class MealSchema(Schema):
    id = fields.Integer(dump_only=True)
    user_id = fields.Integer(dump_only=True)
    name = fields.String(required=True, validate=validate.Length(min=1, max=50))
    calories = fields.Integer(required=True, validate=validate.Range(min=0))
    protein = fields.Integer(required=True, validate=validate.Range(min=0))
    carbohydrates = fields.Integer(required=True, validate=validate.Range(min=0))
    fats = fields.Integer(required=True, validate=validate.Range(min=0))
    timestamp = fields.DateTime(required=False)
    
user_schema = UserSchema()
workout_schema = WorkoutSchema()
meal_schema = MealSchema()