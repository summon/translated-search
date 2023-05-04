from flask import Flask
from translatedsearch import settings


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
    )

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    from . import translatedsearch_ui
    app.register_blueprint(translatedsearch_ui.bp)
    app.add_url_rule('/', endpoint='index')

    return app