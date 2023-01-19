import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, Movie, Actor

casting_assistant_token = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlMwN3JYLTlHa1ZlaFl1U1FFSi1qXyJ9.eyJpc3MiOiJodHRwczovL2Rldi1iemhqMHd3dW40MnJjZDgyLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2M2MwYjhjNTJmYmQ3NTE1ZDNmYjkxZGUiLCJhdWQiOiJhZ2VuY3kiLCJpYXQiOjE2NzQxNjY3NTAsImV4cCI6MTY3NDI1MzE1MCwiYXpwIjoiRkZPTXZ3SnVMZFRGc2xaQUN1YnY4Y0NXQXp6ZlMzMlciLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIl19.1jZR9pBLgzFUvpvU5XOGHV8VhliKO4fLMGXHgqxhx-kxFzDH5rHtBaGAuzbVAdfitjrtrgXGvdYpvNskekna4a36yQ-Jq0HloPlufR75Ugo9cZx9QVFMYREEoFL6Jm1Pj-jZ_i5ZiRZnz6huFlZE7OeysAywQjRZywZDhUFVdS-iN72_jFjI5fYVf3zPMmZNoGlyUBoQa4MZBvMjEb1N3S7oxBzuxJYUgKwldaNvef3x5P1mePI_x9AsHClBD_aDxmg1dBTwDbgn9HbO3lT4AXSSn3sXmFDdlGmTcus3ecsSsJMjSxoOa37GwNwnMiVebC5pPuNy3cI3S9j92yftlA'
casting_director_token = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlMwN3JYLTlHa1ZlaFl1U1FFSi1qXyJ9.eyJpc3MiOiJodHRwczovL2Rldi1iemhqMHd3dW40MnJjZDgyLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2M2MwYjk2YTM1ZjhlMjNhZDdlMGEyNzAiLCJhdWQiOiJhZ2VuY3kiLCJpYXQiOjE2NzQxNjY4MTMsImV4cCI6MTY3NDI1MzIxMywiYXpwIjoiRkZPTXZ3SnVMZFRGc2xaQUN1YnY4Y0NXQXp6ZlMzMlciLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvciIsImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIiwicGF0Y2g6YWN0b3IiLCJwYXRjaDptb3ZpZSIsInBvc3Q6YWN0b3IiXX0.VO8PIUR3v3e4Vq7zDvYYc6AZ_M8XiXl9Flb5KyW9UsvRiBxaRUOpTbx1XAAPZcNhSZ60ZPbVwUIUaQxs55JKfjfWMK3q7X92Mxks-qeerUYsaHnE-ulUbbim5xZibZh_h46C75r-_pG33u4q4ZaDwHFmDR5YJERXSV3M0MQyx_ok4FC-IYP1ib86xFru6FVTevsw-QTMXHWnxjzOCup_C4EwI-JUOQSaEa8SbKM3gaOSP5MHzXcLeGBl9rJegVpelLDPscbTcwAB_IE5NnlchQhy7py-0-q3muyvk2D-7H3dEmJzrQzY7OqzI4_LOrnFoRzvzeyBqrIrye1XfkWq3g'
casting_producer_token = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlMwN3JYLTlHa1ZlaFl1U1FFSi1qXyJ9.eyJpc3MiOiJodHRwczovL2Rldi1iemhqMHd3dW40MnJjZDgyLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2M2MwYjliYTU0YzU2MWQzM2NlNzZhY2IiLCJhdWQiOiJhZ2VuY3kiLCJpYXQiOjE2NzQxMDM5OTUsImV4cCI6MTY3NDE5MDM5NSwiYXpwIjoiRkZPTXZ3SnVMZFRGc2xaQUN1YnY4Y0NXQXp6ZlMzMlciLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvciIsImRlbGV0ZTptb3ZpZSIsImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIiwicGF0Y2g6YWN0b3IiLCJwYXRjaDptb3ZpZSIsInBvc3Q6YWN0b3IiLCJwb3N0Om1vdmllIl19.rBnF0lOhf-XXLW0A8n1jeuAgWYTvcgQJVq3M8yJ0R5pmHumBOqYI8HsWE2GW-25yiZzWAhdBnvgO8aZROwyuZ4Rv6lfpgL9CjPTUsJlgdwdTYWuDTFx9to-tEvobBPNic1ZJEAgA9cTSt4ykJpSIEiJIo2fGVbDz7RNn4cUXaOsTdJtUW6F1M50Tss6TmstqXSZzG9GNR1fGqfR0uiTr57DukyTzpWf7m34r4UQfNBbDc3OQj7s7Z75nnzQK7GorHXEtn-ce3u-k_9y2eFGOjZPj1csBokyVW3Pr7S77dcxRshg-1ykI10Iv1YIqthm8cQ086pCACiGlQ_nLa5sfHg'


