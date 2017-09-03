from . import db
from .base import Base

class Post(Base):

    __tablename__ = 'posts'

    id = db.Column('post_id', db.Integer, primary_key=True)
    title = db.Column(db.String(60))
    text = db.Column(db.Text)

    #user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __init__(self, title, text):
        self.title = title
        self.text = text
