from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from marshmallow import ValidationError
from werkzeug.security import generate_password_hash, check_password_hash

from app import db
from app.schema import user_schema
from app.models import User
from app.utils import validate_password

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/signup", methods=["POST"])
def signup():
    try:
        data = request.get_json()
        user_data = user_schema.load(data)

        # Ensure email isn't already in use
        email = user_data["email"]
        if User.query.filter_by(email=email).first() != None:
            return jsonify({"error": "Email already exists"}), 400

        # Check password strength
        password = user_data["password"]
        password_valid = validate_password(password)
        if password_valid != None:
            return jsonify({"Error": password_valid}), 400

        password_hash = generate_password_hash(password)
        user = User(
            email=user_data["email"],
            password_hash=password_hash,
            weight=user_data["weight"],
            height=user_data["height"],
            goal=user_data["goal"]
        )
        
        db.session.add(user)
        db.session.commit()

        return jsonify(user_schema.dump(user)), 201
    except ValidationError as e:
        return jsonify({"error": e.messages}), 400
    except Exception as e:
        return jsonify({"server serror": str(e)}), 500

@auth_bp.route("/login", methods=["POST"])
def login():
    try:
        data = request.get_json()

        # Validate input
        if "email" not in data or "password" not in data:
            return jsonify({"error": "Invalid request format"})
        email, password = data["email"], data["password"]

        # Validate email
        user = User.query.filter_by(email=email).first()
        if user == None:
            return jsonify({"error": "Email doesn't exists"}), 400
        
        # Check password
        password_hash = user.password_hash
        if not check_password_hash(password_hash, password):
            return jsonify({"error": "Incorrect password"}), 401
        
        # Generate JWT Token
        token = create_access_token(identity=str(user.id))
        return jsonify({"access_token": token}), 200
    except ValidationError as e:
        return jsonify({"error": e.messages}), 400
    except Exception as e:
        return jsonify({"server serror": str(e)}), 500
    
@auth_bp.route("/user", methods=["GET"])
@jwt_required()
def get_user():
    try:
        id = get_jwt_identity()

        # Validate ID
        user = User.query.filter_by(id=id).first()
        if user == None:
            return jsonify({"error": "User doesn't exists"}), 404
        
        return jsonify(user_schema.dump(user)), 200
    except Exception as e:
        return jsonify({"server serror": str(e)}), 500
    
@auth_bp.route("/user", methods=["PUT"])
@jwt_required()
def update_user():
    try:
        id = get_jwt_identity()

        # Validate ID
        user = User.query.filter_by(id=id).first()
        if user == None:
            return jsonify({"error": "User not found"}), 404
        
        # Create new user
        data = request.get_json()
        data = user_schema.load(data, partial=True)
        
        # Update fields
        if "weight" in data:
            user.weight = data['weight']
        if "height" in data:
            user.height = data["height"]
        if "goal" in data:
            user.goal = data["goal"]

        db.session.commit()
    
        return jsonify(user_schema.dump(user)), 200
    except ValidationError as e:
        return jsonify({"error": e.messages}), 400
    except Exception as e:
        return jsonify({"server serror": str(e)}), 500