from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from app import app
from flask_security.models import fsqla_v3 as fsqla
from flask_security import hash_password, verify_password


db = SQLAlchemy(app)
migrate = Migrate(app, db)
fsqla.FsModels.set_db_info(db)

# Creating Model

followers= db.Table('followers',
                       db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
                       db.Column('followed_id', db.Integer, db.ForeignKey('user.id'))
                       )
class Role(db.Model, fsqla.FsRoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

    def __repr__(self) -> str:
        return f'<Role {self.id} "{self.name}">'

class User(db.Model, fsqla.FsUserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), unique=True, nullable=False)
    passhash = db.Column(db.String(512), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    about = db.Column(db.String(256), nullable=False)
    joined = db.Column(db.DateTime(), nullable=False, default=datetime.utcnow)
    photoURL = db.Column(db.String(512), nullable=True)

    posts = db.relationship('Post', backref='author', cascade="all, delete-orphan")
    comments = db.relationship('Comment', backref='author', cascade="all, delete-orphan")
    votes = db.relationship('Vote', backref='author', cascade="all, delete-orphan")

    list_of_followers = db.relationship('User', secondary=followers,
                                        primaryjoin=(
                                            followers.c.follower_id == id),
                                        secondaryjoin=(
                                            followers.c.followed_id == id),
                                        backref=db.backref('followers', lazy='select'), lazy='select')  # many to many relationship with other Users
                            
    list_of_following = db.relationship('User', secondary=followers,
                                        primaryjoin=(
                                            followers.c.followed_id == id),
                                        secondaryjoin=(
                                            followers.c.follower_id == id),
                                        backref=db.backref('following', lazy='select'), lazy='select')  # many to many relationship with other Users

    @property
    def password(self):
        raise AttributeError('password is not a readible attribute')
    
    @password.setter
    def password(self, password):
        self.passhash = hash_password(password)

    def verify_password(self, password):
        return verify_password(password, self.passhash)
    
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
