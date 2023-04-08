from flask_jwt_extended import JWTManager
from app import app
from models import User, db

jwt = JWTManager(app)

def current_user(identity):
    return User.query.get(identity)