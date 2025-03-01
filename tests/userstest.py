import pytest
from flask import Flask
from unittest.mock import Mock, patch
from bson.objectid import ObjectId
from users import users, collect_user
# Import the function to test using absolute import

@pytest.fixture
def app():
    """Create a Flask test app with the users blueprint registered"""
    app = Flask(__name__)
    app.register_blueprint(users)
    return app

@pytest.fixture
def client(app):
    """Create a test client"""
    return app.test_client()

@pytest.fixture
def mock_mongo():
    """Mock MongoDB connection"""
    with patch('users.get_mongo_connection') as mock:
        yield mock

@pytest.fixture
def mock_auth():
    """Mock the authentication decorator"""
    with patch('routes.auth_utils.requires_auth', lambda f: f) as mock:
        yield mock

def test_collect_user_successful(client, mock_mongo, mock_auth):
    """Test successful user retrieval"""
    # Prepare test data
    test_user = {'name': 'Test User', 'email': 'test@example.com'}
    user_id = str(ObjectId())
    
    # Configure mock
    mock_db = Mock()
    mock_mongo.return_value = {'users': mock_db}
    mock_db.find_one.return_value = test_user

    # Make request
    response = client.get(f'/users/?userid={user_id}')
    
    # Assertions
    assert response.status_code == 200
    assert response.json == {'data': test_user}
    mock_db.find_one.assert_called_once_with(
        {'_id': ObjectId(user_id)},
        {'_id': 0}
    )

def test_collect_user_invalid_id(client, mock_mongo, mock_auth):
    """Test invalid user ID handling"""
    # Configure mock
    mock_db = Mock()
    mock_mongo.return_value = {'users': mock_db}
    mock_db.find_one.return_value = None

    # Make request
    response = client.get('/users/?userid=invalid_id')
    
    # Should raise an error due to invalid ObjectId
    assert response.status_code == 500

def test_collect_user_missing_id(client, mock_mongo, mock_auth):
    """Test missing user ID parameter"""
    response = client.get('/users/')
    assert response.status_code == 500

@pytest.mark.hypothesis
def test_collect_user_mongodb_error(client, mock_mongo, mock_auth):
    """Test MongoDB connection error handling"""
    mock_mongo.side_effect = Exception("MongoDB connection failed")
    
    response = client.get('/users/?userid=' + str(ObjectId()))
    assert response.status_code == 500

def test_collect_user_requires_auth(app):
    """Test that the endpoint requires authentication"""
    # Verify that requires_auth decorator is applied
    view_function = app.view_functions['user.collect_user']
    assert hasattr(view_function, '__wrapped__')