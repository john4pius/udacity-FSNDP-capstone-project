import os
from sqlalchemy import Column, String, Integer, DateTime
from flask_sqlalchemy import SQLAlchemy

database_path = os.environ['DATABASE_URL']
db = SQLAlchemy()


def setup_db(app, database_path=database_path):
    app.config['SQLALCHEMY_DATABASE_URI'] = database_path
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)


actors_movies_relation = db.Table('actors_movies_relation',
                         db.Column('actor_id', db.Integer, db.ForeignKey(
                             'actor.id'), primary_key=True),
                         db.Column('movie_id', db.Integer, db.ForeignKey(
                             'movie.id'), primary_key=True)
                         )


class Movie(db.Model):
    id = Column(Integer, primary_key=True)
    title = Column(String, unique=True, nullable=False)
    release = Column(DateTime, nullable=False)
    actors = db.relationship('Actor', secondary=actors_movies_relation,
                             lazy='subquery', backref=db.backref('movies'))

    def __init__(self, attribs={}):
        self.title = attribs['title']
        self.release = attribs['release']

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self, attribs):
        self.title = attribs['title']
        self.release = attribs['release']
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'title': self.title,
            'release': self.release
        }


class Actor(db.Model):
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    age = Column(String, nullable=False)
    gender = Column(String, nullable=False)

    def __init__(self, attribs={}):
        self.name = attribs['name']
        self.age = attribs['age']
        self.gender = attribs['gender']
    
    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self, attribs):
        self.name = attribs['name']
        self.age = attribs['age']
        self.gender = attribs['gender']

        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'gender': self.gender
        }