import unittest
from unittest.mock import patch
from flask import Flask
import json
from routes.admin import admin
class TestAdminRoutes(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.app.register_blueprint(admin, url_prefix='/admin')
        self.client = self.app.test_client()
        
    @patch('routes.admin.requires_auth')
    def test_admin_index_route_success(self, mock_requires_auth):
        # Configure the mock decorator to pass through the function
        mock_requires_auth.side_effect = lambda f: f
        
        # Make a request to the admin index route
        response = self.client.get('/admin/')
        
        # Check status code
        self.assertEqual(response.status_code, 200)
        
        # Parse the JSON response
        data = json.loads(response.data)
        
        # Check response content
        self.assertIn('message', data)
        self.assertEqual(data['message'], 'Greetings')
    
    @patch('routes.admin.requires_auth')
    def test_admin_index_route_unauthorized(self, mock_requires_auth):
        # Configure the mock to raise an unauthorized exception
        def mock_auth_failure(f):
            def wrapped(*args, **kwargs):
                return '', 401
            return wrapped
            
        mock_requires_auth.side_effect = mock_auth_failure
        
        # Make a request to the admin index route
        response = self.client.get('/admin/')
        
        # Check that we get an unauthorized status code
        self.assertEqual(response.status_code, 401)

if __name__ == '__main__':
    unittest.main()