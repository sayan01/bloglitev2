from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from app import app
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Creating Model

followers= db.Table('followers',
                       db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
                       db.Column('followed_id', db.Integer, db.ForeignKey('user.id'))
                       )
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), unique=True, nullable=False)
    passhash = db.Column(db.String(512), nullable=False)

    @property
    def password(self):
        raise AttributeError('password is not a readible attribute')
    
    @password.setter
    def password(self, password):
        self.passhash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.passhash, password)

    name = db.Column(db.String(50), nullable=False)
    about = db.Column(db.String(256), nullable=False)
    joined = db.Column(db.DateTime(), nullable=False, default=datetime.utcnow)
    photoURL = db.Column(db.String(512), nullable=True)

    posts = db.relationship('Post', backref='author', cascade="all, delete-orphan")
    comments = db.relationship('Comment', backref='author', cascade="all, delete-orphan")
    votes = db.relationship('Vote', backref='author', cascade="all, delete-orphan")

    following = db.relationship('User', secondary=followers,
                                primaryjoin=(followers.c.follower_id == id),
                                secondaryjoin=(followers.c.followed_id == id),
                                backref=db.backref('followers', lazy='dynamic'), lazy='dynamic')
    
    def follow(self, user):
        if user not in self.following:
            self.following.append(user)
    
    def unfollow(self, user):
        if user in self.following:
            self.following.remove(user)
    
    def __repr__(self) -> str:
        return f'<User {self.id} "{self.username}">'
    

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    caption = db.Column(db.Text, nullable=False)
    imageURL = db.Column(db.String(512), nullable=True)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    comments = db.relationship('Comment', backref='post', cascade="all, delete-orphan")
    votes = db.relationship('Vote', backref='post', cascade="all, delete-orphan")
    
    @property
    def score(self):
        return sum([vote.score for vote in self.votes ])

    def __repr__(self) -> str:
        return f'<Post {self.id} "{self.title}">'


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class Vote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    score = db.Column(db.Integer, nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))


with app.app_context():
    db.create_all()
