from models import Post, User, db
from flask_jwt_extended import jwt_required, get_jwt_identity
from auth import current_user
from flask_restful import Resource, fields, marshal_with, reqparse, marshal, abort

post_fields = {
    'id': fields.Integer,
    'title': fields.String,
    'caption': fields.String,
    'imageURL': fields.String,
    'author_id': fields.Integer,
    'time': fields.DateTime,
}

post_parser = reqparse.RequestParser()
post_parser.add_argument('title', type=str, required=True)
post_parser.add_argument('caption', type=str, required=True)
post_parser.add_argument('imageURL', type=str, required=False)
post_parser.add_argument('author_id', type=int, required=True)

class PostList(Resource):
    @jwt_required()
    @marshal_with(post_fields)
    def get(self):
        return Post.query.all()
    
    @jwt_required()
    @marshal_with(post_fields)
    def post(self):
        args = post_parser.parse_args()
        author = User.query.get(args['author_id'])
        if not author:
            print(f'User {args["author_id"]} does not exist')
            abort(404, message=f'User {args["author_id"]} does not exist')
        if author != current_user(get_jwt_identity()):
            print('You can only create posts for yourself')
            abort(403, message='You can only create posts for yourself')
        post = Post(title=args['title'], caption=args['caption'], imageURL=args['imageURL'], author=author)
        db.session.add(post)
        db.session.commit()
        return post, 201

class PostDetail(Resource):
    @jwt_required()
    @marshal_with(post_fields)
    def get(self, id):
        post = Post.query.get(id)
        if not post:
            print(f'Post {id} does not exist')
            abort(404, message=f'Post {id} does not exist')
        return post
    
    @jwt_required()
    @marshal_with(post_fields)
    def put(self, id):
        post = Post.query.get(id)
        if not post:
            print(f'Post {id} does not exist')
            abort(404, message=f'Post {id} does not exist')
        args = post_parser.parse_args()
        author = User.query.get(args['author_id'])
        if not author:
            print(f'User {args["author_id"]} does not exist')
            abort(404, message=f'User {args["author_id"]} does not exist')
        if author != current_user(get_jwt_identity()):
            print('You can only edit posts for yourself')
            abort(403, message='You can only edit posts for yourself')
        if post.author != author:
            print('You can only edit posts for yourself')
            abort(403, message='You can only edit posts for yourself')
        post.title = args['title']
        post.caption = args['caption']
        post.imageURL = args['imageURL']
        db.session.commit()
        return post
    
    @jwt_required()
    def delete(self, id):
        post = Post.query.get(id)
        if not post:
            print(f'Post {id} does not exist')
            abort(404, message=f'Post {id} does not exist')
        if post.author != current_user(get_jwt_identity()):
            print('You can only delete posts for yourself')
            abort(403, message='You can only delete posts for yourself')
        db.session.delete(post)
        db.session.commit()
        return '', 204