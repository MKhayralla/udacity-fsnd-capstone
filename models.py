from flask_sqlalchemy import SQLAlchemy
from config import SQLALCHEMY_DATABASE_URI

# ORM instance
db = SQLAlchemy()

# genders enum
genders = ('M', 'F')
gender_enum = db.Enum(*genders, name='gender')

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''


def setup_db(app, db_path=SQLALCHEMY_DATABASE_URI):
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    if db_path != SQLALCHEMY_DATABASE_URI:
        app.config['SQLALCHEMY_DATABASE_URI'] = db_path
    db.app = app
    db.init_app(app)
    # calling flask db upgrade would create all tables
    # db.create_all()


'''
Many to Many relationship association
'''



assignments = db.Table(
    'assignments',
    db.Column('movie_id', db.Integer, db.ForeignKey('movies.id'), primary_key=True),
    db.Column('actor_id', db.Integer, db.ForeignKey('actors.id'), primary_key=True)
)


'''
Movie

'''


class Movie(db.Model):
    '''
    an entity class for movies table in database
    Attributes:
        title : movie title : String
        release_date : movie release date : Date
    '''
    __tablename__ = 'movies'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    release_date = db.Column(db.Date)
    actors = db.relationship(
        'Actor',
        secondary=assignments,
        backref=db.backref('movies', lazy=True)
    )

    def __init__(self, title, release_date):
        self.title = title
        self.release_date = release_date

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'title': self.title,
            'release_date': self.release_date,
            'actors' : [actor.short() for actor in self.actors]
        }

    def short(self):
        '''
        returns a short format of the movie
        used for formatting movies when showing actor data
        '''
        return {
            'id': self.id,
            'title' : self.title
        }


'''
Actor

'''


class Actor(db.Model):
    __tablename__ = 'actors'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    # using age without months here
    age = db.Column(db.SMALLINT)
    gender = db.Column(gender_enum)

    def __init__(self, name, age, gender):
        self.name = name
        self.age = age
        self.gender = gender

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'gender': self.gender,
            'movies': [movie.short() for movie in self.movies]
        }

    def short(self):
        return {
            'id' : self.id,
            'name' : self.name
        }
