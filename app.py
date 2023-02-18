from flask import Flask
from celery import Celery, Task
import redis
import os

def celery_init_app(app: Flask) -> Celery:
  class FlaskTask(Task):
      def __call__(self, *args: object, **kwargs: object) -> object:
          with app.app_context():
              return self.run(*args, **kwargs)

  celery_app = Celery(app.name, task_cls=FlaskTask)
  celery_app.config_from_object(app.config["CELERY"])
  celery_app.set_default()
  app.extensions["celery"] = celery_app
  return celery_app

flask_app = Flask(__name__)
flask_app.config.from_mapping(
    CELERY=dict(
        broker_url=os.getenv('CELERY_BROKER_URL'),
        result_backend=os.getenv('CELERY_RESULT_BACKEND'),
        task_ignore_result=True,
    ),
)
celery_app = celery_init_app(flask_app)

@celery_app.task
def task1():
  print('task received')

@flask_app.route("/")
def hello():
  return 'Hello, World!'

@flask_app.route("/queue_task")
def hello2():
  task1.delay()
  return 'task queued. check console for output'

if __name__ == "__main__":
  flask_app.run(debug=True, host='0.0.0.0')