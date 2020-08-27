import logging

from ariadne import make_executable_schema, load_schema_from_path
from flask import Flask
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_orator import Orator
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


cors = CORS()
jwt = JWTManager()
db = Orator()
sqla_db = SQLAlchemy(session_options={'autocommit': True})
migrate = Migrate(compare_type=True)


def register_blueprints(app):
    from services import auth, upload, notify, product, feed, category, shop
    from commands import blueprint

    app.register_blueprint(auth.blueprint)
    app.register_blueprint(upload.blueprint)
    app.register_blueprint(notify.blueprint)
    app.register_blueprint(product.blueprint)
    app.register_blueprint(feed.blueprint)
    app.register_blueprint(category.blueprint)
    app.register_blueprint(shop.blueprint)
    # app.register_blueprint(graphql.blueprint)
    app.register_blueprint(blueprint)

def create_app(config_file="config.py"):
    app = Flask(__name__)
    app.config.from_pyfile(config_file)
    cors.init_app(app)
    jwt.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    register_blueprints(app)
    return app
