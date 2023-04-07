from models import Vote, Post, User, db
from flask_security import auth_token_required, current_user
from flask_restful import Resource, fields, marshal_with, reqparse, marshal, abort

vote_fields = {
    'id': fields.Integer,
    'score': fields.Integer,
    'post_id': fields.Integer,
    'user_id': fields.Integer,
}

vote_parser = reqparse.RequestParser()
vote_parser.add_argument('score', type=int, required=True)
vote_parser.add_argument('post_id', type=int, required=True)
vote_parser.add_argument('user_id', type=int, required=True)

# edit/delete single vote by id (only author can edit/delete)
class VoteDetail(Resource):
    @auth_token_required
    @marshal_with(vote_fields)
    def get(self, id):
        vote = Vote.query.get(id)
        if not vote:
            abort(404, message=f'Vote {id} does not exist')
        return vote

    @auth_token_required
    @marshal_with(vote_fields)
    def put(self, id):
        vote = Vote.query.get(id)
        if not vote:
            abort(404, message=f'Vote {id} does not exist')
        args = vote_parser.parse_args()
        user = User.query.get(args['user_id'])
        if not user:
            abort(404, message=f'User {args["user_id"]} does not exist')
        if user != current_user:
            abort(403, message='You can only edit votes for yourself')
        if user != vote.user:
            abort(403, message='You can only edit votes for yourself')
        post = Post.query.get(args['post_id'])
        if not post:
            abort(404, message=f'Post {args["post_id"]} does not exist')
        if post != vote.post:
            abort(403, message='You can only edit votes for the post they belong to')
        if args['score'] not in [-1, 1]:
            abort(403, message='Score must be -1 or 1')
        vote.score = args['score']
        db.session.commit()
        return vote

    @auth_token_required
    @marshal_with(vote_fields)
    def delete(self, id):
        vote = Vote.query.get(id)
        if not vote:
            abort(404, message=f'Vote {id} does not exist')
        if vote.user != current_user:
            abort(403, message='You can only delete votes for yourself')
        db.session.delete(vote)
        db.session.commit()
        return vote
    
# add new vote to post using post_id in URL or list all votes for post (only author can add new vote)
class VoteList(Resource):
    @auth_token_required
    @marshal_with(vote_fields)
    def get(self, post_id):
        post = Post.query.get(post_id)
        if not post:
            abort(404, message=f'Post {post_id} does not exist')
        return post.votes
    
    @auth_token_required
    @marshal_with(vote_fields)
    def post(self, post_id):
        args = vote_parser.parse_args()
        user = User.query.get(args['user_id'])
        if not user:
            abort(404, message=f'User {args["user_id"]} does not exist')
        if user != current_user:
            abort(403, message='You can only add votes for yourself')
        post = Post.query.get(post_id)
        if not post:
            abort(404, message=f'Post {post_id} does not exist')
        if args['score'] not in [-1, 1]:
            abort(403, message='Score must be -1 or 1')
        # if user has already voted on this post, update the vote
        vote = Vote.query.filter_by(user=user, post=post).first()
        if vote:
            vote.score = args['score']
        else:
            vote = Vote(score=args['score'], post=post, user=user)
            db.session.add(vote)
        db.session.commit()
        return vote, 201