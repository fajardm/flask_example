from http import HTTPStatus
from flask import abort
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity
from app.domain.user.model import User
from app.config import Config


def login(username, password):
    user = User.query.filter_by(username=username).first()
    if user and user.check_password(password):
        return {'access_token': create_access_token(identity=user.id),
                'access_token_expires': Config.JWT_ACCESS_TOKEN_EXPIRES.seconds,
                'refresh_token': create_refresh_token(identity=user.id)}
    return None


def refresh_token():
    current_user = get_jwt_identity()
    return {'access_token': create_access_token(identity=current_user)}


def get_list():
    return User.get_all()


def create(data):
    user = User(username=data['username'], email=data['email'], password=data['password'])
    user.save()
    return user


def get(id):
    return User.get(id)


def update(id, data):
    current_user = get_jwt_identity()
    user = User.get(id)
    if user.id != current_user:
        return abort(HTTPStatus.UNAUTHORIZED)
    user.email = data['email']
    user.password = data['password']
    user.save()
    return user


def delete(id):
    current_user = get_jwt_identity()
    user = User.get(id)
    if user.id != current_user:
        return abort(HTTPStatus.UNAUTHORIZED)
    return user.delete()
