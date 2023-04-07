#!/bin/env python3
from flask import Flask

app = Flask(__name__)

# configure Flask app
import config

# Init DB and declare all db models
from models import *

# Setup flask security
import auth

import api

if __name__ == '__main__':
    app.run()
