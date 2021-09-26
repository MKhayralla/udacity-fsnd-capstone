from datetime import datetime
import logging
from flask import Flask, request, abort
from flask.json import jsonify
from flask_migrate import Migrate
from models import setup_db, db, Actor, Movie
from auth import AuthError, requires_auth


# define our app
app = Flask(__name__)
# config the app
app.config.from_object('config')
app.logger.setLevel(logging.INFO)
# config database
setup_db(app)
# allow migration management using flask_migrate
migrate = Migrate(app, db)


'''
Movies end points
'''

@requires_auth('view:movies')
@app.route('/movies', methods=['GET'])
@requires_auth('view:movies')
def get_movies():
    '''
    returns all movies
    accessible by anyone
    '''
    movies = Movie.query.all()
    res = {
        movie.id: movie.format() for movie in movies
    }
    return jsonify(
        {
            'success': True,
            'status': 200,
            'movies': res
        }
    )


@app.route('/movies', methods=['POST'])
@requires_auth('add:movies')
def add_movie():
    '''
    posts new movie
    '''
    data = request.json
    try:
        movie = Movie(**data)
        movie.insert()
        return jsonify(
            {
                'success': True,
                'status': 200,
                'created': movie.format(),
                'created_at': datetime.now()
            }
        )
    except:
        abort(422)


@app.route('/movies/<int:movie_id>', methods=['PATCH'])
@requires_auth('patch:movies')
def edit_movie(movie_id):
    '''
    edits an existing movie
    '''
    data = request.json
    movie = Movie.query.get_or_404(movie_id)
    try:
        if 'title' in data:
            movie.title = data['title']
        if 'release_date' in data:
            movie.release_date = data['release_date']
        movie.update()
        return jsonify(
            {
                'success': True,
                'status': 200,
                'movie': movie.format(),
                'modified_at': datetime.now()
            }
        )
    except:
        abort(422)


@app.route('/movies/<int:movie_id>', methods=['DELETE'])
@requires_auth('delete:movies')
def delete_movie(movie_id):
    '''
    deletes an existing movie movie
    '''
    movie = Movie.query.get_or_404(movie_id)
    try:
        movie.delete()
        return jsonify(
            {
                'success': True,
                'status': 200,
                'deleted_id': movie_id,
                'deleted_at': datetime.now()
            }
        )
    except:
        abort(422)


'''
Actors end points
'''

@app.route('/actors', methods=['GET'])
@requires_auth('view:actors')
def get_actors():
    '''
    returns all actors
    accessible by anyone
    '''
    actors = Actor.query.all()
    res = {
        actor.id: actor.format() for actor in actors
    }
    return jsonify(
        {
            'success': True,
            'status': 200,
            'actors': res
        }
    )


@app.route('/actors', methods=['POST'])
@requires_auth('add:actors')
def add_actor():
    '''
    posts new Actor
    '''
    data = request.json
    try:
        actor = Actor(**data)
        actor.insert()
        return jsonify(
            {
                'success': True,
                'status': 200,
                'created': actor.format(),
                'created_at': datetime.now()
            }
        )
    except:
        abort(422)


@app.route('/actors/<int:actor_id>', methods=['PATCH'])
@requires_auth('patch:actors')
def edit_actor(actor_id):
    '''
    edits an existing actor
    '''
    data = request.json
    actor = Actor.query.get_or_404(actor_id)
    try:
        if 'name' in data:
            actor.name = data['name']
        if 'age' in data:
            actor.age = (int)(data['age'])
        if 'gender' in data:
            actor.gender = data['gender']
        actor.update()
        return jsonify(
            {
                'success': True,
                'status': 200,
                'actor': actor.format(),
                'modified_at': datetime.now()
            }
        )
    except:
        abort(422)


@app.route('/actors/<int:actor_id>', methods=['DELETE'])
@requires_auth('delete:actors')
def delete_actor(actor_id):
    '''
    deletes an existing actor
    '''
    actor = Actor.query.get_or_404(actor_id)
    try:
        actor.delete()
        return jsonify(
            {
                'success': True,
                'status': 200,
                'deleted_id': actor_id,
                'modified_at': datetime.now()
            }
        )
    except:
        abort(422)


'''
Error Handlers
'''


# server Error
@app.errorhandler(500)
def server_error(error):
    return jsonify({
        "success": False,
        "error": 500,
        "message": "internal server error"
    }), 500

# unprocessible entity


@app.errorhandler(422)
def server_error(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "unprocessible entity"
    }), 422


'''
Authentication and Authorization errors
'''


@app.errorhandler(AuthError)
def authentication_error(error):
    return jsonify({
        "success": False,
        "error": error.status_code,
        "message": error.message
    }), error.status_code



# Not Found
@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "success": False,
        "error": 404,
        "message": "resource not found"
    }), 404

# Bad Request
@app.errorhandler(400)
def server_error(error):
    return jsonify({
        "success": False,
        "error": 400,
        "message": "bad request"
    }), 400


if __name__ == '__main__':
    app.run()
