from app import app
from flask_restful import Api

api = Api(app)
from api import auth, vote, post, user, comment, photo