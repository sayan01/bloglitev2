from models import User, db
from flask_jwt_extended import jwt_required, get_jwt_identity
from auth import current_user
from flask_restful import Resource, fields, marshal_with, reqparse, marshal, abort

user_fields = {
    'id': fields.Integer,
    'username': fields.String,
    'name': fields.String,
    'about': fields.String,
    'joined': fields.DateTime,
    'photoURL': fields.String,
}

user_parser = reqparse.RequestParser()
user_parser.add_argument('username', type=str, required=True)
user_parser.add_argument('password', type=str, required=True)
user_parser.add_argument('name', type=str, required=True)
user_parser.add_argument('about', type=str, required=True)
user_parser.add_argument('photoURL', type=str, required=False)

class UserList(Resource):
    @jwt_required()
    @marshal_with(user_fields)
    def get(self):
        return User.query.all()
    
    @marshal_with(user_fields)
    def post(self):
        args = user_parser.parse_args()
        if User.query.filter_by(username=args['username']).first():
            print(f'User {args["username"]} already exists')
            abort(409, message=f'User {args["username"]} already exists')
        user = User(username=args['username'], password=args['password'], name=args['name'], about=args['about'], photoURL=args['photoURL'])
        db.session.add(user)
        db.session.commit()
        return user, 201
    
class UserDetail(Resource):
    @jwt_required()
    @marshal_with(user_fields)
    def get(self, id):
        user = User.query.get(id)
        if not user:
            print(f'User {id} does not exist')
            abort(404, message=f'User {id} does not exist')
        return user
    
    @jwt_required()
    @marshal_with(user_fields)
    def put(self, id):
        user = User.query.get(id)
        if not user:
            print(f'User {id} does not exist')
            abort(404, message=f'User {id} does not exist')
        args = user_parser.parse_args()
        if User.query.filter_by(username=args['username']).first():
            print(f'User {args["username"]} already exists')
            abort(409, message=f'User {args["username"]} already exists')
        if user != current_user(get_jwt_identity()):
            print('You can only edit your own account')
            abort(403, message='You can only edit your own account')
        user.username = args['username']
        user.password = args['password']
        user.name = args['name']
        user.about = args['about']
        user.photoURL = args['photoURL']
        db.session.commit()
        return user
    
    @jwt_required()
    def delete(self, id):
        user = User.query.get(id)
        if not user:
            print(f'User {id} does not exist')
            abort(404, message=f'User {id} does not exist')
        if user != current_user(get_jwt_identity()):
            print('You can only delete your own account')
            abort(403, message='You can only delete your own account')
        db.session.delete(user)
        db.session.commit()
        return '', 204

class UserFollow(Resource):
    @jwt_required()
    def post(self, id):
        user = User.query.get(id)
        if not user:
            print(f'User {id} does not exist')
            abort(404, message=f'User {id} does not exist')
        current_user(get_jwt_identity()).follow(user)
        db.session.commit()
        return '', 201
    
    @jwt_required()
    def delete(self, id):
        user = User.query.get(id)
        if not user:
            print(f'User {id} does not exist')
            abort(404, message=f'User {id} does not exist')
        current_user(get_jwt_identity()).unfollow(user)
        db.session.commit()
        return '', 204
