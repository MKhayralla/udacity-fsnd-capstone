from sqlalchemy import Column, String, Integer, Date, SMALLINT, Enum
from flask_sqlalchemy import SQLAlchemy
from config import SQLALCHEMY_DATABASE_URI

# ORM instance
db = SQLAlchemy()

# genders enum
genders = ('M', 'F')
gender_enum = Enum(*genders, name='gender')

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
    db.create_all()


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

    id = Column(Integer, primary_key=True)
    title = Column(String)
    release_date = Column(Date)

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
            'release_date': self.release_date
        }
        


'''
Actor

'''


class Actor(db.Model):
    __tablename__ = 'actors'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    # using age without months here
    age = Column(SMALLINT)
    gender = Column(gender_enum)

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
            'age' : self.age,
            'gender' : self.gender
        }
