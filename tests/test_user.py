import json
import pytest
from http import HTTPStatus


def test_login(client, action):
    response = client.post('/api/users/login',
                           data=json.dumps(dict(
                               username='test',
                               password='secret'
                           )),
                           content_type='application/json')
    data = json.loads(response.data)['data']
    assert HTTPStatus.OK == response.status_code
    assert data['access_token'] is not None
    assert data['refresh_token'] is not None


@pytest.mark.parametrize(
    ('username', 'password', 'status_code'),
    (
            (None, None, HTTPStatus.BAD_REQUEST),
            ('new_test', None, HTTPStatus.BAD_REQUEST),
            (None, 'secret', HTTPStatus.BAD_REQUEST),
    ),
)
def test_login_validate_input(client, action, username, password, status_code):
    response = client.post('/api/users/login',
                           data=json.dumps(dict(
                               username=username,
                               password=password
                           )),
                           content_type='application/json')
    assert status_code == response.status_code


@pytest.mark.parametrize(
    ('username', 'password', 'status_code', 'message'),
    (
            ('', '', HTTPStatus.UNAUTHORIZED, 'Invalid username and/or password'),
            ('user_not_found', 'secret', HTTPStatus.UNAUTHORIZED, 'Invalid username and/or password'),
            ('test', 'invalid_password', HTTPStatus.UNAUTHORIZED, 'Invalid username and/or password'),
    ),
)
def test_login_validate_authentication(client, action, username, password, status_code, message):
    response = client.post('/api/users/login',
                           data=json.dumps(dict(
                               username=username,
                               password=password
                           )),
                           content_type='application/json')
    data = json.loads(response.data)
    assert status_code == response.status_code
    assert message == data['message']


def test_logout(client, action):
    response = client.delete('/api/users/logout', headers={'Authorization': 'Bearer ' + action.auth['access_token']})
    assert HTTPStatus.OK == response.status_code


def test_logout_without_auth(client, action):
    response = client.delete('/api/users/logout')
    assert HTTPStatus.UNAUTHORIZED == response.status_code


def test_refresh_token(client, action):
    response = client.post('/api/users/refresh_token',
                           headers={'Authorization': 'Bearer ' + action.auth['refresh_token']})
    data = json.loads(response.data)['data']
    assert HTTPStatus.OK == response.status_code
    assert data['access_token'] is not None


def test_create(client):
    response = client.post('/api/users',
                           data=json.dumps(dict(
                               email='test1@gmail.com',
                               username='test1',
                               password='secret'
                           )),
                           content_type='application/json')
    data = json.loads(response.data)['data']
    assert HTTPStatus.CREATED == response.status_code
    assert data['email'] == 'test1@gmail.com'
    assert data['username'] == 'test1'


@pytest.mark.parametrize(
    ('email', 'username', 'password', 'status_code'),
    (
            (None, None, None, HTTPStatus.BAD_REQUEST),
            ('new_test@gmail.com', None, None, HTTPStatus.BAD_REQUEST),
            ('new_test@gmail.com', 'new_test', None, HTTPStatus.BAD_REQUEST),
            ('', '', '', HTTPStatus.BAD_REQUEST),
            ('new_test', '', '', HTTPStatus.BAD_REQUEST),
            ('new_test@gmail.com', 'new_test', '', HTTPStatus.BAD_REQUEST),
            ('invalid_email', 'new_test', 'new_test', HTTPStatus.BAD_REQUEST),
            ('test@gmail.com', 'test', 'secret', HTTPStatus.CONFLICT),
    ),
)
def test_create_validate_input(client, action, email, username, password, status_code):
    response = client.post("/api/users",
                           data=json.dumps(dict(
                               email=email,
                               username=username,
                               password=password
                           )),
                           content_type='application/json')
    assert status_code == response.status_code


def test_list(client, action):
    response = client.get('/api/users', headers={'Authorization': 'Bearer ' + action.auth['access_token']})
    data = json.loads(response.data)['data']
    assert HTTPStatus.OK == response.status_code
    assert len(data) == 3


def test_list_without_auth(client):
    response = client.get('/api/users')
    assert HTTPStatus.UNAUTHORIZED == response.status_code


