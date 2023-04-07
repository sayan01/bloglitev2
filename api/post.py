from models import Post, User, db
from flask_security import auth_token_required, current_user
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
    @auth_token_required
    @marshal_with(post_fields)
    def get(self):
        return Post.query.all()
    
    @auth_token_required
    @marshal_with(post_fields)
    def post(self):
        args = post_parser.parse_args()
        author = User.query.get(args['author_id'])
        if not author:
            abort(404, message=f'User {args["author_id"]} does not exist')
        if author != current_user:
            abort(403, message='You can only create posts for yourself')
        post = Post(title=args['title'], caption=args['caption'], imageURL=args['imageURL'], author=author)
        db.session.add(post)
        db.session.commit()
        return post, 201

class PostDetail(Resource):
    @auth_token_required
    @marshal_with(post_fields)
    def get(self, id):
        post = Post.query.get(id)
        if not post:
            abort(404, message=f'Post {id} does not exist')
        return post
    
    @auth_token_required
    @marshal_with(post_fields)
    def put(self, id):
        post = Post.query.get(id)
        if not post:
            abort(404, message=f'Post {id} does not exist')
        args = post_parser.parse_args()
        author = User.query.get(args['author_id'])
        if not author:
            abort(404, message=f'User {args["author_id"]} does not exist')
        if author != current_user:
            abort(403, message='You can only edit posts for yourself')
        if post.author != author:
            abort(403, message='You can only edit posts for yourself')
        post.title = args['title']
        post.caption = args['caption']
        post.imageURL = args['imageURL']
        db.session.commit()
        return post
    
    @auth_token_required
    def delete(self, id):
        post = Post.query.get(id)
        if not post:
            abort(404, message=f'Post {id} does not exist')
        if post.author != current_user:
            abort(403, message='You can only delete posts for yourself')
        db.session.delete(post)
        db.session.commit()
        return '', 204