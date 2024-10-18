import unittest
from app import create_app

class TestRoutes(unittest.TestCase):

    def setUp(self):
        # Set up a test app
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()

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

    def test_profile_page_access(self):
        # Assuming the user needs to be logged in to access profile, here we'll just test for redirection
        response = self.client.get('/profile', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Login', response.data)  # Expect redirection to login page if not logged in

if __name__ == '__main__':
    unittest.main()