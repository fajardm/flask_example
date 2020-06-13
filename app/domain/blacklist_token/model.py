import uuid
from datetime import datetime
from app import db


class BlacklistToken(db.Model):
    """Token model for storing blacklisted JWT tokens"""
    __tablename__ = "blacklist_tokens"

    id = db.Column(db.String(36), primary_key=True)
    token = db.Column(db.String(500), unique=True, nullable=False)
    created = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())

    def __init__(self, token):
        self.id = str(uuid.uuid4())
        self.token = token
        self.created = datetime.now()

    @staticmethod
    def get_by_token(token):
        return BlacklistToken.query.filter_by(token=token).first()

    def save(self):
        db.session.add(self)
        db.session.commit()

    def serialize(self):
        return {'id': self.id, 'token': self.token, 'created': self.created}

    def __repr__(self):
        return '<BlacklistToken %r>' % self.serialize()
