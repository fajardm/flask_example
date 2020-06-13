import json
import pytest
from http import HTTPStatus


def test_create(client, action):
    response = client.post('/api/lists',
                           data=json.dumps(dict(
                               name='list name',
                               email='list@gmail.com',
                               clothes_size=32
                           )),
                           headers={'Authorization': 'Bearer ' + action.auth['access_token']},
                           content_type='application/json')
    data = json.loads(response.data)['data']
    assert HTTPStatus.CREATED == response.status_code
    assert data['name'] == 'list name'
    assert data['email'] == 'list@gmail.com'
    assert data['clothes_size'] == 32


@pytest.mark.parametrize(
    ('name', 'email', 'clothes_size', 'status_code'),
    (
            (None, None, None, HTTPStatus.BAD_REQUEST),
            ('list name', None, None, HTTPStatus.BAD_REQUEST),
            ('', '', '', HTTPStatus.BAD_REQUEST),
            ('', 'list@gmail.com', 32, HTTPStatus.BAD_REQUEST),
            ('', '', 32, HTTPStatus.BAD_REQUEST),
            ('list name', 'list@gmail.com', 0, HTTPStatus.BAD_REQUEST),
    ),
)
def test_create_validate_input(client, action, name, email, clothes_size, status_code):
    response = client.post('/api/lists',
                           data=json.dumps(dict(
                               name=name,
                               email=email,
                               clothes_size=clothes_size
                           )),
                           headers={'Authorization': 'Bearer ' + action.auth['access_token']},
                           content_type='application/json')
    print(json.loads(response.data))
    assert status_code == response.status_code


def test_create_without_auth(client):
    response = client.post('/api/lists',
                           data=json.dumps(dict(
                               name='list name',
                               email='list@gmail.com',
                               clothes_size=32
                           )),
                           content_type='application/json')
    assert HTTPStatus.UNAUTHORIZED == response.status_code


def test_list(client, action):
    response = client.get('/api/lists', headers={'Authorization': 'Bearer ' + action.auth['access_token']})
    data = json.loads(response.data)['data']
    assert HTTPStatus.OK == response.status_code
    assert len(data) == 3


def test_list_without_auth(client):
    response = client.get('/api/lists')
    assert HTTPStatus.UNAUTHORIZED == response.status_code


def test_get(client, action):
    response = client.get('/api/lists/' + action.list[0]['id'],
                          headers={'Authorization': 'Bearer ' + action.auth['access_token']})
    assert HTTPStatus.OK == response.status_code


def test_get_validate_id(client, action):
    response = client.get('/api/lists/1', headers={'Authorization': 'Bearer ' + action.auth['access_token']})
    assert HTTPStatus.NOT_FOUND == response.status_code


def test_get_without_auth(client, action):
    response = client.get('/api/lists/' + action.list[0]['id'])
    assert HTTPStatus.UNAUTHORIZED == response.status_code


def test_update(client, action):
    response = client.put('/api/lists/' + action.list[0]['id'],
                          data=json.dumps(dict(
                              name='list name update',
                              email='list_update@gmail.com',
                              clothes_size=36
                          )),
                          headers={'Authorization': 'Bearer ' + action.auth['access_token']},
                          content_type='application/json')
    data = json.loads(response.data)['data']
    assert HTTPStatus.OK == response.status_code
    assert data['name'] == 'list name update'
    assert data['email'] == 'list_update@gmail.com'
    assert data['clothes_size'] == 36


def test_update_validate_id(client, action):
    response = client.put('/api/lists/1',
                          data=json.dumps(dict(
                              name='list name update',
                              email='list_update@gmail.com',
                              clothes_size=36
                          )),
                          headers={'Authorization': 'Bearer ' + action.auth['access_token']},
                          content_type='application/json')
    assert HTTPStatus.NOT_FOUND == response.status_code


def test_update_without_auth(client, action):
    response = client.put('/api/lists/' + action.list[0]['id'],
                          data=json.dumps(dict(
                              name='list name update',
                              email='list_update@gmail.com',
                              clothes_size=36
                          )),
                          content_type='application/json')
    assert HTTPStatus.UNAUTHORIZED == response.status_code


@pytest.mark.parametrize(
    ('name', 'email', 'clothes_size', 'status_code'),
    (
            (None, None, None, HTTPStatus.BAD_REQUEST),
            ('list name', None, None, HTTPStatus.BAD_REQUEST),
            ('', '', '', HTTPStatus.BAD_REQUEST),
            ('', 'list@gmail.com', 32, HTTPStatus.BAD_REQUEST),
            ('', '', 32, HTTPStatus.BAD_REQUEST),
            ('list name', 'list@gmail.com', 0, HTTPStatus.BAD_REQUEST),
    ),
)
def test_update_validate_input(client, action, name, email, clothes_size, status_code):
    response = client.put('/api/lists/' + action.list[0]['id'],
                          data=json.dumps(dict(
                              name=name,
                              email=email,
                              clothes_size=clothes_size
                          )),
                          headers={'Authorization': 'Bearer ' + action.auth['access_token']},
                          content_type='application/json')
    assert status_code == response.status_code


def test_update_other_entity(client, action):
    action.auth = action.login('1test', 'secret')
    list = action.create_list()
    response = client.put('/api/lists/' + list[0]['id'],
                          data=json.dumps(dict(
                              name='list name update',
                              email='list_update@gmail.com',
                              clothes_size=36
                          )),
                          content_type='application/json')
    assert HTTPStatus.UNAUTHORIZED == response.status_code


def test_delete(client, action):
    response = client.delete('/api/lists/' + action.list[0]['id'],
                             headers={'Authorization': 'Bearer ' + action.auth['access_token']})
    assert HTTPStatus.OK == response.status_code


def test_delete_validate_id(client, action):
    response = client.delete('/api/lists/1', headers={'Authorization': 'Bearer ' + action.auth['access_token']})
    assert HTTPStatus.NOT_FOUND == response.status_code


def test_delete_without_auth(client, action):
    response = client.delete('/api/lists/' + action.list[0]['id'])
    assert HTTPStatus.UNAUTHORIZED == response.status_code


def test_delete_other_entity(client, action):
    action.auth = action.login('1test', 'secret')
    list = action.create_list()
    response = client.delete('/api/lists/' + list[0]['id'])
    assert HTTPStatus.UNAUTHORIZED == response.status_code
