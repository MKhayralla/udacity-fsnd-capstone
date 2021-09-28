# import modules
from datetime import datetime
from pprint import pprint
import logging
from flask import Flask, request, abort
from flask.json import jsonify
from flask_migrate import Migrate
from flask_cors import CORS
from models import setup_db, db, Actor, Movie
from auth import AuthError, requires_auth


# define our app
app = Flask(__name__)
# config the app
app.config.from_object('config')
app.logger.setLevel(logging.INFO)
#allow cors
cors = CORS(app)
# allow migration management using flask_migrate
migrate = Migrate(app, db)
# config database
setup_db(app)


'''
Movies end points
'''

@requires_auth('view:movies')
@app.route('/movies', methods=['GET'])
@requires_auth('view:movies')
def get_movies(current_user):
    '''
    returns all movies
    accessible by anyone
    '''
    # get all movies
    movies = Movie.query.all()
    # format output into an object
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
def add_movie(current_user):
    '''
    posts new movie
    '''
    data = request.json
    try:
        # read date from input
        data['release_date'] = datetime.strptime(data['release_date'], '%m %d %Y')
        # instantiate a movie from inputs
        movie = Movie(**data)
        # insert it into the database
        movie.insert()
        return jsonify(
            {
                'success': True,
                'status': 200,
                'created': movie.format(),
                'created_at': datetime.now()
            }
        )
    except Exception as e:
        abort(422)


@app.route('/movies/<int:movie_id>', methods=['PATCH'])
@requires_auth('patch:movies')
def edit_movie(current_user, movie_id):
    '''
    edits an existing movie
    '''
    data = request.json
    # find the required movie oe return 404
    movie = Movie.query.get_or_404(movie_id)
    # edit the data
    try:
        if 'title' in data:
            movie.title = data['title']
        if 'release_date' in data:
            movie.release_date = datetime.strptime(
                data['release_date'],
                '%m %d %Y'
            )
        # save changes
        movie.update()
        return jsonify(
            {
                'success': True,
                'status': 200,
                'movie': movie.format(),
                'modified_at': datetime.now()
            }
        )
    except Exception as e:
        abort(422)


@app.route('/movies/<int:movie_id>', methods=['DELETE'])
@requires_auth('delete:movies')
def delete_movie(current_user, movie_id):
    '''
    deletes an existing movie movie
    '''
    # get the required movie or 404 
    movie = Movie.query.get_or_404(movie_id)
    try:
        # delete the movie from the database
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
def get_actors(current_user):
    '''
    returns all actors
    accessible by anyone
    '''
    # get all actors
    actors = Actor.query.all()
    # format output
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
def add_actor(current_user):
    '''
    posts new Actor
    '''
    data = request.json
    try:
        # instantiate an actor
        actor = Actor(**data)
        # add it to the database
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
def edit_actor(current_user, actor_id):
    '''
    edits an existing actor
    '''
    data = request.json
    # find the required actor or 404
    actor = Actor.query.get_or_404(actor_id)
    # try editing data
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
def delete_actor(current_user, actor_id):
    '''
    deletes an existing actor
    '''
    # find the required actor or 404
    actor = Actor.query.get_or_404(actor_id)
    try:
        # delete it from the database
        actor.delete()
        return jsonify(
            {
                'success': True,
                'status': 200,
                'deleted_id': actor_id,
                'deleted_at': datetime.now()
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

# Method not allowed Error
@app.errorhandler(405)
def server_error(error):
    return jsonify({
        "success": False,
        "error": 405,
        "message": "Method Not Allowed!"
    }), 405

# unprocessible entity


@app.errorhandler(422)
def unprocessible_error(error):
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
def bad_request_error(error):
    return jsonify({
        "success": False,
        "error": 400,
        "message": "bad request"
    }), 400


if __name__ == '__main__':
    app.run()
