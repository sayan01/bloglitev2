from flask_wtf import *
from wtforms import *
from wtforms.validators import *
from wtforms.widgets import *

# Form Class Register
class UserForm(FlaskForm):
    username = StringField("Username", 
        validators=[
            DataRequired(message="Username cannot be empty"),
            Length(max=32, message="Username cannot be longer than 32 characters")
        ]
    )
    password = PasswordField("Password", 
        validators=[
            DataRequired(message="Password cannot be empty"), 
            Length(min=8, message="Password should be atleast 8 characteres long")
        ]
    )
    password_confirm = PasswordField("Confirm Password", 
        validators=[
            DataRequired(message="Confirm the password"), 
            Length(min=8, message="Password should be atleast 8 characteres long"),
            EqualTo('password', message="Passwords must match")
        ]
    )
    name = StringField("Name", 
        validators=[
            DataRequired(message="Name cannot be empty"), 
            Length(max=50, message="First Name cannot be longer than 50 characters")
        ]
    )
    about = StringField("About (Bio)", 
        validators=[
            DataRequired(message="About cannot be empty"), 
            Length(max=256, message="About cannot be longer than 256 characters")
        ]
    )
    submit = SubmitField("Login")

class PostForm(FlaskForm):
    title = StringField("Title", 
        validators=[
            DataRequired(message="Title cannot be empty"), 
            Length(max=50, message="Title cannot be longer than 50 characters")
        ]
    )
    caption = StringField("Caption", 
        validators=[
            DataRequired(message="Caption cannot be empty"), 
            Length(max=200, message="Caption cannot be longer than 200 characters")
        ], 
        widget=TextArea()
    )
    image = FileField("Photo", 
        validators=[

        ]
    )
    submit = SubmitField("Post")

class CommentForm(FlaskForm):
    content = StringField("Comment",
        validators=[
            DataRequired(message="Comment cannot be empty"),
            Length(max=200, message="Comment cannot be longer than 200 characters")
        ]
    )
    submit = SubmitField("Comment")