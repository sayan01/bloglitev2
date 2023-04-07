from models import Comment, Post, User, db
from flask_security import auth_token_required, current_user
from flask_restful import Resource, fields, marshal_with, reqparse, marshal, abort

comment_fields = {
    'id': fields.Integer,
    'content': fields.String,
    'time': fields.DateTime,
    'author_id': fields.Integer,
    'post_id': fields.Integer,
}

comment_parser = reqparse.RequestParser()
comment_parser.add_argument('content', type=str, required=True)
comment_parser.add_argument('author_id', type=int, required=True)
comment_parser.add_argument('post_id', type=int, required=True)

# edit/delete single comment by id (only author can edit/delete)
class CommentDetail(Resource):
    @auth_token_required
    @marshal_with(comment_fields)
    def get(self, id):
        comment = Comment.query.get(id)
        if not comment:
            abort(404, message=f'Comment {id} does not exist')
        return comment

    @auth_token_required
    @marshal_with(comment_fields)
    def put(self, id):
        comment = Comment.query.get(id)
        if not comment:
            abort(404, message=f'Comment {id} does not exist')
        args = comment_parser.parse_args()
        author = User.query.get(args['author_id'])
        if not author:
            abort(404, message=f'User {args["author_id"]} does not exist')
        if author != current_user:
            abort(403, message='You can only edit comments for yourself')
        post = Post.query.get(args['post_id'])
        if not post:
            abort(404, message=f'Post {args["post_id"]} does not exist')
        if post != comment.post:
            abort(403, message='You can only edit comments for the post they belong to')
        comment.content = args['content']
        db.session.commit()
        return comment

    @auth_token_required
    @marshal_with(comment_fields)
    def delete(self, id):
        comment = Comment.query.get(id)
        if not comment:
            abort(404, message=f'Comment {id} does not exist')
        if comment.author != current_user:
            abort(403, message='You can only delete comments for yourself')
        db.session.delete(comment)
        db.session.commit()
        return comment

# get all comments for a post
class CommentList(Resource):
    @auth_token_required
    @marshal_with(comment_fields)
    def get(self, post_id):
        post = Post.query.get(post_id)
        if not post:
            abort(404, message=f'Post {post_id} does not exist')
        return post.comments

    @auth_token_required
    @marshal_with(comment_fields)
    def post(self, post_id):
        args = comment_parser.parse_args()
        author = User.query.get(args['author_id'])
        if not author:
            abort(404, message=f'User {args["author_id"]} does not exist')
        if author != current_user:
            abort(403, message='You can only create comments for yourself')
        post = Post.query.get(post_id)
        if not post:
            abort(404, message=f'Post {post_id} does not exist')
        comment = Comment(content=args['content'], author=author, post=post)
        db.session.add(comment)
        db.session.commit()
        return comment, 201