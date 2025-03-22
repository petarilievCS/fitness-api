from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from marshmallow import ValidationError

from app import db
from app.schema import workout_schema
from app.models import Workout, User
from app.utils import WORKOUT_MET_VALUES, calculate_calories, get_utc_timestamp

workout_bp = Blueprint("workout", __name__)

# TODO: POST Workout
@workout_bp.route("/log", methods=["POST"])
@jwt_required()
def log_workout():
    try:
        user_id = get_jwt_identity()

        data = request.get_json()
        workout_data = workout_schema.load(data)

        # Validate workout type
        if workout_data["type"] not in WORKOUT_MET_VALUES:
            return jsonify({"error": "Invalid workout type."}), 400
        
        user = User.query.filter_by(id=user_id).first()
        weight = user.weight
        calories = calculate_calories(workout_data["type"], weight, workout_data["duration"])

        workout = Workout(
            user_id=user_id,
            duration=workout_data["duration"],
            type=workout_data["type"],
            calories=calories
        )

        if "timestamp" in workout_data:
            workout.timestamp = get_utc_timestamp(workout_data["timestamp"])

        db.session.add(workout)
        db.session.commit()

        return jsonify(workout_schema.dump(workout)), 201
    except ValidationError as e:
        return jsonify({"error": e.messages}), 400
    except Exception as e:
        return jsonify({"server serror": str(e)}), 500
    