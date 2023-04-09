from flask_restful import Resource, Api
from flask import request
from models import User, db
from app import app

api = Api(app)

from .auth import Login
from .vote import VoteDetail, VoteList
from .post import PostDetail, PostList
from .user import UserDetail, UserList, UserFollow
from .comment import CommentDetail, CommentList

api.add_resource(Login, '/user/login')
api.add_resource(VoteDetail, '/vote/<int:id>')
api.add_resource(VoteList, '/vote')
api.add_resource(PostDetail, '/post/<int:id>')
api.add_resource(PostList, '/post')
api.add_resource(UserDetail, '/user/<int:id>')
api.add_resource(UserList, '/user')
api.add_resource(UserFollow, '/user/follow/<int:id>')
api.add_resource(CommentDetail, '/comment/<int:id>')
api.add_resource(CommentList, '/comment')

# photo upload
from .photo import PhotoUpload
api.add_resource(PhotoUpload, '/photo')