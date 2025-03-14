from flask import Blueprint

from app.routes.auth_routes import auth_bp

api_blueprint = Blueprint("api", __name__)
api_blueprint.register_blueprint(auth_bp, url_prefix="/auth")

@api_blueprint.route("/", methods=["GET"])
def home():
    return "Hello World"