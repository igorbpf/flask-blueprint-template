from . import db
from .base import Base

class User(Base):

    __tablename__ = 'users'

    username = db.Column(db.String(20), unique=True, index=True)
    email = db.Column(db.String(50), unique=True, index=True)
    hashed_password = db.Column(db.String(100))
    email_confirmed = db.Column(db.Boolean)

    #todos = db.relationship('Todo', backref='user', lazy='dynamic')

    def __init__(self, username, email):
        self.username = username
        self.email = email
        self.email_confirmed = False
    #
    # def hash_password(self, password):
    #     self.hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    #
    # def verify_password(self, password):
    #     return bcrypt.check_password_hash(self.hashed_password, password)
    #
    # def is_authenticated(self):
    #     return True
    #
    # def is_active(self):
    #     return False
    #
    # def get_id(self):
    #     return str(self.id)
    #
    # def __repr__(self):
    #     return '<User %r>' % (self.username)
