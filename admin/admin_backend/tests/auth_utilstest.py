import pytest
from flask import Flask, json
from unittest.mock import Mock, patch
import base64
from auth_utils import requires_auth, check_auth, auth

@pytest.fixture
def app():
    """
    Fixture to create a Flask test application.
    Returns:
        Flask: A Flask test application instance
    """
    app = Flask(__name__)
    app.register_blueprint(auth)
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
def mock_db_connection():
    """
    Fixture to mock RDBMS connection and cursor.
    Returns:
        tuple: (Mock connection, Mock cursor)
    """
    with patch('auth_utils.get_rdbms_connection') as mock_conn:
        mock_cursor = Mock()
        mock_conn.return_value.cursor.return_value = mock_cursor
        yield mock_conn.return_value, mock_cursor

def create_auth_header(username, password):
    """
    Helper function to create Basic Auth header.
    Args:
        username (str): Username for authentication
        password (str): Password for authentication
    Returns:
        dict: Headers dictionary with Basic Auth
    """
    credentials = base64.b64encode(f"{username}:{password}".encode()).decode()
    return {'Authorization': f'Basic {credentials}'}

class TestAuthUtils:
    """Test suite for authentication utilities"""

    def test_check_auth_valid_credentials(self, mock_db_connection):
        """Test successful authentication with valid credentials"""
        # Arrange
        mock_conn, mock_cursor = mock_db_connection
        mock_cursor.fetchone.return_value = {'password': 'hashed_password'}
        with patch('auth_utils.check_password_hash', return_value=True):
            credentials = base64.b64encode("test:password".encode()).decode()
            
            # Act
            result = check_auth(credentials)
            
            # Assert
            assert result is True
            mock_cursor.execute.assert_called_once()

    def test_check_auth_invalid_credentials(self, mock_db_connection):
        """Test failed authentication with invalid credentials"""
        # Arrange
        mock_conn, mock_cursor = mock_db_connection
        mock_cursor.fetchone.return_value = {'password': 'hashed_password'}
        with patch('auth_utils.check_password_hash', return_value=False):
            credentials = base64.b64encode("test:wrong_password".encode()).decode()
            
            # Act
            result = check_auth(credentials)
            
            # Assert
            assert result is False

    def test_check_auth_nonexistent_user(self, mock_db_connection):
        """Test authentication with non-existent user"""
        # Arrange
        mock_conn, mock_cursor = mock_db_connection
        mock_cursor.fetchone.return_value = None
        credentials = base64.b64encode("nonexistent:password".encode()).decode()
        
        # Act
        result = check_auth(credentials)
        
        # Assert
        assert result is False

    def test_protected_route_no_auth_header(self, client):
        """Test accessing protected route without auth header"""
        # Act
        response = client.get('/auth/protected')
        
        # Assert
        assert response.status_code == 401
        assert json.loads(response.data)["message"] == "Authentication required."

    def test_protected_route_invalid_auth_header(self, client):
        """Test accessing protected route with invalid auth header"""
        # Act
        response = client.get('/auth/protected', headers={'Authorization': 'Invalid'})
        
        # Assert
        assert response.status_code == 401

    def test_protected_route_valid_auth(self, client, mock_db_connection):
        """Test accessing protected route with valid authentication"""
        # Arrange
        mock_conn, mock_cursor = mock_db_connection
        mock_cursor.fetchone.return_value = {'password': 'hashed_password'}
        with patch('auth_utils.check_password_hash', return_value=True):
            headers = create_auth_header('test', 'password')
            
            # Act
            response = client.get('/auth/protected', headers=headers)
            
            # Assert
            assert response.status_code == 200
            assert "You have accessed a protected route" in json.loads(response.data)["message"]

    def test_check_auth_malformed_token(self):
        """Test authentication with malformed token"""
        # Arrange
        invalid_token = "invalid_base64_token"
        
        # Act
        result = check_auth(invalid_token)
        
        # Assert
        assert result is False
