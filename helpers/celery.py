from celery import Celery, Task
from flask import Flask

def register_tasks(celery_app: Celery) -> Celery:
  import tasks
  for attr_key in dir(tasks):
    value = getattr(tasks, attr_key)
    if callable(value): 
      task_func = value
      celery_app.task(task_func)
  return celery_app

def celery_init_app(app: Flask) -> Celery:
  class FlaskTask(Task):
      def __call__(self, *args: object, **kwargs: object) -> object:
          with app.app_context():
              return self.run(*args, **kwargs)

  celery_app = Celery(app.name, task_cls=FlaskTask)
  celery_app.config_from_object(app.config["CELERY"])
  celery_app.set_default()
  app.extensions["celery"] = celery_app

  return register_tasks(celery_app)