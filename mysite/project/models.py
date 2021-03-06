from project import db
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship


class UserPost(db.Model):

    __tablename__ = 'posts'

    id          = db.Column(db.Integer, primary_key=True)
    title       = db.Column(db.String, nullable=False)
    link        = db.Column(db.String, nullable=False)
    votes       = db.Column(db.Integer)
    description = db.Column(db.String, nullable=False)
    author_id   = db.Column(db.Integer, ForeignKey('users.id'))

    def __init__(self, title, description, link, votes, author_id):
        self.title       = title
        self.description = description
        self.link        = link
        self.votes       = votes
        self.author_id   = author_id

    def __repr__(self):
        return '{}--{}'.format(self.title, self.description)

class User(db.Model):

    __tablename__ = 'users'

    id       = db.Column(db.Integer, primary_key=True)
    name     = db.Column(db.String, nullable=False)
    email    = db.Column(db.String, nullable=False)
    password = db.Column(db.String)
    posts    = relationship('UserPost', backref='author')

    def __init__(self, name, email, password):
        self.name     = name
        self.email    = email
        self.password = password

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)

    def __repr__(self):
        return '{}'.format(self.name)

class VotedUsers(db.Model):

    __tablename__ = 'voted_users'

    id = db.Column(db.Integer, primary_key=True)
    voted_post = db.Column(db.Integer)
    voted_user = db.Column(db.String)
    vote_value = db.Column(db.Integer, nullable=False)

    def __init__(self, voted_post, voted_user, vote_value):
        self.voted_post = voted_post
        self.voted_user = voted_user
        self.vote_value = vote_value







