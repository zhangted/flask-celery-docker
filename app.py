import os
from flask import Flask, jsonify
from helpers import celery_init_app
from clients import get_redis_connection

flask_app = Flask(__name__)
flask_app.config.from_mapping(
    CELERY=dict(
        broker_url=os.getenv('CELERY_BROKER_URL'),
        result_backend=os.getenv('CELERY_RESULT_BACKEND'),
        task_ignore_result=True,
    ),
)
celery_app = celery_init_app(flask_app)

@flask_app.before_first_request
def connect_to_services():
  flask_app.config['REDIS_CLIENT'] = get_redis_connection()

@flask_app.route("/")
def index():
  return 'Hello, World!'

@flask_app.route("/check_redis")
def check_redis_conn():
  if flask_app.config['REDIS_CLIENT'] is not None: return 'Redis connection is live'
  return 'No redis connection'

@flask_app.route("/queue_task")
def queue_task():
  celery_app.send_task('tasks.task1._dummy_task_func')
  return 'task queued. check console for output'

if __name__ == "__main__":
  flask_app.run(debug=True, host='0.0.0.0')