from app import app
from celery import Task, Celery

class ContextTask(Task):
    def __call__(self, *args, **kwargs):
        with app.app_context():
            return super(ContextTask, self).__call__(*args, **kwargs)

celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'], backend=app.config['CELERY_RESULT_BACKEND'])
celery.conf.update(timezone='Asia/Kolkata', enable_utc=True)
celery.Task = ContextTask
