import app.domain.profile.service as service
from http import HTTPStatus
from flask import Blueprint, request
from flask_jwt_extended import jwt_required
from marshmallow import ValidationError
from app.helper.response import response_success
from app.helper.error import InvalidRequest
from app.domain.profile.schema import CreationSchema, EditingSchema

blueprint = Blueprint('profile', __name__)


@blueprint.route('/profiles', methods=['POST'])
@jwt_required
def create():
    try:
        data = CreationSchema().load(data=request.form)
        if request.files and request.files['picture']:
            data['picture'] = request.files['picture']
        res = service.create(data)
        return response_success(res.serialize(), HTTPStatus.CREATED)
    except ValidationError as err:
        raise InvalidRequest(message='Validation error', payload={'validation': err.messages})


@blueprint.route('/profiles', methods=['GET'])
@jwt_required
def list():
    res = service.get_list()
    return response_success([i.serialize() for i in res])


@blueprint.route('/profiles/<user_id>', methods=['GET'])
@jwt_required
def get(user_id):
    res = service.get(user_id)
    return response_success(res.serialize())


@blueprint.route('/profiles/<user_id>', methods=['PUT'])
@jwt_required
def update(user_id):
    try:
        data = EditingSchema().load(data=request.form)
        if request.files and request.files['picture']:
            data['picture'] = request.files['picture']
        res = service.update(user_id, data)
        return response_success(res.serialize(), HTTPStatus.OK)
    except ValidationError as err:
        raise InvalidRequest(message='Validation error', payload={'validation': err.messages})


@blueprint.route('/profiles/<user_id>', methods=['DELETE'])
@jwt_required
def delete(user_id):
    service.delete(user_id)
    return response_success(True)
