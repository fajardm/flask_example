from http import HTTPStatus
from flask import abort
from flask_jwt_extended import get_jwt_identity
from datetime import datetime
from app.domain.list.model import List


def create(data):
    current_user = get_jwt_identity()
    list = List(data['name'], data['email'], data['clothes_size'], current_user)
    list.save()
    return list


def get(id):
    return List.get(id)


def get_list():
    return List.get_all()


def update(id, data):
    current_user = get_jwt_identity()
    list = List.get(id)
    if list.created_by != current_user:
        return abort(HTTPStatus.UNAUTHORIZED)
    list.name = data['name']
    list.email = data['email']
    list.clothes_size = data['clothes_size']
    list.updated = datetime.now()
    list.updated_by = current_user
    list.save()
    return list


def delete(id):
    current_user = get_jwt_identity()
    list = List.get(id)
    if list.created_by != current_user:
        return abort(HTTPStatus.UNAUTHORIZED)
    return list.delete()
