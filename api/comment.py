from models import Comment, Post, User, db
from flask_jwt_extended import jwt_required, get_jwt_identity
from auth import current_user
from flask_restful import Resource, fields, marshal_with, reqparse, marshal, abort
from api import api

comment_fields = {
    'id': fields.Integer,
    'content': fields.String,
    'time': fields.DateTime,
    'author_id': fields.Integer,
    'post_id': fields.Integer,
}

comment_parser = reqparse.RequestParser()
comment_parser.add_argument('content', type=str, required=True)
comment_parser.add_argument('post_id', type=int, required=True)

# edit/delete single comment by id (only author can edit/delete)
class CommentDetail(Resource):
    @jwt_required()
    @marshal_with(comment_fields)
    def get(self, id):
        comment = Comment.query.get(id)
        if not comment:
            print(f'Comment {id} does not exist')
            abort(404, message=f'Comment {id} does not exist')
        return comment

    @jwt_required()
    @marshal_with(comment_fields)
    def put(self, id):
        comment = Comment.query.get(id)
        if not comment:
            print(f'Comment {id} does not exist')
            abort(404, message=f'Comment {id} does not exist')
        args = comment_parser.parse_args()
        author = current_user(get_jwt_identity())
        post = Post.query.get(args['post_id'])
        if not post:
            print(f'Post {args["post_id"]} does not exist')
            abort(404, message=f'Post {args["post_id"]} does not exist')
        if post != comment.post:
            print('You can only edit comments for the post they belong to')
            abort(403, message='You can only edit comments for the post they belong to')
        comment.content = args['content']
        db.session.commit()
        return comment

    @jwt_required()
    @marshal_with(comment_fields)
    def delete(self, id):
        comment = Comment.query.get(id)
        if not comment:
            print(f'Comment {id} does not exist')
            abort(404, message=f'Comment {id} does not exist')
        if comment.author != current_user(get_jwt_identity()):
            print('You can only delete comments for yourself')
            abort(403, message='You can only delete comments for yourself')
        db.session.delete(comment)
        db.session.commit()
        return comment

api.add_resource(CommentDetail, '/comment/<int:id>')
# get all comments for a post
class CommentList(Resource):
    @jwt_required()
    @marshal_with(comment_fields)
    def get(self, post_id):
        post = Post.query.get(post_id)
        if not post:
            print(f'Post {post_id} does not exist')
            abort(404, message=f'Post {post_id} does not exist')
        return sorted(post.comments, key=lambda c: c.time, reverse=True)

    @jwt_required()
    @marshal_with(comment_fields)
    def post(self, post_id):
        args = comment_parser.parse_args()
        author = current_user(get_jwt_identity())
        post = Post.query.get(post_id)
        if not post:
            print(f'Post {post_id} does not exist')
            abort(404, message=f'Post {post_id} does not exist')
        comment = Comment(content=args['content'], author=author, post=post)
        db.session.add(comment)
        db.session.commit()
        return comment, 201

api.add_resource(CommentList, '/post/<int:post_id>/comment')