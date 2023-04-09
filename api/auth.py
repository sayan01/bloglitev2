
from models import User, db
from flask_restful import Resource, fields, marshal_with, reqparse, marshal, abort
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from auth import current_user
from datetime import timedelta

login_parser = reqparse.RequestParser()
login_parser.add_argument('username', type=str, required=True)
login_parser.add_argument('password', type=str, required=True)

class Login(Resource):
    def post(self):
        args = login_parser.parse_args()
        user = User.query.filter_by(username=args['username']).first()
        if not user:
            print(f'User {args["username"]} does not exist')
            abort(404, message=f'User {args["username"]} does not exist')
        if not user.verify_password(args['password']):
            print('Invalid password')
            abort(403, message='Invalid password')
        access_token = create_access_token(identity=user.id, expires_delta=timedelta(days=1))
        return {'access_token': access_token}, 200
        
    @jwt_required()
    def get(self):
        return {'login': True, 'message': 'Logged in as {}'.format(current_user(get_jwt_identity()).username)}, 200