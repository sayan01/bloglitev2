from models import Post, User, db
from flask_jwt_extended import jwt_required, get_jwt_identity
from auth import current_user
from flask_restful import Resource, fields, marshal_with, reqparse, marshal, abort
from api import api
from cache import cache

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

class PostList(Resource):
    @jwt_required()
    @cache.cached(timeout=3)
    @marshal_with(post_fields)
    def get(self):
        return Post.query.all()
    
    @jwt_required()
    @marshal_with(post_fields)
    def post(self):
        args = post_parser.parse_args()
        author = current_user(get_jwt_identity())
        post = Post(title=args['title'], caption=args['caption'], imageURL=args['imageURL'], author=author)
        db.session.add(post)
        db.session.commit()
        return post, 201

api.add_resource(PostList, '/post')
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
        author = current_user(get_jwt_identity())
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
        
api.add_resource(PostDetail, '/post/<int:id>')


class PostofUser(Resource):
    @jwt_required()
    @cache.cached(timeout=3)
    @marshal_with(post_fields)
    def get(self, user_id):
        user = User.query.get(user_id)
        if not user:
            print(f'User {user_id} does not exist')
            abort(404, message=f'User {user_id} does not exist')
        return user.posts

api.add_resource(PostofUser, '/user/<int:user_id>/posts')

class PostofMe(Resource):
    @jwt_required()
    @cache.cached(timeout=3)
    @marshal_with(post_fields)
    def get(self):
        user = current_user(get_jwt_identity())
        return user.posts

api.add_resource(PostofMe, '/user/posts')

class Feed(Resource):
    @jwt_required()
    @cache.cached(timeout=3)
    @marshal_with(post_fields)
    def get(self):
        user = current_user(get_jwt_identity())
        posts = []
        for user2 in user.following:
            posts += user2.posts
        posts.sort(key=lambda x: x.time, reverse=True)
        return posts

api.add_resource(Feed, '/user/feed')