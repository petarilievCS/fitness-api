from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from marshmallow import ValidationError

from app import db

meal_bp = Blueprint("meal", __name__)

# TODO: POST/meal/log
@meal_bp.route('/log', methods=["POST"])
@jwt_required
def log_meal():
    try:
        user_id = get_jwt_identity()

        data = request.get_json()
        # meal_data = meal_s

        return
    except Exception as e:
        return jsonify({"server serror": str(e)}), 500