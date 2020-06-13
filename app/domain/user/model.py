import uuid
from datetime import datetime
from app import db, bcrypt


class User(db.Model):
    """User Model for storing user data"""
    __tablename__ = "users"

    id = db.Column(db.String(36), primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(128), unique=True, nullable=False)
    password_hash = db.Column(db.String(100), nullable=False)
    created = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())
    updated = db.Column(db.DateTime, onupdate=db.func.current_timestamp())

    def __init__(self, username, email, password):
        self.id = str(uuid.uuid4())
        self.username = username
        self.email = email
        self.password = password
        self.created = datetime.now()
        pass

    @property
    def password(self):
        raise AttributeError('password: write-only field')

    @password.setter
    def password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

    @staticmethod
    def get(id):
        return User.query.filter_by(id=id).first_or_404()

    @staticmethod
    def get_all():
        return User.query.all()

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def serialize(self):
        return {'id': self.id, 'username': self.username, 'email': self.email, 'created': self.created,
                'updated': self.updated}

    def __repr__(self):
        return '<User %r>' % self.serialize()
