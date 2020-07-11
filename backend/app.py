import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import setup_db, Actor, Movie
from auth import requires_auth, Auth_Error

def create_app(test_config=None):
    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type, Authorization, true')
        response.headers.add('Access-Control-Allow-Methods', '*')
        return response

    def check_movie_params(body):
        if not body['title']:
            abort(422, {'message': 'Payload has no title'})

        if not body['release']:
            abort(422, {'message': 'payload has no release date'})


    @app.route('/actors')
    @requires_auth('read:actors')
    def read_actors(payload):
        actors = Actor.query.all()
        return jsonify({
            'success': True,
            'actors': [actor.format() for actor in actors]
        }), 200

    @app.route('/actors', methods=['POST'])
    @requires_auth('create:actors')
    def create_actor(payload):
        body = request.get_json()
        try:
            actor = Actor(body)
            actor.insert()
        except KeyError as e:
            abort(422, {'message': f'Missing {e}.'})

        return jsonify({
            'success': True,
            'created': actor.id
        }), 201

    @app.route('/actors/<int:actor_id>', methods=['PATCH'])
    @requires_auth('update:actors')
    def update_actor(payload, actor_id):
        actor = Actor.query.get_or_404(actor_id)
        try:
            body = request.get_json()
            actor.update(body)
        except KeyError as e:
            abort(422, {'message': f'Missing {e}.'})

        return jsonify({
            'success': True,
            'updated': actor.id
        }), 200

    @app.route('/actors/<int:actor_id>', methods=['DELETE'])
    @requires_auth('delete:actors')
    def delete_actor(payload, actor_id):
        actor = Actor.query.get_or_404(actor_id)
        actor.delete()
        return jsonify({
            'success': True,
            'deleted': actor_id
        }), 200

    @app.route('/movies')
    @requires_auth('read:movies')
    def read_movies(payload):
        movies = Movie.query.all()
        return jsonify({
            'success': True,
            'movies': [movie.format() for movie in movies]
        }), 200

    @app.route('/movies', methods=['POST'])
    @requires_auth('create:movies')
    def create_movie(payload):
        body = request.get_json()
        try:
            movie = Movie(body)
            movie.insert()
        except KeyError as e:
            abort(422, {'message': f'Missing {e}.'})

        return jsonify({
            'success': True,
            'created': movie.id
        }), 201

    @app.route('/movies/<int:movie_id>', methods=['PATCH'])
    @requires_auth('update:movies')
    def update_movie(payload, movie_id):
        movie = Movie.query.get_or_404(movie_id)
        try:
            body = request.get_json()
            movie.update(body)
        except KeyError as e:
            abort(422, {'message': f'Missing {e}.'})

        return jsonify({
            'success': True,
            'updated': movie.id
        }), 200

    @app.route('/movies/<int:movie_id>', methods=['DELETE'])
    @requires_auth('delete:movies')
    def delete_movie(payload, movie_id):
        movie = Movie.query.get_or_404(movie_id)
        movie.delete()
        return jsonify({
            'success': True,
            'deleted': movie.id
        }), 200

    @app.errorhandler(Auth_Error)
    def auth_error(Auth_Error):
        return jsonify({
            'error': 401,
            'message': 'Authentication_Error'
        }), 401

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'error': 404,
            'message': 'Not Found'
        }), 404

    @app.errorhandler(422)
    def not_found(error):
        return jsonify({
            'error': 422,
            'message': error.description['message']
        }), 422

    return app


APP = create_app()

if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)
