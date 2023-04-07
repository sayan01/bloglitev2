#!/bin/env python3
from flask import Flask

app = Flask(__name__)

# configure Flask app
import config

# Import Flask-WTF forms classes
from forms import *

# Init DB and declare all db models
from models import *

# Init Flask_Login Manager
import auth

# Init routes
from routes import *

if __name__ == '__main__':
    app.run()
