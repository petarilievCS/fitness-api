from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Factory method for creating a Flask application
def create():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///fitness_tracker.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False 

    db.init_app(app)
    from app.models import User, Workout, Meal  # Register models

    return app  


