from flask import Flask
from routes.auth import auth
from routes.admin import admin

app = Flask(__name__)
app.register_blueprint(auth)
app.register_blueprint(admin)
if __name__ == '__main__':
    app.run(debug=True)
