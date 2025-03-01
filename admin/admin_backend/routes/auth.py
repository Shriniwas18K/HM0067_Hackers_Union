from flask import Flask, request, jsonify, Blueprint
from werkzeug.security import generate_password_hash
from db import get_rdbms_connection

auth = Blueprint('auth', __name__)


@auth.route('/register', methods=['POST'])
def register():
    """
    Handles user registration.

    For POST requests, processes the registration form data and creates a new user.

    Request JSON Body:
        {
            "username": "your_username",
            "password": "your_password"
        }

    Returns:
        JSON response indicating success or failure.
    """
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'error': 'Username and password are required'}), 400

    conn = get_rdbms_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM users WHERE username = ?', (username,))
    user = cur.fetchone()
    if user:
        return jsonify({'error': 'User already exists'}), 400

    cur.execute('INSERT INTO users (username, password) VALUES (?, ?)',
                (username, generate_password_hash(password)))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'message': 'Registration successful'}), 201
