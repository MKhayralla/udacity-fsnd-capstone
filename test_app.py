import os
from datetime import datetime
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from api import app
from models import Actor, Movie, setup_db

# get tokens from environment variables
tokens = {
    'assistant' : os.environ.get('assistant'),
    'director' : os.environ.get('director'),
    'producer' : os.environ.get('producer')
}


class CastingAgencyTestCase(unittest.TestCase):
    """This class represents the casting agency api test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = app
        self.app.config["DEBUG"] = False
        self.client = self.app.test_client
        setup_db(self.app, test=True)
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
        # get actors with assistant credentials
        res = self.client().get(
            '/actors',
            headers={'Authorization': 'Bearer {}'.format(tokens['assistant'])}
        )
        data = json.loads(res.data)
        # success
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        # has actors in response
        self.assertTrue(data['actors'])

    def test_get_actors_with_no_authorization(self):
        '''
        No authorization header assigned
        '''
        # get actors with no credentials
        res = self.client().get('/actors')
        data = json.loads(res.data)
        # not authenticated
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'No authorization header found')

    def test_post_actor_success_by_director(self):
        '''test adding new actor by director'''
        # actor payload
        new_actor = {
            'name': 'Mohamed Henedy',
            'age': 55,
            'gender': 'M'
        }
        # post actor with director credentials
        res = self.client().post(
            '/actors',
            json=new_actor,
            headers={
                'Content-Type': 'application/json',
                'Authorization': 'Bearer {}'.format(tokens['director'])
            }
        )
        # get response
        data = json.loads(res.data)
        # success
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        # has created actor in the response
        self.assertTrue(data['created'])
        self.assertTrue(data['created_at'])

    def test_post_actor_fail_by_assistant(self):
        '''test adding new actor by assistant'''
        # new actor payload
        new_actor = {
            'name': 'Mohamed Henedy',
            'age': 55,
            'gender': 'M'
        }
        # post actor with assistant credentials
        res = self.client().post(
            '/actors',
            json=new_actor,
            headers={
                'Content-Type': 'application/json',
                'Authorization': 'Bearer {}'.format(tokens['assistant'])
            }
        )
        # grab response
        data = json.loads(res.data)
        # not authorized to do this
        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)
        self.assertEqual(
            data['message'],
            'you don\'t have enough permissions to perform this action'
        )

    def test_patch_actor_success_by_director(self):
        '''test editing existing actor by director'''
        # get some actor from database
        actor_id = Actor.query.first().id
        # request payload
        new_data = {
            'name': 'Some name',
            'age': 47
        }
        # patch actor with director credentials
        res = self.client().patch(
            '/actors/{}'.format(actor_id),
            json=new_data,
            headers={
                'Content-Type': 'application/json',
                'Authorization': 'Bearer {}'.format(tokens['director'])
            }
        )
        # grab response
        data = json.loads(res.data)
        # success
        self.assertEqual(res.status_code, 200)
        # check response fields
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actor'])
        self.assertTrue(data['modified_at'])
        # grab edited actor
        Sample = Actor.query.get(actor_id)
        # check if it is actually patched
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
        # payload
        new_data = {
            'name': 'El Sakka',
            'age': 47
        }
        # patch non-existing actor with director credentials
        res = self.client().patch(
            '/actors/404',
            json=new_data,
            headers={
                'Content-Type': 'application/json',
                'Authorization': 'Bearer {}'.format(tokens['director'])
            }
        )
        # grab response
        data = json.loads(res.data)
        # not found
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(
            'resource not found',
            data['message']
        )

    def test_delete_actor_success_by_producer(self):
        '''test deleting existing actor by producer'''
        # grab an existing id
        actor_id = Actor.query.first().id
        # delete actor with director credentials
        res = self.client().delete(
            '/actors/{}'.format(actor_id),
            headers={
                'Authorization': 'Bearer {}'.format(tokens['producer'])
            }
        )
        # grab response
        data = json.loads(res.data)
        # success
        self.assertEqual(res.status_code, 200)
        # check data
        self.assertEqual(data['success'], True)
        self.assertTrue(data['deleted_id'])
        self.assertEqual(
            actor_id,
            data['deleted_id']
        )

    def test_delete_actor_404_by_producer(self):
        '''test deleting non-existing actor by producer'''
        # delete non-existing actor with director credentials
        res = self.client().delete(
            '/actors/404',
            headers={
                'Authorization': 'Bearer {}'.format(tokens['producer'])
            }
        )
        # grab response
        data = json.loads(res.data)
        # not found
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
        # get movies with assistant credentials
        res = self.client().get(
            '/movies',
            headers={'Authorization': 'Bearer {}'.format(tokens['assistant'])}
        )
        # grab response
        data = json.loads(res.data)
        # success
        self.assertEqual(res.status_code, 200)
        # check data
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movies'])

    def test_get_movies_with_no_authorization(self):
        '''
        No authorization header assigned
        '''
        # get movies with no credentials
        res = self.client().get('/movies')
        # grab response
        data = json.loads(res.data)
        # not authenticated
        self.assertEqual(res.status_code, 401)
        # check response
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'No authorization header found')

    def test_post_movie_success_by_producer(self):
        '''test adding new movie by producer'''
        # new movie payload
        new_movie = {
            'title': 'face off',
            'release_date': '01 01 1999'
        }
        # post movie with producer credentials
        res = self.client().post(
            '/movies',
            json=new_movie,
            headers={
                'Content-Type': 'application/json',
                'Authorization': 'Bearer {}'.format(tokens['producer'])
            }
        )
        # grab response
        data = json.loads(res.data)
        # success
        self.assertEqual(res.status_code, 200)
        # check response
        self.assertEqual(data['success'], True)
        self.assertTrue(data['created'])
        self.assertTrue(data['created_at'])
        # get posted movie
        find_movie = Movie.query.filter_by(
            title='face off'
        ).one_or_none()
        # check if it does exist
        self.assertIsNotNone(find_movie)

    def test_post_movie_fail_by_director(self):
        '''test adding new movie by director'''
        # new movie payload
        new_movie = {
            'title': 'face off',
            'release_date': datetime.strptime('01 01 1999', '%d %m %Y').date()
        }
        # post movie with director credentials
        res = self.client().post(
            '/movies',
            json=new_movie,
            headers={
                'Content-Type': 'application/json',
                'Authorization': 'Bearer {}'.format(tokens['director'])
            }
        )
        # grab repsponse
        data = json.loads(res.data)
        # not authorized to perform the action
        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)
        self.assertEqual(
            data['message'],
            'you don\'t have enough permissions to perform this action'
        )

    def test_patch_movie_success_by_director(self):
        '''test editing existing movie by director'''
        # grab some valid id
        movie_id = Movie.query.first().id
        # editing payload
        new_data = {
            'release_date': '01 01 2022',
            'title': 'Mafia reloaded'
        }
        # patch movie with director credentials
        res = self.client().patch(
            '/movies/{}'.format(movie_id),
            json=new_data,
            headers={
                'Content-Type': 'application/json',
                'Authorization': 'Bearer {}'.format(tokens['director'])
            }
        )
        # grab response
        data = json.loads(res.data)
        # success
        self.assertEqual(res.status_code, 200)
        # check response
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movie'])
        self.assertTrue(data['modified_at'])
        # grab the edited movie from database
        Mafia = Movie.query.get(movie_id)
        # check edited title
        self.assertEqual(
            'Mafia reloaded',
            Mafia.title
        )

    def test_patch_movie_404_by_producer(self):
        '''test editing non-existing movie by producer'''
        # editing payload
        new_data = {
            'release_date': '01 01 2022',
            'title': 'Mafia reloaded'
        }
        # patch non-existing movie with producer credentials
        res = self.client().patch(
            '/movies/404',
            json=new_data,
            headers={
                'Content-Type': 'application/json',
                'Authorization': 'Bearer {}'.format(tokens['producer'])
            }
        )
        # grab response
        data = json.loads(res.data)
        # not found 
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(
            'resource not found',
            data['message']
        )

    def test_delete_movie_success_by_producer(self):
        '''test deleting existing movie by producer'''
        # grab valid id
        movie_id = Movie.query.first().id
        # delete movie with producer credentials
        res = self.client().delete(
            '/movies/{}'.format(movie_id),
            headers={
                'Authorization': 'Bearer {}'.format(tokens['producer'])
            }
        )
        # grab response
        data = json.loads(res.data)
        # success
        self.assertEqual(res.status_code, 200)
        # check response
        self.assertEqual(data['success'], True)
        self.assertTrue(data['deleted_id'])
        self.assertEqual(
            movie_id,
            data['deleted_id']
        )

    def test_delete_movie_403_by_director(self):
        '''test deleting existing movie failed by director'''
        # grab existing id
        movie_id = Movie.query.first().id
        # delete movie with director credentials
        res = self.client().delete(
            '/movies/{}'.format(movie_id),
            headers={
                'Authorization': 'Bearer {}'.format(tokens['director'])
            }
        )
        # grab response
        data = json.loads(res.data)
        # not authorized to perform the action
        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)
        self.assertEqual(
            'you don\'t have enough permissions to perform this action',
            data['message']
        )


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
