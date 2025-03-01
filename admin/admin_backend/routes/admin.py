from flask import Flask, request, jsonify, Blueprint
from routes.auth_utils import requires_auth

admin = Blueprint('admin', __name__)

@admin.route('/')
@requires_auth
def index():
    return """
    {
        "message":"Greetings",
    }
    """