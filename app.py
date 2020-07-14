import os
from flask_cors import CORS
from flask import Flask, jsonify, abort, request
from models import setup_db, db, Movie, Actor
from auth import AuthError, requires_auth
from sqlalchemy import exc
from utils import *


def create_app(test_config=None):

    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    @app.route('/')
    def welcome():
        return 'Welcome to Movies Inventory!'

    @app.route('/movies')
    @requires_auth('get:movies')
    def get_movies(jwt):
        try:
            movies = Movie.query.all()
            return jsonify({
                'success': True,
                'movies': [movie.format() for movie in movies],
            }), 200
        
        except Exception:
            abort(404)

    @app.route('/movies/<int:id>')
    @requires_auth('get:movies')
    def get_movie_by_id(jwt, id):
        try:
            movie = Movie.query.get(id)

            if movie is None:
                abort(404)
            else:
                return jsonify({
                    'success': True,
                    'movie': movie.format(),
                }), 200
        
        except Exception:
            abort(404)        

    @app.route('/movies', methods=['POST'])
    @requires_auth('post:movies')
    def post_movie(jwt):
        data = request.get_json()
        title = data.get('title', '')
        date = data.get('release_date', '')

        movie = Movie(title=title, release_date=date)
        if validate_movie(movie) is False:
            abort(400)
        try:
            movie.insert()
            return jsonify({
                'success': True,
                'message': 'Movie added',
                'movie': movie.format()
            }), 201
        except:
            abort(500)

    @app.route('/movies/<int:id>', methods=['PATCH'])
    @requires_auth('patch:movies')
    def edit_movie(jwt, id):
        data = request.get_json()
        title = data.get('title', '')
        date = data.get('release_date', '')

        movie = Movie.query.get(id)

        if movie is None:
            abort(404)

        movie.title = title
        movie.release_date = date
        if validate_movie(movie) is False:
            db.session.rollback()
            abort(400)
        try:
            movie.update()
            return jsonify({
                'success': True,
                'message': 'Movie updated',
                'movie': movie.format()
            }), 200
        except:
            db.session.rollback()
            abort(500)

    @app.route('/movies/<int:id>', methods=['DELETE'])
    @requires_auth('delete:movies')
    def delete_movie(jwt, id):
        movie = Movie.query.get(id)

        if movie is None:
            abort(404)
        try:
            movie.delete()
            return jsonify({
                'success': True,
                'message': 'Movie deleted',
                'movie': movie.id
            })
        except:
            db.session.rollback()
            abort(500)

    '''
    ACTORS ENDPOINTS
    '''
    @app.route('/actors')
    @requires_auth('get:actors')
    def get_actors(jwt):
        actors = Actor.query.all()
        return jsonify({
            'success': True,
            'actors': [actor.format() for actor in actors],
        }), 200

    @app.route('/actors/<int:id>')
    @requires_auth('get:movies')
    def get_actor_by_id(jwt, id):
        actor = Actor.query.get(id)

        if actor is None:
            abort(404)
        else:
            return jsonify({
                'success': True,
                'actor': actor.format(),
            }), 200

    @app.route('/actors', methods=['POST'])
    @requires_auth('post:actors')
    def post_actor(jwt):
        data = request.get_json()
        name = data.get('name', '')
        age = data.get('age', '')
        gender = data.get('gender', '')

        actor = Actor(name=name, age=age, gender=gender)
        if validate_actor(actor) is False:
            abort(400)
        try:
            actor.insert()
            return jsonify({
                'success': True,
                'message': 'Actor added',
                'actor': actor.format()
            }), 201
        except:
            abort(500)

    @app.route('/actors/<int:id>', methods=['PATCH'])
    @requires_auth('patch:actors')
    def edit_actor(jwt, id):
        data = request.get_json()
        name = data.get('name', '')
        age = data.get('age', '')
        gender = data.get('gender', '')

        actor = Actor.query.get(id)

        if actor is None:
            abort(404)

        actor.name = name
        actor.age = age
        actor.gender = gender
        if validate_actor(actor) is False:
            db.session.rollback()
            abort(400)
        try:
            actor.update()
            return jsonify({
                'success': True,
                'message': 'Actor updated',
                'actor': actor.format()
            }), 200
        except:
            db.session.rollback()
            abort(500)

    @app.route('/actors/<int:id>', methods=['DELETE'])
    @requires_auth('delete:actors')
    def delete_actor(jwt, id):
        actor = Actor.query.get(id)

        if actor is None:
            abort(404)
        try:
            actor.delete()
            return jsonify({
                'success': True,
                'message': 'Actor deleted',
                'actor': actor.id
            })
        except:
            db.session.rollback()
            abort(500)

    '''
    Create error handlers for all expected errors
    '''
    ''' handle bad request '''
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "message": "Bad Request, pls check your inputs"
        }), 400

    '''  handle unauthorized request errors '''
    @app.errorhandler(401)
    def unathorized(error):
        return jsonify({
            "success": False,
            "error": 401,
            "message": error.description,
        }), 401
        
    
    @app.errorhandler(AuthError)
    def handle_auth_error(ex):
        return jsonify({
            "success": False,
            "error": ex.status_code,
            'message': ex.error
        }), 401
        

    ''' handle forbidden requests '''
    @app.errorhandler(403)
    def forbidden(error):
        return jsonify({
            "success": False,
            "error": 403,
            "message": "You are forbidden from accessing this resource",
        }), 403

    ''' # handle resource not found errors '''
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "message": "Resource not found"
        }), 404
        
    
    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
            }), 422

    ''' handle bad request '''
    @app.errorhandler(500)
    def bad_request(error):
        return jsonify({
            "success": False,
            "message": "Something went wrong, please try again"
        }), 500

    return app

app = create_app()

if __name__ == '__main__':
    app.run()