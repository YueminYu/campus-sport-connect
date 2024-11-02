import unittest
import sys
import os
import time
from flask import url_for


if __name__ == "__main__" and __package__ is None:
    current_path = os.path.dirname(os.path.abspath(__file__))
    parent_path = os.path.dirname(current_path)
    sys.path.insert(0, parent_path)
    from app import create_app, db
    from app.models import User, Event
else:
    from ..app import create_app, db
    from ..app.models import User, Event

class TestRoutes(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['WTF_CSRF_ENABLED'] = False  
        self.client = self.app.test_client()

        with self.app.app_context():
            db.create_all()
            user = User(username="testuser", email="test@example.com")
            user.set_password("password")
            db.session.add(user)
            db.session.commit()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def login_test_user(self):
        """Helper method to log in the test user."""
        return self.client.post('/login', data=dict(
            email='test@example.com',
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

    def test_register_user(self):
        response = self.client.post('/register', data=dict(
            username='newuser',
            email='newuser@example.com',
            password='newpassword',
            confirm_password='newpassword'
        ), follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_login_with_wrong_password(self):
        response = self.client.post('/login', data=dict(
            email='test@example.com',
            password='wrongpassword'
        ), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Login failed. Please check your email and password.', response.data)

    def test_logout(self):
        self.login_test_user()
        response = self.client.get('/logout', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Login', response.data)

    def test_create_event(self):
        self.login_test_user()
        response = self.client.post('/create_event', data=dict(
            sport_type='Basketball',
            date='2024-11-02',
            time='15:00',
            location='UIUC Court',
            max_participants=10
        ), follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_delete_event(self):
        self.login_test_user()
        with self.app.app_context():
            user = User.query.filter_by(username="testuser").first()
            event = Event(sport_type='Tennis', date='2024-11-03', time='14:00',
                          location='Court 1', max_participants=5, user_id=user.id)
            db.session.add(event)
            db.session.commit()
            event_id = event.id

        response = self.client.post(f'/delete_event/{event_id}', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_join_event(self):
        self.login_test_user()
        with self.app.app_context():
            other_user = User(username='anotheruser', email='another@example.com')
            other_user.set_password('password')
            db.session.add(other_user)
            db.session.commit()

            event = Event(sport_type='Soccer', date='2024-11-04', time='10:00',
                          location='Field 1', max_participants=5, user_id=other_user.id)
            db.session.add(event)
            db.session.commit()
            event_id = event.id

        response = self.client.post(f'/join_event/{event_id}', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_leave_event(self):
        self.login_test_user()
        with self.app.app_context():
            other_user = User(username='eventhost', email='eventhost@example.com')
            other_user.set_password('password')
            db.session.add(other_user)
            db.session.commit()

            event = Event(sport_type='Volleyball', date='2024-11-05', time='09:00',
                          location='Gym', max_participants=8, user_id=other_user.id)
            event.participants.append(User.query.filter_by(username="testuser").first())
            db.session.add(event)
            db.session.commit()
            event_id = event.id

        response = self.client.post(f'/delete_event/{event_id}', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_view_all_events(self):
        self.login_test_user()
        with self.app.app_context():
            user = User.query.filter_by(username="testuser").first()
            event = Event(sport_type='Baseball', date='2024-11-06', time='13:00',
                          location='Stadium', max_participants=15, user_id=user.id)
            db.session.add(event)
            db.session.commit()

        response = self.client.get('/view_all_events')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Baseball', response.data)
        self.assertIn(b'Stadium', response.data)
        self.assertIn(b'0/15', response.data)

    def test_edit_profile(self):
        self.login_test_user()
        response = self.client.post('/edit_profile', data=dict(
            username='updateduser',
            email='updated@example.com',
            basketball=True,
            soccer=False
        ), follow_redirects=True)
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()
