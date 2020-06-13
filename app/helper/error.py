from http import HTTPStatus
from app.helper.response import response_error, response_fail


class InvalidRequest(Exception):
    """Custom error class for invalid request"""
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv


def error_handler(app):
    @app.errorhandler(InvalidRequest)
    def invalid_request(e):
        return response_fail(status_code=e.status_code, data=e.to_dict())

    @app.errorhandler(HTTPStatus.NOT_FOUND)
    @app.errorhandler(HTTPStatus.UNAUTHORIZED)
    @app.errorhandler(HTTPStatus.INTERNAL_SERVER_ERROR)
    @app.errorhandler(HTTPStatus.CONFLICT)
    def _error_handler(e):
        return response_error(e)
