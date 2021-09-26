from datetime import datetime
import logging
from flask import Flask, request, abort
from flask.json import jsonify
from flask_migrate import Migrate
from models import setup_db, db, Actor, Movie


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

@app.route('/movies', methods=['GET'])
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
                'status': 201,
                'created': movie.format(),
                'created_at': datetime.now()
            }
        )
    except:
        abort(422)





if __name__ == '__main__':
    app.run()
