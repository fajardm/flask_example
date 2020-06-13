import os
import json
import pytest
import tempfile
import shutil
from app import create_app, db
from app.config import Config


@pytest.fixture
def app():
    """Create and configure a new app instance for each test."""
    # create a temporary file to isolate the database for each test
    db_fd, db_path = tempfile.mkstemp()
    upload_path = tempfile.mkdtemp()
    # create the app with common test config
    Config.SQLALCHEMY_DATABASE_URI = 'sqlite:////' + db_path
    Config.UPLOAD_FOLDER = upload_path
    Config.TESTING = True
    app = create_app()
    # create the database
    with app.app_context():
        db.create_all()
    yield app
    # close and remove the temporary database
    os.close(db_fd)
    os.unlink(db_path)
    shutil.rmtree(upload_path)


@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()


class Action(object):
    def __init__(self, client):
        self._client = client
        self.users = self.create_users()
        self.auth = self.login()
        self.list = self.create_list()

    def create_users(self):
        data = [
            {'email': 'test@gmail.com', 'username': 'test', 'password': 'secret'},
            {'email': 'test1@gmail.com', 'username': '1test', 'password': 'secret'},
            {'email': 'test2@gmail.com', 'username': '2test', 'password': 'secret'},
        ]
        users = []
        for item in data:
            response = self._client.post('/api/users', data=json.dumps(item), content_type='application/json')
            users.append(json.loads(response.data)['data'])
        return users

    def create_list(self):
        data = [
            {'name': 'list 1', 'email': 'list1@gmail.com', 'clothes_size': 32},
            {'name': 'list 2', 'email': 'list2@gmail.com', 'clothes_size': 32},
            {'name': 'list 3', 'email': 'list3@gmail.com', 'clothes_size': 32},
        ]
        lists = []
        for item in data:
            response = self._client.post('/api/lists',
                                         data=json.dumps(item),
                                         content_type='application/json',
                                         headers={'Authorization': 'Bearer ' + self.auth['access_token']})
            lists.append(json.loads(response.data)['data'])
        return lists

    def create_profile(self):
        response = self._client.post('/api/profiles',
                                     data={'first_name': 'first', 'last_name': 'last', 'birth_of_date': '2020-01-01',
                                           'picture': None},
                                     headers={'Authorization': 'Bearer ' + self.auth['access_token']},
                                     content_type='multipart/form-data')
        return json.loads(response.data)['data']

    def login(self, username="test", password="secret"):
        response = self._client.post('/api/auth/login',
                                     data=json.dumps(dict(
                                         username=username,
                                         password=password
                                     )),
                                     content_type='application/json')
        return json.loads(response.data)['data']

    def logout(self):
        response = self._client.delete('/api/auth/logout',
                                       headers={'Authorization': 'Bearer ' + self.auth['access_token']})
        return json.loads(response.data)['data']


@pytest.fixture
def action(client):
    return Action(client)
