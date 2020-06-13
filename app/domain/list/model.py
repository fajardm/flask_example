import uuid
from datetime import datetime
from app import db


class List(db.Model):
    """List model for storing list data"""
    __tablename__ = "lists"

    id = db.Column(db.String(36), primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(128), nullable=False)
    clothes_size = db.Column(db.SmallInteger, nullable=False)
    created = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())
    created_by = db.Column(db.String(36), nullable=False)
    updated = db.Column(db.DateTime, onupdate=db.func.current_timestamp())
    updated_by = db.Column(db.String(36))

    def __init__(self, name, email, clothes_size, user_id):
        self.id = str(uuid.uuid4())
        self.name = name
        self.email = email
        self.clothes_size = clothes_size
        self.created = datetime.now()
        self.created_by = user_id
        pass

    @staticmethod
    def get(id):
        return List.query.filter_by(id=id).first_or_404()

    @staticmethod
    def get_all():
        return List.query.all()

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def serialize(self):
        return {'id': self.id, 'name': self.name, 'email': self.email, 'clothes_size': self.clothes_size,
                'created': self.created, 'created_by': self.created_by, 'updated': self.updated,
                'updated_by': self.updated_by}

    def __repr__(self):
        return '<Profile %r>' % self.serialize()
