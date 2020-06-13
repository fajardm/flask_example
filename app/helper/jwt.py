from http import HTTPStatus
from werkzeug.exceptions import HTTPException
from app.helper.response import response_error
from app.domain.blacklist_token.model import BlacklistToken


def jwt_handler(jwt):
    @jwt.claims_verification_failed_loader
    def claims_verification_failed_loader():
        e = HTTPException(description='User claims verification failed')
        e.code = HTTPStatus.UNAUTHORIZED
        return response_error(e)

    @jwt.expired_token_loader
    def expired_token_loader(expired_token):
        e = HTTPException(description='Token has expired')
        e.code = HTTPStatus.UNAUTHORIZED
        return response_error(e)

    @jwt.invalid_token_loader
    def invalid_token_loader(message):
        e = HTTPException(description=message)
        e.code = HTTPStatus.BAD_REQUEST
        return response_error(e)

    @jwt.needs_fresh_token_loader
    def needs_fresh_token_loader():
        e = HTTPException(description='Fresh token required')
        e.code = HTTPStatus.UNAUTHORIZED
        return response_error(e)

    @jwt.revoked_token_loader
    def revoked_token_loader():
        e = HTTPException(description='Token has been revoked')
        e.code = HTTPStatus.UNAUTHORIZED
        return response_error(e)

    @jwt.token_in_blacklist_loader
    def token_in_blacklist_loader(decrypted_token):
        token = decrypted_token['jti']
        return BlacklistToken.get_by_token(token)

    @jwt.unauthorized_loader
    def unauthorized_loader(message):
        e = HTTPException(description=message)
        e.code = HTTPStatus.UNAUTHORIZED
        return response_error(e)

    @jwt.user_loader_error_loader
    def user_loader_error_loader(identity):
        e = HTTPException(description='Error loading the user %r' % identity)
        e.code = HTTPStatus.UNAUTHORIZED
        return response_error(e)
