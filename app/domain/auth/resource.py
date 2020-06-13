import app.domain.auth.service as service
import app.domain.blacklist_token.service as blacklist_service
from http import HTTPStatus
from flask import Blueprint, request, abort
from flask_jwt_extended import jwt_required, get_raw_jwt, jwt_refresh_token_required
from app.helper.response import response_success
from app.helper.error import InvalidRequest
from app.domain.auth.schema import AuthenticationSchema

blueprint = Blueprint('auth', __name__)


@blueprint.route('/auth/test', methods=['GET'])
def login_test():
    return response_success(True)


@blueprint.route('/auth/login', methods=['POST'])
def login():
    data = request.get_json()
    error = AuthenticationSchema().validate(data)
    if error:
        raise InvalidRequest(message='Validation error', payload={'validation': error})
    res = service.login(data['username'], data['password'])
    if not res:
        return abort(HTTPStatus.UNAUTHORIZED, "Invalid username and/or password")
    return response_success(res)


@blueprint.route('/auth/logout', methods=['DELETE'])
@jwt_required
def logout():
    token = get_raw_jwt()['jti']
    blacklist_service.create(token)
    return response_success(True)


@blueprint.route('/auth/refresh_token', methods=['POST'])
@jwt_refresh_token_required
def refresh_token():
    res = service.refresh_token()
    return response_success(res)
