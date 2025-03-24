from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from marshmallow import ValidationError
from datetime import datetime

from app import db
from app.models import Meal
from app.schema import meal_schema
from app.utils import get_utc_timestamp

meal_bp = Blueprint("meal", __name__)

@meal_bp.route('/log', methods=["POST"])
@jwt_required()
def log_meal():
    try:
        user_id = get_jwt_identity()

        data = request.get_json()
        meal_data = meal_schema.load(data)

        meal = Meal(
            user_id=user_id,
            name=meal_data["name"],
            calories=meal_data["calories"],
            protein=meal_data["protein"],
            carbohydrates=meal_data["carbohydrates"],
            fats=meal_data["fats"]
        )

        if "timestamp" in meal_data:
            meal.timestamp = get_utc_timestamp(meal_data["timestamp"])

        db.session.add(meal)
        db.session.commit()

        return jsonify(meal_schema.dump(meal)), 201
    except ValidationError as e:
        return jsonify({"error": e.messages}), 400
    except Exception as e:
        return jsonify({"server serror": str(e)}), 500
    
@meal_bp.route("/history", methods=["GET"])
@jwt_required()
def get_history():
    try:
        user_id = get_jwt_identity()
        query = Meal.query.filter_by(user_id=user_id).order_by(Meal.timestamp.desc())

        from_date_string = request.args.get("from")
        if from_date_string:
            from_date = datetime.strptime(from_date_string, "%Y-%m-%d")
            query = query.filter(Meal.timestamp >= from_date)

        to_date_string = request.args.get("to")
        if to_date_string:
            to_date = datetime.strptime(to_date_string, "%Y-%m-%d")
            query = query.filter(Meal.timestamp <= to_date)

        name = request.args.get("name")
        if name:
            query = query.filter(Meal.name.ilike(f"%{name}%"))

        limit = request.args.get("limit", default=10, type=int)
        if limit < 1 or limit > 100:
            return jsonify({"error": "'limit' must be between 1 and 100"}), 400
        
        offset = request.args.get("offset", default=0, type=int)
        if offset < 0:
            return jsonify({"error": "'offset' must be 0 or greater"}), 400
    
        meals = query.limit(limit).offset(offset).all()
        return jsonify(meal_schema.dump(meals, many=True)), 200
    except Exception as e:
        return jsonify({"server serror": str(e)}), 500
    
@meal_bp.route("/<int:meal_id>", methods=["GET"])
@jwt_required()
def get_meal(meal_id):
    try:
        user_id = int(get_jwt_identity())
        meal = Meal.query.get(meal_id)

        if not meal:
            return jsonify({"error": "Meal not found."}), 404

        if meal.user_id != user_id:
            return jsonify({"error": "You are not authorized to access this meal."}), 403

        return jsonify(meal_schema.dump(meal)), 200
    except Exception as e:
        return jsonify({"server serror": str(e)}), 500
    
@meal_bp.route("/<int:meal_id>", methods=["DELETE"])
@jwt_required()
def delete_meal(meal_id):
    try:
        user_id = int(get_jwt_identity())
        meal = Meal.query.get(meal_id)

        if not meal:
            return jsonify({"error": "Meal not found."}), 404

        if meal.user_id != user_id:
            return jsonify({"error": "You are not authorized to delete this meal."}), 403

        db.session.delete(meal)
        db.session.commit()

        return jsonify({"message": f"Workout {meal} deleted"}), 200
    except Exception as e:
        return jsonify({"server serror": str(e)}), 500