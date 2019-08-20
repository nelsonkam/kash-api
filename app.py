import logging
from flask import Flask
from flask.logging import default_handler
from flask_jwt_extended import JWTManager
import config
from services import auth, upload, notify

# db logger
# logger = logging.getLogger('orator.connection.queries')
# logger.setLevel(logging.DEBUG)
# logger.addHandler(default_handler)

app = Flask(__name__)
app.config.from_pyfile("config.py")
jwt = JWTManager(app)
app.register_blueprint(auth.blueprint)
app.register_blueprint(upload.blueprint)
app.register_blueprint(notify.blueprint)


if __name__ == "__main__":
    app.run()
