import logging

from flask import Flask
from flask.logging import default_handler
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_orator import Orator

from logging.config import dictConfig

dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
    }},
    'handlers': {'wsgi': {
        'class': 'logging.StreamHandler',
        'stream': 'ext://flask.logging.wsgi_errors_stream',
        'formatter': 'default'
    }},
    'root': {
        'level': 'INFO',
        'handlers': ['wsgi']
    }
})

cors = CORS()
jwt = JWTManager()
db = Orator()

def register_blueprints(app):
    from services import auth, upload, notify, product, feed, category, shop, graphql, cart, checkout
    from commands import blueprint

    app.register_blueprint(auth.blueprint)
    app.register_blueprint(upload.blueprint)
    app.register_blueprint(notify.blueprint)
    app.register_blueprint(product.blueprint)
    app.register_blueprint(feed.blueprint)
    app.register_blueprint(category.blueprint)
    app.register_blueprint(shop.blueprint)
    app.register_blueprint(graphql.blueprint)
    app.register_blueprint(cart.blueprint)
    app.register_blueprint(checkout.blueprint)
    app.register_blueprint(blueprint)

def configure_gunicorn_logger(app):
    gunicorn_error_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers.extend(gunicorn_error_logger.handlers)
    app.logger.setLevel(logging.DEBUG)

def create_app(config_file="config.py"):
    app = Flask(__name__)
    app.config.from_pyfile(config_file)
    cors.init_app(app)
    jwt.init_app(app)
    db.init_app(app)
    register_blueprints(app)
    configure_gunicorn_logger(app)
    return app

