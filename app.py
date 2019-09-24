import logging
from flask import Flask
from flask.logging import default_handler
from flask_jwt_extended import JWTManager
from flask_cors import CORS
import config
from services import auth, upload, notify, product, feed, category

# db logger
# logger = logging.getLogger('orator.connection.queries')
# logger.setLevel(logging.DEBUG)
# logger.addHandler(default_handler)

app = Flask(__name__)
app.config.from_pyfile("config.py")
CORS(app)
jwt = JWTManager(app)
app.register_blueprint(auth.blueprint)
app.register_blueprint(upload.blueprint)
app.register_blueprint(notify.blueprint)
app.register_blueprint(product.blueprint)
app.register_blueprint(feed.blueprint)
app.register_blueprint(category.blueprint)


if __name__ == "__main__":
    app.run()
