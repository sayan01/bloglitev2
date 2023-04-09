from dotenv import load_dotenv
from app import app
from os import getenv

# config
load_dotenv()
app.config['SQLALCHEMY_DATABASE_URI'] = getenv('SQLALCHEMY_DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = getenv('SQLALCHEMY_TRACK_MODIFICATIONS')
app.config['CELERY_BROKER_URL'] = "redis://localhost:6379/4"
app.config['CELERY_RESULT_BACKEND'] = "redis://localhost:6379/5"
app.config['REDIS_URL'] = "redis://localhost:6379/6"
app.config['CACHE_TYPE'] = 'RedisCache'
app.config['CACHE_REDIS_HOST'] = 'localhost'
app.config['CACHE_REDIS_PORT'] = 6379
app.config['CACHE_REDIS_DB'] = 7
app.config['SECRET_KEY'] = getenv('SECRET_KEY')
app.config['JWT_SECRET_KEY'] = getenv('SECRET_KEY') 

app.config['SMTP_SERVER_HOST'] = 'localhost'
app.config['SMTP_SERVER_PORT'] = 1025
app.config['SMTP_SERVER_EMAIL'] = 'noreply@localhost'
app.config['SMTP_SERVER_PASSWORD'] = 'password'