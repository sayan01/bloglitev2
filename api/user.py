from models import User, db
from flask_security import auth_token_required, current_user
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
    @auth_token_required
    @marshal_with(user_fields)
    def get(self):
        return User.query.all()
    
    @marshal_with(user_fields)
    def post(self):
        args = user_parser.parse_args()
        user = User(username=args['username'], password=args['password'], name=args['name'], about=args['about'], photoURL=args['photoURL'])
        db.session.add(user)
        db.session.commit()
        return user, 201
    
class UserDetail(Resource):
    @auth_token_required
    @marshal_with(user_fields)
    def get(self, id):
        user = User.query.get(id)
        if not user:
            abort(404, message=f'User {id} does not exist')
        return user
    
    @auth_token_required
    @marshal_with(user_fields)
    def put(self, id):
        user = User.query.get(id)
        if not user:
            abort(404, message=f'User {id} does not exist')
        args = user_parser.parse_args()
        user.username = args['username']
        user.password = args['password']
        user.name = args['name']
        user.about = args['about']
        user.photoURL = args['photoURL']
        db.session.commit()
        return user
    
    @auth_token_required
    def delete(self, id):
        user = User.query.get(id)
        if not user:
            abort(404, message=f'User {id} does not exist')
        db.session.delete(user)
        db.session.commit()
        return '', 204