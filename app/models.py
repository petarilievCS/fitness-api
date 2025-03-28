import enum
from . import db

class Goal(enum.Enum):
    LOSE_WEIGHT = "lose_weight"
    GAIN_MUSCLE = "gain_muscle"
    MAINTAIN_WEIGHT = "maintain_weight"

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    weight = db.Column(db.Float, nullable=False) # in kg
    height = db.Column(db.Float, nullable=False) # in cm
    goal = db.Column(db.Enum(Goal), nullable=False, default=Goal.MAINTAIN_WEIGHT)

class Workout(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    duration = db.Column(db.Integer, nullable=False) # in minutes
    type = db.Column(db.String(50), nullable=False)
    calories = db.Column(db.Integer, nullable=False)
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp()) # in UTC

    user = db.relationship("User", backref="workouts")

class Meal(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    calories = db.Column(db.Integer, nullable=False)
    protein = db.Column(db.Integer, nullable=False)
    carbohydrates = db.Column(db.Integer, nullable=False)
    fats = db.Column(db.Integer, nullable=False)
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp())

    user = db.relationship("User", backref="meals")

class WeightLog(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp())
    weight = db.Column(db.Float, nullable=False) # in kg

    user = db.relationship("User", backref="weight_logs")

