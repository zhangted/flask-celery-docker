import pytest

def test_app_index(app_instance):
  assert app_instance.index() == 'Hello, World!'

def test_app_redis_conn(app_client):
  response = app_client.get('/check_redis') 
  assert 'Redis connection is live' in str(response.data)

def test_app_index_clientside(app_client):
  response = app_client.get('/')
  print(response)
  assert response.status_code == 200
  assert 'Hello, World!' in str(response.data)

def test_queue_task(mocker, app_instance, celery_instance):
  spy = mocker.spy(celery_instance, 'send_task')
  app_instance.queue_task()
  spy.assert_called_once_with('tasks.task1._dummy_task_func')