from flask_sse import sse
from app import app

app.register_blueprint(sse, url_prefix='/stream')