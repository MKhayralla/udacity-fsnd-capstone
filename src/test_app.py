from datetime import datetime
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from api import app
from models import Actor, Movie, setup_db

# get tokens
f = open('tokens.json', 'r')
tokens = json.load(f)
f.close()


class CastingAgencyTestCase(unittest.TestCase):
    """This class represents the casting agency api test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.database_path = 'postgresql://postgres:password@localhost:5432/casting_test'
        self.app = app
        self.app.config["DEBUG"] = False
        self.client = self.app.test_client
        setup_db(self.app, self.database_path)
        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
            

    def tearDown(self):
        """Executed after each test"""
        pass

    """
    Actor Endpoints
    """
    def test_get_actors_correctly(self):
        '''test the successful actors result'''
        res = self.client().get(
            '/actors',
            headers= {'Authorization' : 'Bearer {}'.format(tokens['assistant'])}
            ) 
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actors'])

    def test_get_actors_with_no_authorization(self):
        '''
        No authorization header assigned
        '''
        res = self.client().get('/actors')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'No authorization header found')

    
    def test_post_actor_success_by_director(self):
        '''test adding new actor by director'''
        new_actor = {
            'name' : 'Mohamed Henedy',
            'age' : 55,
            'gender' : 'M'
        }
        res = self.client().post(
            '/actors',
            json = new_actor,
            headers = {
                'Content-Type' : 'application/json',
                'Authorization' : 'Bearer {}'.format(tokens['director'])
            }
            )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['created'])
        self.assertTrue(data['created_at'])
        
    def test_post_actor_fail_by_assistant(self):
        '''test adding new actor by assistant'''
        new_actor = {
            'name' : 'Mohamed Henedy',
            'age' : 55,
            'gender' : 'M'
        }
        res = self.client().post(
            '/actors',
            json = new_actor,
            headers = {
                'Content-Type' : 'application/json',
                'Authorization' : 'Bearer {}'.format(tokens['assistant'])
            }
            )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)
        self.assertEqual(
            data['message'],
            'you don\'t have enough permissions to perform this action'
            )

    def test_patch_actor_success_by_director(self):
        '''test editing existing actor by director'''
        actor_id = Actor.query.first().id
        new_data = {
            'name' : 'Some name',
            'age' : 47
        }
        res = self.client().patch(
            '/actors/{}'.format(actor_id),
            json = new_data,
            headers = {
                'Content-Type' : 'application/json',
                'Authorization' : 'Bearer {}'.format(tokens['director'])
            }
            )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actor'])
        self.assertTrue(data['modified_at'])
        Sample = Actor.query.get(actor_id)
        self.assertEqual(
            'Some name',
            Sample.name
        )
        self.assertEqual(
            47,
            Sample.age
        )

    def test_patch_actor_404_by_director(self):
        '''test editing non-existing actor by director'''
        new_data = {
            'name' : 'El Sakka',
            'age' : 47
        }
        res = self.client().patch(
            '/actors/404',
            json = new_data,
            headers = {
                'Content-Type' : 'application/json',
                'Authorization' : 'Bearer {}'.format(tokens['director'])
            }
            )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(
            'resource not found',
            data['message']
        )
    
    def test_delete_actor_success_by_producer(self):
        '''test deleting existing actor by producer'''
        actor_id = Actor.query.first().id
        res = self.client().delete(
            '/actors/{}'.format(actor_id),
            headers = {
                'Authorization' : 'Bearer {}'.format(tokens['producer'])
            }
            )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['deleted_id'])
        self.assertEqual(
            actor_id,
            data['deleted_id']
            )
    
    def test_delete_actor_404_by_producer(self):
        '''test deleting non-existing actor by producer'''
        res = self.client().delete(
            '/actors/404',
            headers = {
                'Authorization' : 'Bearer {}'.format(tokens['producer'])
            }
            )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(
            'resource not found',
            data['message']
            )
    
    """
    Movie Endpoints
    """
    def test_get_movies_correctly(self):
        '''test the successful movies result'''
        res = self.client().get(
            '/movies',
            headers= {'Authorization' : 'Bearer {}'.format(tokens['assistant'])}
            ) 
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movies'])

    def test_get_movies_with_no_authorization(self):
        '''
        No authorization header assigned
        '''
        res = self.client().get('/movies')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'No authorization header found')

    
    def test_post_movie_success_by_producer(self):
        '''test adding new movie by producer'''
        new_movie = {
            'title' : 'face off',
            'release_date' : datetime.strptime('01 01 1999', '%d %m %Y').date()
        }
        res = self.client().post(
            '/movies',
            json = new_movie,
            headers = {
                'Content-Type' : 'application/json',
                'Authorization' : 'Bearer {}'.format(tokens['producer'])
            }
            )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['created'])
        self.assertTrue(data['created_at'])
        find_movie = Movie.query.filter_by(
            title = 'face off'
            ).one_or_none()
        self.assertIsNotNone(find_movie)
        
    def test_post_movie_fail_by_director(self):
        '''test adding new movie by director'''
        new_movie = {
            'title' : 'face off',
            'release_date' : datetime.strptime('01 01 1999', '%d %m %Y').date()
        }
        res = self.client().post(
            '/movies',
            json = new_movie,
            headers = {
                'Content-Type' : 'application/json',
                'Authorization' : 'Bearer {}'.format(tokens['director'])
            }
            )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)
        self.assertEqual(
            data['message'],
            'you don\'t have enough permissions to perform this action'
            )

    def test_patch_movie_success_by_director(self):
        '''test editing existing movie by director'''
        movie_id = Movie.query.first().id
        new_data = {
            'release_date' : datetime.strptime(
                '01 01 2022', '%d %m %Y'
            ),
            'title' : 'Mafia reloaded'
        }
        res = self.client().patch(
            '/movies/{}'.format(movie_id),
            json = new_data,
            headers = {
                'Content-Type' : 'application/json',
                'Authorization' : 'Bearer {}'.format(tokens['director'])
            }
            )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movie'])
        self.assertTrue(data['modified_at'])
        Mafia = Movie.query.get(movie_id)
        self.assertEqual(
            'Mafia reloaded',
            Mafia.title
        )

    def test_patch_movie_404_by_producer(self):
        '''test editing non-existing movie by producer'''
        new_data = {
            'release_date' : datetime.strptime(
                '01 01 2022', '%d %m %Y'
            ),
            'title' : 'Mafia reloaded'
        }
        res = self.client().patch(
            '/movies/404',
            json = new_data,
            headers = {
                'Content-Type' : 'application/json',
                'Authorization' : 'Bearer {}'.format(tokens['producer'])
            }
            )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(
            'resource not found',
            data['message']
        )
    
    def test_delete_movie_success_by_producer(self):
        '''test deleting existing movie by producer'''
        movie_id = Movie.query.first().id
        res = self.client().delete(
            '/movies/{}'.format(movie_id),
            headers = {
                'Authorization' : 'Bearer {}'.format(tokens['producer'])
            }
            )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['deleted_id'])
        self.assertEqual(
            movie_id,
            data['deleted_id']
            )
    
    def test_delete_movie_403_by_director(self):
        '''test deleting existing movie failed by director'''
        movie_id = Movie.query.first().id
        res = self.client().delete(
            '/movies/{}'.format(movie_id),
            headers = {
                'Authorization' : 'Bearer {}'.format(tokens['director'])
            }
            )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)
        self.assertEqual(
            'you don\'t have enough permissions to perform this action',
            data['message']
            )

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
