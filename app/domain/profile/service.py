import os
from http import HTTPStatus
from flask import abort
from flask_jwt_extended import get_jwt_identity
from werkzeug.datastructures import FileStorage
from datetime import datetime
from werkzeug.utils import secure_filename
from app.domain.profile.model import Profile
from app.config import Config
from app.helper.error import InvalidRequest


def allowed_image(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_IMAGE_EXTENSIONS


def save_image(file):
    current_user = get_jwt_identity()
    if not allowed_image(file.filename):
        raise InvalidRequest(message='Image extension not allowed')
    filename = secure_filename(file.filename)
    path = os.path.join(Config.UPLOAD_FOLDER, current_user + '.' + filename.rsplit('.', 1)[1].lower())
    file.save(path)
    return path


def create(data):
    current_user = get_jwt_identity()
    profile = Profile.query.filter_by(user_id=current_user).first()
    if profile:
        return abort(HTTPStatus.CONFLICT, 'Entity already exists')
    profile = Profile(data['first_name'], data['last_name'], data['birth_of_date'], current_user)
    if isinstance(data.get('picture'), FileStorage):
        path = save_image(data['picture'])
        profile.picture_path = path
    profile.save()
    return profile


def get(id):
    return Profile.get_by_user_id(id)


def get_list():
    return Profile.get_all()


def update(id, data):
    current_user = get_jwt_identity()
    profile = Profile.get_by_user_id(id)
    if profile.user_id != current_user:
        return abort(HTTPStatus.UNAUTHORIZED)
    profile.first_name = data['first_name']
    profile.last_name = data['last_name']
    profile.birth_of_date = data['birth_of_date']
    profile.user_id = current_user
    profile.updated = datetime.now()
    profile.updated_by = current_user
    if isinstance(data.get('picture'), FileStorage):
        if os.path.exists(profile.picture_path):
            os.remove(profile.picture_path)
        path = save_image(data['picture'])
        profile.picture_path = path
    profile.save()
    return profile


def delete(id):
    current_user = get_jwt_identity()
    profile = Profile.get_by_user_id(id)
    if profile.user_id != current_user:
        return abort(HTTPStatus.UNAUTHORIZED)
    return profile.delete()
