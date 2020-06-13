import app.domain.user.service as service
from http import HTTPStatus
from flask import Blueprint, request
from flask_jwt_extended import jwt_required
from app.helper.response import response_success
from app.helper.error import InvalidRequest
from app.domain.user.schema import CreationSchema, EditingSchema

blueprint = Blueprint('user', __name__)


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
