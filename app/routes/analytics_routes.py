from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime, timedelta, timezone

from app import db
from app.models import Workout, Meal

analytics_bp = Blueprint("analytics", __name__)

@analytics_bp.route("/workouts", methods=["GET"])
@jwt_required()
def get_workout_analytics():
    try:
        user_id = get_jwt_identity()
        workouts = Workout.query.filter_by(user_id=user_id).all()

        if not workouts:
            return jsonify({
                "total_workouts": 0,
                "total_calories": 0,
                "calories_by_day": {},
                "average_duration": 0,
                "most_frequent_type": None
            }), 200

        total_workouts = len(workouts)
        total_calories = int(sum(workout.calories for workout in workouts))
        
        calories_by_day = {}
        for workout in workouts:
            date = str(workout.timestamp.date())
            if date not in calories_by_day:
                calories_by_day[date] = 0
            calories_by_day[date] += int(workout.calories)
        
        average_duration = round(sum(workout.duration for workout in workouts) / len(workouts), 2)

        type_freq = {}
        for workout in workouts:
            workout_type = workout.type
            type_freq[workout_type] = type_freq.get(workout_type, 0) + 1
        most_frequent_type = max(type_freq.items(), key=lambda x: x[1])[0]

        result = {
            "total_workouts": total_workouts,
            "total_calories": total_calories,
            "calories_by_day": calories_by_day,
            "average_duration": average_duration,
            "most_frequent_type": most_frequent_type
        }

        return jsonify(result), 200
    except Exception as e:
        return jsonify({"server serror": str(e)}), 500
    
@analytics_bp.route("/nutrition", methods=["GET"])
@jwt_required()
def get_meal_analytics():
    try:
        user_id = get_jwt_identity()

        # Get all meals from this week (in UTC)
        now = datetime.now(timezone.utc)
        week_ago = (now - timedelta(days=7)).replace(hour=0, minute=0, second=0, microsecond=0)
        meals = Meal.query \
            .filter_by(user_id=user_id) \
            .filter(Meal.timestamp <= now) \
            .filter(Meal.timestamp >= week_ago) \
            .all()

        result = {}
        for meal in meals:
            date = str(meal.timestamp.date())
            if date not in result:
                result[date] = {
                    "calories": 0,
                    "protein": 0,
                    "carbohydrates": 0,
                    "fats": 0
                }
            
            result[date]["calories"] += meal.calories
            result[date]["protein"] += meal.protein
            result[date]["carbohydrates"] += meal.carbohydrates
            result[date]["fats"] += meal.fats

        return jsonify(result), 200    
    except Exception as e:
        return jsonify({"server serror": str(e)}), 500