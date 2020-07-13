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
    Movie(title='Black Panther', release_date='2018-12-12').insert()
    Movie(title='Hangover', release_date='2009-12-12').insert()
    Movie(title='Superbad', release_date='2006-12-12').insert()

    Actor(name='Pierce Brosnan', age=66, gender='male').insert()
    Actor(name='Tyler Perry', age=50, gender='male').insert()
    Actor(name='Jonah Hill', age=32, gender='male').insert()

if __name__ == '__main__':
    manager.run()