from flask_restful import Resource, Api
from flask import request
from models import User, db
from app import app
from flask_security import auth_token_required, current_user
from flask_security.utils import verify_password

api = Api(app)
