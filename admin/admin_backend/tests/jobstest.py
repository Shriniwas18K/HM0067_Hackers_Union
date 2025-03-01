import pytest
from flask import Flask, json
from unittest.mock import Mock, patch
from bson import ObjectId
import sqlite3
from jobs import jobs

@pytest.fixture
def app():
    """
    Fixture to create a Flask test application.
    Returns:
        Flask: A Flask test application instance
    """
    app = Flask(__name__)
    app.register_blueprint(jobs)
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

@pytest.fixture
def mock_mongo():
    """
    Fixture to mock MongoDB connection and operations.
    Returns:
        Mock: A mocked MongoDB connection
    """
    with patch('jobs.get_mongo_connection') as mock:
        mock_db = Mock()
        mock.return_value = mock_db
        yield mock_db

@pytest.fixture
def mock_rdbms():
    """
    Fixture to mock RDBMS connection and operations.
    Returns:
        Mock: A mocked RDBMS connection
    """
    with patch('jobs.get_rdbms_connection') as mock:
        mock_conn = Mock()
        mock_cursor = Mock()
        mock_conn.cursor.return_value = mock_cursor
        mock.return_value = mock_conn
        yield mock_conn, mock_cursor

def test_post_job_success(client, mock_auth, mock_mongo):
    """
    Test successful job posting creation.
    """
    # Arrange
    test_job = {
        "title": "Test Job",
        "description": "Test Description"
    }
    mock_mongo['job_postings'].insert_one.return_value.inserted_id = ObjectId("507f1f77bcf86cd799439011")

    # Act
    response = client.post('/jobs/create', 
                         data=json.dumps(test_job),
                         content_type='application/json')
    
    # Assert
    assert response.status_code == 201
    assert "jobid" in json.loads(response.data)

def test_apply_job_success(client, mock_rdbms):
    """
    Test successful job application submission.
    """
    # Arrange
    mock_conn, mock_cursor = mock_rdbms

    # Act
    response = client.get('/jobs/application?jobid=123&userid=456')

    # Assert
    assert response.status_code == 201
    mock_cursor.execute.assert_called_once()
    assert json.loads(response.data)["msg"] == "Application submitted successfully"

def test_segragate_applications_success(client, mock_auth, mock_rdbms):
    """
    Test successful retrieval of job applications.
    """
    # Arrange
    mock_conn, mock_cursor = mock_rdbms
    mock_cursor.fetchall.return_value = [
        (1, "user1", "2024-03-01"),
        (2, "user2", "2024-03-01")
    ]

    # Act
    response = client.get('/jobs/segragate?jobid=123')

    # Assert
    assert response.status_code == 200
    assert "applns" in json.loads(response.data)
    mock_cursor.execute.assert_called_once()

def test_shortlist_application_success(client, mock_auth, mock_rdbms):
    """
    Test successful shortlisting of an application.
    """
    # Arrange
    mock_conn, mock_cursor = mock_rdbms

    # Act
    response = client.get('/jobs/shortlist?applnid=123&userid=456')

    # Assert
    assert response.status_code == 200
    assert json.loads(response.data)["msg"] == "Application shortlisted successfully"
    mock_cursor.execute.assert_called_once()

def test_collect_job_success(client, mock_auth, mock_mongo):
    """
    Test successful retrieval of job details.
    """
    # Arrange
    mock_job_data = {
        "title": "Test Job",
        "description": "Test Description"
    }
    mock_mongo['job_postings'].find_one.return_value = mock_job_data

    # Act
    response = client.get('/jobs/collect?jobid=507f1f77bcf86cd799439011')

    # Assert
    assert response.status_code == 200
    assert json.loads(response.data)["data"] == mock_job_data

def test_post_job_failure(client, mock_auth, mock_mongo):
    """
    Test job posting creation with database error.
    """
    # Arrange
    mock_mongo['job_postings'].insert_one.side_effect = Exception("Database error")

    # Act
    response = client.post('/jobs/create',
                         data=json.dumps({"title": "Test"}),
                         content_type='application/json')

    # Assert
    assert response.status_code == 400
    assert "error" in json.loads(response.data)

def test_apply_job_failure(client, mock_rdbms):
    """
    Test job application with database error.
    """
    # Arrange
    mock_conn, mock_cursor = mock_rdbms
    mock_cursor.execute.side_effect = sqlite3.Error("Database error")

    # Act
    response = client.get('/jobs/application?jobid=123&userid=456')

    # Assert
    assert response.status_code == 400
    assert "error" in json.loads(response.data)