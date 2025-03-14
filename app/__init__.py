import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager

from dotenv import load_dotenv 

load_dotenv()

db = SQLAlchemy()
jwt = JWTManager()

# Factory method for creating a Flask application
def create():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///fitness_tracker.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False 
    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")

    db.init_app(app)
    jwt.init_app(app)

    from app.models import User, Workout, Meal  # Register models
    
    from app.routes import api_blueprint # Register blueprints
    app.register_blueprint(api_blueprint)

    return app  
    


