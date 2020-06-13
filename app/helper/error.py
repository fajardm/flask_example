from http import HTTPStatus
from werkzeug.exceptions import HTTPException
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
    @app.errorhandler(HTTPStatus.CONFLICT)
    @app.errorhandler(HTTPStatus.INTERNAL_SERVER_ERROR)
    def handler_known_error(e):
        return response_error(e)

    @app.errorhandler(Exception)
    def handle_500(e):
        app.logger.error(e)
        e = HTTPException(description='Internal server error')
        e.code = HTTPStatus.INTERNAL_SERVER_ERROR
        return response_error(e)
