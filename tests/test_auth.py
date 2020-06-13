import json
import pytest
from http import HTTPStatus


def test_login(client, action):
    response = client.post('/api/auth/login',
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
    response = client.post('/api/auth/login',
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
    response = client.post('/api/auth/login',
                           data=json.dumps(dict(
                               username=username,
                               password=password
                           )),
                           content_type='application/json')
    data = json.loads(response.data)
    assert status_code == response.status_code
    assert message == data['message']


def test_logout(client, action):
    response = client.delete('/api/auth/logout', headers={'Authorization': 'Bearer ' + action.auth['access_token']})
    assert HTTPStatus.OK == response.status_code


def test_logout_without_auth(client, action):
    response = client.delete('/api/auth/logout')
    assert HTTPStatus.UNAUTHORIZED == response.status_code


def test_refresh_token(client, action):
    response = client.post('/api/auth/refresh_token',
                           headers={'Authorization': 'Bearer ' + action.auth['refresh_token']})
    data = json.loads(response.data)['data']
    assert HTTPStatus.OK == response.status_code
    assert data['access_token'] is not None