class AgencyTestCase(unittest.TestCase):
    """This class represents the agency test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.DB_HOST = os.getenv('DB_HOST', '127.0.0.1:5432')
        self.DB_USER = os.getenv('DB_USER', 'zhuochen')
        self.DB_NAME = os.getenv('DB_NAME', 'agency')
        self.database_path = "postgresql://{}@{}/{}".format(self.DB_USER, self.DB_HOST, self.DB_NAME)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass


    # GET /actors -- success behavior
    # RBAC for Casting Assistant role -- method allowed
    def test_get_actors(self):
        res = self.client().get('/actors', headers = {'Authorization': 'Bearer ' + casting_assistant_token})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['actors']))

    # GET /actors -- error behavior
    # Invalid token -- method not allowed
    def test_invalid_token_get_actors(self):
        res = self.client().get('/actors', headers = {'Authorization': 'Bearer ' + 'invalidtoken'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Invalid token.')

    # GET /movies -- success behavior
    # RBAC for Casting Assistant role -- method allowed
    def test_get_movies(self):
        res = self.client().get('/movies', headers = {'Authorization': 'Bearer ' + casting_assistant_token})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['movies']))

    # GET /movies -- error behavior
    # Invalid token -- method not allowed
    def test_invalid_token_get_movies(self):
        res = self.client().get('/movies', headers = {'Authorization': 'Bearer ' + 'invalidtoken'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Invalid token.')

    # POST /actors -- success behavior
    # RBAC for Casting Director role -- method allowed
    def test_create_actor(self):
        res = self.client().post('/actors', json={'name': 'Tom Cruise', 'age': 60, 'gender': 'male'}, headers = {'Authorization': 'Bearer ' + casting_director_token})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actors'])

    # POST /actors -- error behavior
    # RBAC for Casting Assistant role -- method not allowed
    def test_not_auth_create_actor(self):
        res = self.client().post('/actors', json={'name': 'Michelle Yeoh', 'age': 60, 'gender': 'female'}, headers = {'Authorization': 'Bearer ' + casting_assistant_token})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Permission not found')

    # # POST /actors -- error behavior, invalid route
    # # RBAC for Casting Director role -- method allowed
    def test_create_existing_actor(self):
        res = self.client().post('/actors/2', json={'name': 'Johnny Depp', 'age': 59, 'gender': 'male'}, headers = {'Authorization': 'Bearer ' + casting_director_token})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'method not allowed')

    # POST /movies -- success behavior
    # RBAC for Casting Producer role -- method allowed
    def test_create_movie(self):
        res = self.client().post('/movies', json={'title': 'Pirates of the Caribbean', 'release_date': '12022003', 'category': 'adventure'}, headers = {'Authorization': 'Bearer ' + casting_producer_token})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movies'])

    # POST /movies -- error behavior
    # RBAC for Casting Assistant role -- method not allowed
    def test_not_auth_create_movie(self):
        res = self.client().post('/movies', json={'title': 'Inception', 'release_date': '07162010', 'category': 'action'}, headers = {'Authorization': 'Bearer ' + casting_assistant_token})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Permission not found')

    # POST /movies -- error behavior, invalid route
    # RBAC for Casting Director role -- method allowed
    def test_create_existing_movie(self):
        res = self.client().post('/movies/2', json={'title': 'Inception', 'release_date': '07162010', 'category': 'action'}, headers = {'Authorization': 'Bearer ' + casting_director_token})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'method not allowed')

    # PATCH /actors -- success behavior
    # RBAC for Casting Director role -- method allowed
    def test_modify_actor(self):
        res = self.client().patch('/actors/3', json={'age': 61}, headers = {'Authorization': 'Bearer ' + casting_director_token})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['updated_actor'])

    # PATCH /actors -- error behavior, invalid route
    # RBAC for Casting Director role -- method allowed
    def test_invalid_route_modify_actor(self):
        res = self.client().patch('/actors', json={'age': 61}, headers = {'Authorization': 'Bearer ' + casting_director_token})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'method not allowed')

    # PATCH /movies -- success behavior
    # RBAC for Casting Producer role -- method allowed
    def test_modify_movie(self):
        res = self.client().patch('/movies/1', json={'title': 'Superman'}, headers = {'Authorization': 'Bearer ' + casting_producer_token})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['updated_movie'])

    # PATCH /movies -- error behavior
    # RBAC for Casting Assistant role -- method not allowed
    def test_not_auth_modify_movie(self):
        res = self.client().patch('/movies/1', json={'title': 'Superman'}, headers = {'Authorization': 'Bearer ' + casting_assistant_token})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Permission not found')

    # DELETE /actors -- success behavior
    # RBAC for Casting Producer role -- method allowed
    def test_delete_actor_producer(self):
            res = self.client().delete('/actors/8', headers = {'Authorization': 'Bearer ' + casting_producer_token})
            data = json.loads(res.data)

            self.assertEqual(res.status_code, 200)
            self.assertEqual(data['success'], True)
            self.assertTrue(data['actors'])
            self.assertTrue(data['delete_actor_id'])

    # DELETE /actors -- error behavior, invalid route
    # RBAC for Casting Producer role -- method allowed
    def test_delete_invalid_id_actor(self):
        res = self.client().delete('/actors/100', headers = {'Authorization': 'Bearer ' + casting_producer_token})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')

    # DELETE /actors -- success behavior
    # RBAC for Casting Director role -- method allowed
    def test_delete_actor_director(self):
            res = self.client().delete('/actors/7', headers = {'Authorization': 'Bearer ' + casting_director_token})
            data = json.loads(res.data)

            self.assertEqual(res.status_code, 200)
            self.assertEqual(data['success'], True)
            self.assertTrue(data['actors'])
            self.assertTrue(data['delete_actor_id'])

    # DELETE /movies -- success behavior
    # RBAC for Casting Producer role -- method allowed
    def test_delete_movie_producer(self):
            res = self.client().delete('/movies/5', headers = {'Authorization': 'Bearer ' + casting_producer_token})
            data = json.loads(res.data)

            self.assertEqual(res.status_code, 200)
            self.assertEqual(data['success'], True)
            self.assertTrue(data['movies'])
            self.assertTrue(data['delete_movie_id'])

    # DELETE /movies -- error behavior
    # RBAC for Casting Director role -- method not allowed
    def test_delete_movie_director(self):
            res = self.client().delete('/movies/3', headers = {'Authorization': 'Bearer ' + casting_director_token})
            data = json.loads(res.data)

            self.assertEqual(res.status_code, 403)
            self.assertEqual(data['success'], False)
            self.assertEqual(data['message'], 'Permission not found')




# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
