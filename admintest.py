import pytest
from flask import Flask
from unittest.mock import patch
from admin import admin

@pytest.fixture
def app():
    """
    Fixture to create a Flask test application.
    Returns:
        Flask: A Flask test application instance
    """
    app = Flask(__name__)
    app.register_blueprint(admin)
    return app

@pytest.fixture
def client(app):
    """
    Fixture to create a test client.
    Args:
        app: Flask application fixture
    Returns:
        FlaskClient: A Flask test client
    """
    return app.test_client()

@pytest.fixture
def mock_auth():
    """
    Fixture to mock the authentication decorator.
    Simulates a successfully authenticated request.
    """
    with patch('routes.auth_utils.requires_auth', lambda f: f):
        yield

def test_index_route_without_auth(client):
    """
    Test accessing index route without authentication.
    Should return 401 Unauthorized.
    """
    # Act
    response = client.get('/')
    
    # Assert
    assert response.status_code == 401

def test_index_route_with_auth(client, mock_auth):
    """
    Test accessing index route with valid authentication.
    Should return 200 OK with greeting message.
    """
    # Act
    response = client.get('/')
    
    # Assert
    assert response.status_code == 200
    assert "message" in response.get_json()
    assert "Greetings" in response.get_json()["message"]

def test_index_route_invalid_method(client, mock_auth):
    """
    Test accessing index route with invalid HTTP method.
    Should return 405 Method Not Allowed.
    """
    # Act
    response = client.post('/')
    
    # Assert
    assert response.status_code == 405