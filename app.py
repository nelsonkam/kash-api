import logging

from flask import Flask
from flask.logging import default_handler
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_orator import Orator

cors = CORS()
jwt = JWTManager()
db = Orator()

logging.basicConfig(level=logging.DEBUG)

def register_blueprints(app):
    from services import auth, upload, notify, product, feed, category, shop, graphql
    from commands import blueprint

    app.register_blueprint(auth.blueprint)
    app.register_blueprint(upload.blueprint)
    app.register_blueprint(notify.blueprint)
    app.register_blueprint(product.blueprint)
    app.register_blueprint(feed.blueprint)
    app.register_blueprint(category.blueprint)
    app.register_blueprint(shop.blueprint)
    app.register_blueprint(graphql.blueprint)
    app.register_blueprint(blueprint)



def create_app(config_file="config.py"):
    app = Flask(__name__)
    app.config.from_pyfile(config_file)
    cors.init_app(app)
    jwt.init_app(app)
    db.init_app(app)
    register_blueprints(app)
    return app

