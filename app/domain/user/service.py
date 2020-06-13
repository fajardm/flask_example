from http import HTTPStatus
from flask_jwt_extended import get_jwt_identity
from flask import abort
from app.domain.user.model import User


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
