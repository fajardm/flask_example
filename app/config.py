import os
import datetime
from dotenv import load_dotenv

load_dotenv()


class Config(object):
    """Configuration class"""
    DEBUG = os.getenv('FLASK_DEBUG')
    TESTING = os.getenv('TESTING')
    SECRET_KEY = os.getenv('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URI")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_ACCESS_TOKEN_EXPIRES = datetime.timedelta(seconds=int(os.getenv('JWT_ACCESS_TOKEN_EXPIRES_SECONDS')) or 900)
    JWT_BLACKLIST_ENABLED = True
    JWT_BLACKLIST_TOKEN_CHECKS = ['access', 'refresh']
    UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER')
    ALLOWED_IMAGE_EXTENSIONS = os.getenv('ALLOWED_IMAGE_EXTENSIONS').split(',')
