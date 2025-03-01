from flask import Flask
from routes.auth import auth
from routes.admin import admin
from routes.jobs import jobs
from routes.users import users
from db import db_inits
from flask_cors import CORS
app = Flask(__name__)
CORS(app)
db_inits()
app.register_blueprint(auth)
app.register_blueprint(admin)
app.register_blueprint(users)
app.register_blueprint(jobs)

if __name__ == '__main__':      
    app.run(debug=True)
