from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from marshmallow import ValidationError
from datetime import datetime

from app import db
from app.schema import workout_schema
from app.models import Workout, User
from app.utils import WORKOUT_MET_VALUES, calculate_calories, get_utc_timestamp

workout_bp = Blueprint("workout", __name__)

@workout_bp.route("/log", methods=["POST"])
@jwt_required()
def log_workout():
    try:
        user_id = get_jwt_identity()

        data = request.get_json()
        workout_data = workout_schema.load(data)

        if workout_data["type"] not in WORKOUT_MET_VALUES:
            return jsonify({"error": "Invalid workout type."}), 400
        if workout_data["duration"] <= 0:
            return jsonify({"error": "Duration must be a positive number."}), 400
        
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
    
@workout_bp.route("/history", methods=["GET"])
@jwt_required()
def get_history():
    try:
        user_id = get_jwt_identity()
        query = Workout.query.filter_by(user_id=user_id).order_by(Workout.timestamp.desc())

        workout_type = request.args.get("type")
        if workout_type and workout_type in WORKOUT_MET_VALUES:
            query = query.filter_by(type=workout_type)

        from_date_string = request.args.get("from")
        if from_date_string:
            from_date = datetime.strptime(from_date_string, "%Y-%m-%d")
            query = query.filter(Workout.timestamp >= from_date)

        to_date_string = request.args.get("to")
        if to_date_string:
            to_date = datetime.strptime(to_date_string, "%Y-%m-%d")
            query = query.filter(Workout.timestamp <= to_date)

        max_duration = request.args.get("max_duration")
        if max_duration:
            query = query.filter(Workout.duration <= int(max_duration))

        min_duration = request.args.get("min_duration")
        if min_duration:
            query = query.filter(Workout.duration >= int(min_duration))

        limit = request.args.get("limit", default=10, type=int)
        if limit < 1 or limit > 100:
            return jsonify({"error": "'limit' must be between 1 and 100"}), 400
        
        offset = request.args.get("offset", default=0, type=int)
        if offset < 0:
            return jsonify({"error": "'offset' must be 0 or greater"}), 400
    
        workouts = query.limit(limit).offset(offset).all()
        return jsonify(workout_schema.dump(workouts, many=True)), 200
    except Exception as e:
        return jsonify({"server serror": str(e)}), 500
    
@workout_bp.route("/<int:workout_id>", methods=["GET"])
@jwt_required()
def get_workout(workout_id):
    try:
        user_id = int(get_jwt_identity())
        workout = Workout.query.get(workout_id)

        if not workout:
            return jsonify({"error": "Workout not found."}), 404

        if workout.user_id != user_id:
            return jsonify({"error": "You are not authorized to access this workout."}), 403

        return jsonify(workout_schema.dump(workout)), 200
    except Exception as e:
        return jsonify({"server serror": str(e)}), 500
    
@workout_bp.route("/<int:workout_id>", methods=["DELETE"])
@jwt_required()
def delete_workout(workout_id):
    try:
        user_id = int(get_jwt_identity())
        workout = Workout.query.get(workout_id)

        if not workout:
            return jsonify({"error": "Workout not found."}), 404

        if workout.user_id != user_id:
            return jsonify({"error": "You are not authorized to delete this workout."}), 403

        db.session.delete(workout)
        db.session.commit()

        return jsonify({"message": f"Workout {workout_id} deleted"}), 200
    except Exception as e:
        return jsonify({"server serror": str(e)}), 500