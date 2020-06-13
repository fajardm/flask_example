from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from app.helper.error import error_handler
from app.config import Config

db = SQLAlchemy()
bcrypt = Bcrypt()
migrate = Migrate()
jwt_manager = JWTManager()


def create_app():
    """Application factory"""
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    bcrypt.init_app(app)
    migrate.init_app(app, db)
    jwt_manager.init_app(app)

    error_handler(app)

    @app.route('/')
    def ping():
        return "Flask Example is working!"

    from app.domain.user.resource import blueprint
    app.register_blueprint(blueprint, url_prefix='/api')

    from app.domain.auth.resource import blueprint
    app.register_blueprint(blueprint, url_prefix='/api')

    from app.domain.profile.resource import blueprint
    app.register_blueprint(blueprint, url_prefix='/api')

    from app.domain.list.resource import blueprint
    app.register_blueprint(blueprint, url_prefix='/api')

    from app.helper.jwt import jwt_handler
    jwt_handler(jwt_manager)

    return app
