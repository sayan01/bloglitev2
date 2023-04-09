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
user_parser.add_argument('password', type=str, required=False)
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
        if not args['password']:
            print('Password is required')
            abort(400, message='Password is required')
        user = User(username=args['username'], password=args['password'], name=args['name'], about=args['about'], photoURL=args['photoURL'])
        db.session.add(user)
        db.session.commit()
        return user, 201
    
class UserDetail(Resource):
    @jwt_required()
    @marshal_with(user_fields)
    def get(self, id):
        user = current_user(get_jwt_identity())
        if not user:
            print(f'User {id} does not exist')
            abort(404, message=f'User {id} does not exist')
        return user
    
    @jwt_required()
    @marshal_with(user_fields)
    def put(self, id):
        user = current_user(get_jwt_identity())
        if not user:
            print(f'User {id} does not exist')
            abort(404, message=f'User {id} does not exist')
        args = user_parser.parse_args()
        if User.query.filter_by(username=args['username']).first() and args['username'] != user.username:
            print(f'User {args["username"]} already exists')
            abort(409, message=f'User {args["username"]} already exists')

        user.username = args['username']
        if args['password']:
            user.password = args['password']
        user.name = args['name']
        user.about = args['about']
        user.photoURL = args['photoURL']
        db.session.commit()
        return user
    
    @jwt_required()
    def delete(self, id):
        user = current_user(get_jwt_identity())
        if not user:
            print(f'User {id} does not exist')
            abort(404, message=f'User {id} does not exist')
        db.session.delete(user)
        db.session.commit()
        return '', 204

class UserFollow(Resource):
    @jwt_required()
    def post(self, id):
        user = current_user(get_jwt_identity())
        if not user:
            print(f'User {id} does not exist')
            abort(404, message=f'User {id} does not exist')
        current_user(get_jwt_identity()).follow(user)
        db.session.commit()
        return '', 201
    
    @jwt_required()
    def delete(self, id):
        user = current_user(get_jwt_identity())
        if not user:
            print(f'User {id} does not exist')
            abort(404, message=f'User {id} does not exist')
        current_user(get_jwt_identity()).unfollow(user)
        db.session.commit()
        return '', 204
