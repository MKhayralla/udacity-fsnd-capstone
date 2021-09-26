import logging
from flask import Flask, request
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
@app.route('/movies', methods = ['GET', 'POST'])
def FunctionName():
    http_method = request.method
    if http_method == 'GET':
        movies = Movie.query.all()
        res = {
            movie.id:movie.format() for movie in movies
        }
        return jsonify(
            {
                'success' : True,
                'status' : 200,
                'movies' : res
            }
        )


if __name__ == '__main__':
    app.run(port=8080)