def test_get(client, action):
    response = client.get('/api/users/' + action.users[0]['id'],
                          headers={'Authorization': 'Bearer ' + action.auth['access_token']})
    assert HTTPStatus.OK == response.status_code


def test_get_validate_id(client, action):
    response = client.get('/api/users/1', headers={'Authorization': 'Bearer ' + action.auth['access_token']})
    assert HTTPStatus.NOT_FOUND == response.status_code


def test_get_without_auth(client, action):
    response = client.get('/api/users/' + action.users[0]['id'])
    assert HTTPStatus.UNAUTHORIZED == response.status_code


def test_update(client, action):
    response = client.put('/api/users/' + action.users[0]['id'],
                          data=json.dumps(dict(
                              email='test_update@gmail.com',
                              username='test_update',
                              password='secret'
                          )),
                          headers={'Authorization': 'Bearer ' + action.auth['access_token']},
                          content_type='application/json')
    data = json.loads(response.data)['data']
    assert HTTPStatus.OK == response.status_code
    assert data['email'] == 'test_update@gmail.com'
    assert data['username'] == 'test'


def test_update_validate_id(client, action):
    response = client.put('/api/users/1',
                          data=json.dumps(dict(
                              email='test_update@gmail.com',
                              username='test_update',
                              password='secret'
                          )),
                          headers={'Authorization': 'Bearer ' + action.auth['access_token']},
                          content_type='application/json')
    assert HTTPStatus.NOT_FOUND == response.status_code


@pytest.mark.parametrize(
    ('email', 'username', 'password', 'status_code'),
    (
            ('', '', '', HTTPStatus.BAD_REQUEST),
            ('test_updated@gmail.com', '', '', HTTPStatus.BAD_REQUEST),
            ('test_updated@gmail.com', 'test_updated', '', HTTPStatus.BAD_REQUEST),
            ('invalid_email', 'test_updated', 'test_updated', HTTPStatus.BAD_REQUEST),
            ('test_updated@gmail.com', '', 'test_updated', HTTPStatus.OK),
            ('test1@gmail.com', '1test', 'secret', HTTPStatus.INTERNAL_SERVER_ERROR),
    ),
)
def test_update_validate_input(client, action, email, username, password, status_code):
    response = client.put('/api/users/' + action.users[0]['id'],
                          data=json.dumps(dict(
                              email=email,
                              username=username,
                              password=password
                          )),
                          headers={'Authorization': 'Bearer ' + action.auth['access_token']},
                          content_type='application/json')
    assert status_code == response.status_code


def test_update_without_auth(client, action):
    response = client.put('/api/users/' + action.users[0]['id'],
                          data=json.dumps(dict(
                              email='test_update@gmail.com',
                              username='test_update',
                              password='secret'
                          )),
                          content_type='application/json')
    assert HTTPStatus.UNAUTHORIZED == response.status_code


def test_update_other_entity(client, action):
    response = client.put('/api/users/' + action.users[1]['id'],
                          data=json.dumps(dict(
                              email='test_update@gmail.com',
                              username='test_update',
                              password='secret'
                          )),
                          headers={'Authorization': 'Bearer ' + action.auth['access_token']},
                          content_type='application/json')
    assert HTTPStatus.UNAUTHORIZED == response.status_code


def test_delete(client, action):
    response = client.delete('/api/users/' + action.users[0]['id'],
                             headers={'Authorization': 'Bearer ' + action.auth['access_token']})
    assert HTTPStatus.OK == response.status_code


def test_delete_validate_id(client, action):
    response = client.delete('/api/users/1', headers={'Authorization': 'Bearer ' + action.auth['access_token']})
    assert HTTPStatus.NOT_FOUND == response.status_code


def test_delete_without_auth(client, action):
    response = client.delete('/api/users/' + action.users[0]['id'])
    assert HTTPStatus.UNAUTHORIZED == response.status_code


def test_delete_other_entity(client, action):
    response = client.delete('/api/users/' + action.users[1]['id'],
                             headers={'Authorization': 'Bearer ' + action.auth['access_token']})
    assert HTTPStatus.UNAUTHORIZED == response.status_code
