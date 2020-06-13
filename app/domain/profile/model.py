import uuid
from datetime import datetime
from app import db


class Profile(db.Model):
    """Profile model for storing user profile"""
    __tablename__ = "profiles"

    id = db.Column(db.String(36), primary_key=True)
    first_name = db.Column(db.String(32), nullable=False)
    last_name = db.Column(db.String(32), nullable=False)
    birth_of_date = db.Column(db.Date, nullable=False)
    picture_path = db.Column(db.String(256))
    user_id = db.Column(db.String(36), db.ForeignKey(column='users.id', ondelete="cascade"), unique=True,
                        nullable=False)
    created = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())
    created_by = db.Column(db.String(36), nullable=False)
    updated = db.Column(db.DateTime, onupdate=db.func.current_timestamp())
    updated_by = db.Column(db.String(36))

    def __init__(self, first_name, last_name, birth_of_date, user_id, picture=None):
        self.id = str(uuid.uuid4())
        self.first_name = first_name
        self.last_name = last_name
        self.birth_of_date = birth_of_date
        self.picture = picture
        self.user_id = user_id
        self.created = datetime.now()
        self.created_by = user_id
        pass

    @staticmethod
    def get(id):
        return Profile.query.filter_by(id=id).first_or_404()

    @staticmethod
    def get_by_user_id(user_id):
        return Profile.query.filter_by(user_id=user_id).first_or_404()

    @staticmethod
    def get_all():
        return Profile.query.all()

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def serialize(self):
        return {'id': self.id, 'first_name': self.first_name, 'last_name': self.last_name,
                'birth_of_date': self.birth_of_date.strftime('%Y-%m-%d'), 'picture_path': self.picture_path,
                'user_id': self.user_id, 'created': self.created, 'created_by': self.created_by,
                'updated': self.updated, 'updated_by': self.updated_by}

    def __repr__(self):
        return '<Profile %r>' % self.serialize()
