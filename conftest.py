import pytest
import app

@pytest.fixture(scope='module')
def app_instance():
  return app

@pytest.fixture(scope='module')
def app_client():
  return app.flask_app.test_client()

@pytest.fixture(scope='module')
def celery_instance():
  return app.celery_app