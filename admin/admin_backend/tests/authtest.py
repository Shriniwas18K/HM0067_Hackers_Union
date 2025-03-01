import pytest
from flask import Flask, json
from unittest.mock import Mock, patch
import sqlite3
from auth import auth

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
    with patch('auth.get_rdbms_connection') as mock_conn:
        mock_cursor = Mock()
        mock_conn.return_value.cursor.return_value = mock_cursor
        yield mock_conn.return_value, mock_cursor

def test_register_success(client, mock_db_connection):
    """
    Test successful user registration with valid credentials.
    """
    # Arrange
    mock_conn, mock_cursor = mock_db_connection
    mock_cursor.fetchone.return_value = None  # User doesn't exist
    test_user = {
        "username": "testuser",
        "password": "testpass123"
    }

    # Act
    response = client.post('/register',
                          data=json.dumps(test_user),
                          content_type='application/json')
    
    # Assert
    assert response.status_code == 201
    assert json.loads(response.data)["message"] == "Registration successful"
    # Verify DB operations
    mock_cursor.execute.assert_called()
    mock_conn.commit.assert_called_once()

def test_register_missing_credentials(client):
    """
    Test registration with missing credentials.
    Should return 400 Bad Request.
    """
    # Test cases for missing credentials
    test_cases = [
        {},  # Empty payload
        {"username": "testuser"},  # Missing password
        {"password": "testpass123"},  # Missing username
    ]

    for test_case in test_cases:
        # Act
        response = client.post('/register',
                             data=json.dumps(test_case),
                             content_type='application/json')
        
        # Assert
        assert response.status_code == 400
        assert "error" in json.loads(response.data)
        assert json.loads(response.data)["error"] == "Username and password are required"

def test_register_existing_user(client, mock_db_connection):
    """
    Test registration with an existing username.
    Should return 400 Bad Request.
    """
    # Arrange
    mock_conn, mock_cursor = mock_db_connection
    mock_cursor.fetchone.return_value = ("existing_user", "hashed_password")  # User exists
    test_user = {
        "username": "existing_user",
        "password": "testpass123"
    }

    # Act
    response = client.post('/register',
                          data=json.dumps(test_user),
                          content_type='application/json')
    
    # Assert
    assert response.status_code == 400
    assert json.loads(response.data)["error"] == "User already exists"

def test_register_database_error(client, mock_db_connection):
    """
    Test registration with database error.
    Should handle the error gracefully.
    """
    # Arrange
    mock_conn, mock_cursor = mock_db_connection
    mock_cursor.execute.side_effect = sqlite3.Error("Database error")
    test_user = {
        "username": "testuser",
        "password": "testpass123"
    }

    # Act
    response = client.post('/register',
                          data=json.dumps(test_user),
                          content_type='application/json')
    
    # Assert
    assert response.status_code == 400