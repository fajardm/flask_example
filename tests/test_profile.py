import os
import pathlib
import json
import pytest
from io import BytesIO
from http import HTTPStatus

current_path = pathlib.Path(__file__).parent.absolute()


def get_image_file():
    return BytesIO(open(os.path.join(current_path, 'image_1024.png'), 'rb').read()), 'image_1024.png'


def test_create(client, action):
    response = client.post('/api/profiles',
                           data={'first_name': 'first', 'last_name': 'last', 'birth_of_date': '2020-01-01',
                                 'picture': get_image_file()},
                           headers={'Authorization': 'Bearer ' + action.auth['access_token']},
                           content_type='multipart/form-data')
    data = json.loads(response.data)['data']
    assert HTTPStatus.CREATED == response.status_code
    assert data['first_name'] == 'first'
    assert data['last_name'] == 'last'
    assert data['birth_of_date'] == '2020-01-01'
    assert data['picture_path'] is not None


@pytest.mark.parametrize(
    ('first_name', 'last_name', 'birth_of_date', 'picture', 'status_code'),
    (
            (None, None, None, None, HTTPStatus.BAD_REQUEST),
            ('first', None, None, None, HTTPStatus.BAD_REQUEST),
            ('first', 'last', None, None, HTTPStatus.BAD_REQUEST),
            ('first', 'last', '01-01-2020', None, HTTPStatus.BAD_REQUEST),
            ('first', 'last', '2020-01-01', get_image_file(), HTTPStatus.CREATED),
    ),
)
def test_create_validate_input(client, action, first_name, last_name, birth_of_date, picture, status_code):
    response = client.post('/api/profiles',
                           data={'first_name': first_name, 'last_name': last_name, 'birth_of_date': birth_of_date,
                                 'picture': picture},
                           headers={'Authorization': 'Bearer ' + action.auth['access_token']},
                           content_type='multipart/form-data')
    assert status_code == response.status_code


def test_create_without_auth(client, action):
    response = client.post('/api/profiles',
                           data={'first_name': 'first', 'last_name': 'last', 'birth_of_date': '2020-01-01',
                                 'picture': None},
                           content_type='multipart/form-data')
    assert HTTPStatus.UNAUTHORIZED == response.status_code


def test_list(client, action):
    action.create_profile()
    response = client.get('/api/profiles', headers={'Authorization': 'Bearer ' + action.auth['access_token']})
    data = json.loads(response.data)['data']
    assert HTTPStatus.OK == response.status_code
    assert len(data) == 1


def test_list_without_auth(client):
    response = client.get('/api/profiles')
    assert HTTPStatus.UNAUTHORIZED == response.status_code


def test_get(client, action):
    profile = action.create_profile()
    response = client.get('/api/profiles/' + profile['user_id'],
                          headers={'Authorization': 'Bearer ' + action.auth['access_token']})
    assert HTTPStatus.OK == response.status_code


def test_get_validate_id(client, action):
    response = client.get('/api/profiles/1', headers={'Authorization': 'Bearer ' + action.auth['access_token']})
    assert HTTPStatus.NOT_FOUND == response.status_code


def test_get_without_auth(client, action):
    profile = action.create_profile()
    response = client.get('/api/profiles/' + profile['user_id'])
    assert HTTPStatus.UNAUTHORIZED == response.status_code


def test_update(client, action):
    profile = action.create_profile()
    response = client.put('/api/profiles/' + profile['user_id'],
                          data={'first_name': 'first updated', 'last_name': 'last updated',
                                'birth_of_date': '2020-01-02'},
                          headers={'Authorization': 'Bearer ' + action.auth['access_token']},
                          content_type='multipart/form-data')
    data = json.loads(response.data)['data']
    assert HTTPStatus.OK == response.status_code
    assert data['first_name'] == 'first updated'
    assert data['last_name'] == 'last updated'
    assert data['birth_of_date'] == '2020-01-02'


def test_update_validate_id(client, action):
    action.create_profile()
    response = client.put('/api/profiles/1',
                          data={'first_name': 'first updated', 'last_name': 'last updated ',
                                'birth_of_date': '2020-01-02'},
                          headers={'Authorization': 'Bearer ' + action.auth['access_token']},
                          content_type='multipart/form-data')
    assert HTTPStatus.NOT_FOUND == response.status_code


def test_update_without_auth(client, action):
    profile = action.create_profile()
    response = client.put('/api/profiles/' + profile['user_id'],
                          data={'first_name': 'first updated', 'last_name': 'last updated ',
                                'birth_of_date': '2020-01-02'},
                          content_type='multipart/form-data')
    assert HTTPStatus.UNAUTHORIZED == response.status_code


def test_update_other_entity(client, action):
    action.auth = action.login('1test', 'secret')
    profile = action.create_profile()
    response = client.put('/api/profiles/' + profile['user_id'],
                          data={'first_name': 'first updated', 'last_name': 'last updated ',
                                'birth_of_date': '2020-01-02'},
                          content_type='multipart/form-data')
    assert HTTPStatus.UNAUTHORIZED == response.status_code


def test_delete(client, action):
    profile = action.create_profile()
    response = client.delete('/api/profiles/' + profile['user_id'],
                             headers={'Authorization': 'Bearer ' + action.auth['access_token']})
    assert HTTPStatus.OK == response.status_code


def test_delete_validate_id(client, action):
    response = client.delete('/api/profiles/1', headers={'Authorization': 'Bearer ' + action.auth['access_token']})
    assert HTTPStatus.NOT_FOUND == response.status_code


def test_delete_without_auth(client, action):
    profile = action.create_profile()
    response = client.delete('/api/profiles/' + profile['user_id'])
    assert HTTPStatus.UNAUTHORIZED == response.status_code


def test_delete_other_entity(client, action):
    action.auth = action.login('1test', 'secret')
    profile = action.create_profile()
    response = client.delete('/api/profiles/' + profile['user_id'])
    assert HTTPStatus.UNAUTHORIZED == response.status_code
