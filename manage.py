from flask_script import Manager
from sqlalchemy import Column, String, Integer, create_engine
from flask_migrate import Migrate, MigrateCommand

from app import app
from models import db, Movie, Actor

migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)


# custom seed command
@manager.command
def seed():
    Movie(title='San Andreas', release_date='2015-08-01').insert()
    Movie(title='Black Swan', release_date='2010-05-01').insert()
    Movie(title='Maleficient', release_date='2014-12-01').insert()

    Actor(name='Dwayne Johnson', age=52, gender='male').insert()
    Actor(name='Natalie Portman', age=36, gender='female').insert()
    Actor(name='Angelina Jolie', age=46, gender='female').insert()

if __name__ == '__main__':
    manager.run()