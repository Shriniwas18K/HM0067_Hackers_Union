from flask import Flask, request, jsonify, Blueprint
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
from db import get_rdbms_connection
import base64

app = Flask(__name__)
auth = Blueprint('auth', __name__)

def check_auth(token):
    """
    Verifies if the provided username and password in the token are correct.

    Args:
        token (str): The Base64-encoded token containing the username and password.

    Returns:
        bool: True if authentication is successful, False otherwise.
    """
    try:
        token_decoded = base64.b64decode(token).decode('utf-8')
        username, password = token_decoded.split(':')
        conn = get_rdbms_connection()
        cur = conn.cursor()
        cur.execute('SELECT password FROM users WHERE username = ?', (username,))
        user = cur.fetchone()
        cur.close()
        conn.close()
        if user and check_password_hash(user['password'], password):
            return True
        return False
    except Exception:
        return False

def requires_auth(f):
    """
    Decorator function that ensures authentication is required for a route.

    Args:
        f (function): The function to be decorated.

    Returns:
        function: The decorated function that requires authentication.
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Basic '):
            return jsonify({'message': 'Authentication required.'}), 401

        token = auth_header.split(' ')[1]
        if not check_auth(token):
            return jsonify({'message': 'Invalid credentials.'}), 401

        return f(*args, **kwargs)
    return decorated

