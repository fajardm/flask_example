from http import HTTPStatus
from flask import jsonify


def response_success(data, status_code=HTTPStatus.OK):
    return jsonify({'status': 'success', 'data': data}), status_code


def response_fail(data, status_code=HTTPStatus.BAD_REQUEST):
    return jsonify({'status': 'fail', 'data': data}), status_code


def response_error(e):
    return jsonify({'status': 'error', 'message': e.description}), e.code
