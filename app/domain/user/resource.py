import app.domain.user.service as service
import app.domain.blacklist_token.service as blacklist_service
from http import HTTPStatus
from flask import Blueprint, request, abort
from flask_jwt_extended import jwt_required, get_raw_jwt, jwt_refresh_token_required
from app.helper.response import response_success
from app.helper.error import InvalidRequest
from app.domain.user.schema import CreationSchema, EditingSchema, LoginSchema

blueprint = Blueprint('user', __name__)


@blueprint.route('/users/login', methods=['POST'])
def login():
    data = request.get_json()
    error = LoginSchema().validate(data)
    if error:
        raise InvalidRequest(message='Validation error', payload={'validation': error})
    res = service.login(data['username'], data['password'])
    if not res:
        return abort(HTTPStatus.UNAUTHORIZED, "Invalid username and/or password")
    return response_success(res)


@blueprint.route('/users/logout', methods=['DELETE'])
@jwt_required
def logout():
    token = get_raw_jwt()['jti']
    blacklist_service.create(token)
    return response_success(True)


@blueprint.route('/users/refresh_token', methods=['POST'])
@jwt_refresh_token_required
def refresh_token():
    res = service.refresh_token()
    return response_success(res)


@blueprint.route('/users', methods=['POST'])
def create():
    data = request.get_json()
    error = CreationSchema().validate(data)
    if error:
        raise InvalidRequest(message='Validation error', payload={'validation': error})
    res = service.create(data)
    return response_success(res.serialize(), HTTPStatus.CREATED)


@blueprint.route('/users', methods=['GET'])
@jwt_required
def list():
    res = service.get_list()
    return response_success([i.serialize() for i in res])


@blueprint.route('/users/<id>', methods=['GET'])
@jwt_required
def get(id):
    res = service.get(id)
    return response_success(res.serialize())


@blueprint.route('/users/<id>', methods=['PUT'])
@jwt_required
def update(id):
    data = request.get_json()
    error = EditingSchema().validate(data)
    if error:
        raise InvalidRequest(message='Validation error', payload={'validation': error})
    res = service.update(id, data)
    return response_success(res.serialize())


@blueprint.route('/users/<id>', methods=['DELETE'])
@jwt_required
def delete(id):
    service.delete(id)
    return response_success(True)
