from flask_security import Security, SQLAlchemyUserDatastore
from app import app
from models import User, Role, db
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore, token_authentication_enabled=True)