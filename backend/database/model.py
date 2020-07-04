import os
from sqlalchemy import Column, String, Integer, create_engine
from flask_sqlalchemy import SQLAlchemy
import json

database_path = os.environ['DATABASE_URL']
db = SQLAlchemy()


def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()


def db_drop_and_create_all():
    db.drop_all()
    db.create_all()

class Site(db.Model):
    site_id = Column(Integer, primary_key=True)
    site_name = Column(String)
    town = Column(String)

    def __init__(self, title, release_date):
        self.site_name = site_name
        self.town = town

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def format(self):
        return {
            'site_id': self.site_id,
            'site_name': self.site_name,
            'town': self.town
        }

class Inventory(db.Model):
    site_id = Column(Integer, primary_key=True)
    site_name = Column(String)
    technology = Column(String)
    count_radio = Column(String)

    def __init__(self, site_name, technology, gender):
        self.name = site_name
        self.technology = technology
        self.count_radio = count_radio

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def format(self):
        return {
            'site_id': self.site_id,
            'count_radio': self.count_radio,
            'technology': self.technology,
            'count_radio': self.count_radio
        }
        