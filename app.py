from flask import Flask
from flask_migrate import Migrate
from models import *

# define our app
app = Flask(__name__)
# config the app
app.config.from_object('config')
# config database
setup_db(app)
# allow migration management using flask_migrate
migrate = Migrate(app, db)

if __name__ == '__main__':
    app.run(port=8080)
    