import unittest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import create_app, db
from app.models import User, Event
import time


class TestRoutes(unittest.TestCase):

    def setUp(self):
        # Set up a test app
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()

        with self.app.app_context():
            # Generate a unique username based on the timestamp
            unique_username = f'testuser_{int(time.time())}'

            # Create a new test user with a unique username
            user = User(username=unique_username, email='test@example.com')
            user.set_password('password')
            db.session.add(user)
            db.session.commit()

            # Store the unique username for use in tests
            self.username = unique_username

    def login_test_user(self):
        return self.client.post('/login', data=dict(
            email='test@example.com',
            password='password'
        ), follow_redirects=True)
    
    def tearDown(self):
        # Clean up the database
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def login(self):
        """Helper method to log in the test user."""
        return self.client.post('/login', data=dict(
            email='testuser@example.com',
            password='password'
        ), follow_redirects=True)

    def test_main_page_access(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Campus Sports Connect', response.data)

    def test_login_page_access(self):
        response = self.client.get('/login')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Login', response.data)

    def test_register_page_access(self):
        response = self.client.get('/register')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Register', response.data)

    def test_logout(self):
        self.login()
        response = self.client.get('/logout', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Login', response.data)

if __name__ == '__main__':
    unittest.main()
