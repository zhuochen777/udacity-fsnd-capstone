import os
from xml.dom.pulldom import ErrorHandler
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import setup_db, Movie, Actor
from auth import AuthError, requires_auth

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    # CORS(app)
    cors = CORS(app, resources={r'/api/*': {'origin': '*'}})

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization, true')
        response.headers.add('Access-Control-Allow_Methods', 'GET, PACTH, POST, DELETE, OPTIONS')
        return response

    @app.route('/', methods=['GET'])
    def index():
        return 'Hello World, Engineer!'


    @app.route('/actors', methods=['GET'])
    @requires_auth('get:actors')
    def get_actors(payload):
        try:
            actors = Actor.query.all()

            if not actors:
                abort(404)

            return jsonify({
                'success': True,
                'actors': [item.format() for item in actors]
            }), 200

        except:
            abort(422)

    @app.route('/movies', methods=['GET'])
    @requires_auth('get:movies')
    def get_movies(payload):
        try:
            movies = Movie.query.all()

            if not movies:
                abort(404)

            return jsonify({
                'success': True,
                'movies': [item.format() for item in movies]
            }), 200

        except:
            abort(422)

    @app.route('/actors/<int:actor_id>', methods=['DELETE'])
    @requires_auth('delete:actor')
    def delete_actor(payload, actor_id):
        try:
            delete_actor = Actor.query.filter(Actor.id == actor_id).one_or_none()

            if not delete_actor:
                abort(404)

            delete_actor.delete()

            actors = Actor.query.all()

            return jsonify({
                'success': True,
                'delete_actor_id': actor_id,
                'actors': [item.format() for item in actors]
            }), 200

        except:
            abort(422)

    @app.route('/movies/<int:movie_id>', methods=['DELETE'])
    @requires_auth('delete:movie')
    def delete_movie(payload, movie_id):
        try:
            delete_movie = Movie.query.filter(Movie.id == movie_id).one_or_none()

            if not delete_movie:
                abort(404)

            delete_movie.delete()

            movies = Movie.query.all()

            return jsonify({
                'success': True,
                'delete_movie_id': movie_id,
                'movies': [item.format() for item in movies]
            }), 200

        except:
            abort(422)

    @app.route('/actors', methods=['POST'])
    @requires_auth('post:actor')
    def create_actor(payload):
        try:
            body = request.get_json()

            new_name = body.get('name', None)
            new_age = body.get('age', None)
            new_gender = body.get('gender', None)

            new_actor = Actor(name=new_name, age=new_age, gender=new_gender)
            new_actor.insert()

            actors = Actor.query.all()

            return jsonify({
                'success': True,
                'actors': [item.format() for item in actors]
            }), 200

        except:
            abort(422)

    @app.route('/movies', methods=['POST'])
    @requires_auth('post:movie')
    def create_movie(payload):
        try:
            body = request.get_json()

            new_title = body.get('title', None)
            new_release_date = body.get('release_date', None)
            new_category = body.get('category', None)

            new_movie = Movie(title=new_title, release_date=new_release_date, category=new_category)
            new_movie.insert()

            movies = Movie.query.all()

            return jsonify({
                'success': True,
                'movies': [item.format() for item in movies]
            }), 200

        except:
            abort(422)

    @app.route('/actors/<int:actor_id>', methods=['PATCH'])
    @requires_auth('patch:actor')
    def update_actor(payload, actor_id):
        try:
            actor = Actor.query.filter(Actor.id == actor_id).one_or_none()

            if not actor:
                abort(404)

            body = request.get_json()

            if 'name' in body:
                new_name = body.get('name')
                actor.name = new_name

            if 'age' in body:
                new_age = body.get('age')
                actor.age = new_age

            if 'gender' in body:
                new_gender = body.get('gender')
                actor.gender = new_gender

            actor.update()

            return jsonify({
                'success': True,
                'updated_actor': [actor.format()]
            })

        except:
            abort(422)

    @app.route('/movies/<int:movie_id>', methods=['PATCH'])
    @requires_auth('patch:movie')
    def update_movie(payload, movie_id):
        try:
            movie = Movie.query.filter(Movie.id == movie_id).one_or_none()

            if not movie:
                abort(404)

            body = request.get_json()

            if 'title' in body:
                new_title = body.get('title')
                movie.title = new_title

            if 'release_date' in body:
                new_release_date = body.get('release_date')
                movie.release_date = new_release_date

            if 'category' in body:
                new_category = body.get('category')
                movie.category = new_category

            movie.update()

            return jsonify({
                'success': True,
                'updated_movie': [movie.format()]
            })

        except:
            abort(422)

    @app.errorhandler(404)
    def not_found(error):
      return jsonify({
          'error': 404,
          'success': False,
          'message': 'resource not found'
      }), 404

    @app.errorhandler(422)
    def unprocessable(error):
      return jsonify({
        'error': 422,
        'success': False,
        'message': 'unprocessable'
      }), 422

    @app.errorhandler(405)
    def not_allowed(error):
      return jsonify({
        'error': 405,
        'success': False,
        'message': 'method not allowed'
      }), 405

    @app.errorhandler(AuthError)
    def autherror(error):
        return jsonify({
            "success": False,
            "error": error.status_code,
            "message": error.error['description']
        }), error.status_code



    return app

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
