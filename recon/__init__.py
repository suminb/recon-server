import os
import sys

from flask import Flask, jsonify
from flask_cors import CORS
from logbook import Logger, StreamHandler


__version__ = '0.1.0'


StreamHandler(sys.stderr).push_application()
log = Logger('recon')


def create_app(name=__name__, config=None):
    if config is None:
        config = {}

    app = Flask(name)
    app.secret_key = os.environ.get('SECRET', 'default_secret_key')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['RECON_DB_URL']
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['DEBUG'] = bool(os.environ.get('RECON_DEBUG'))

    app.config.update(config)

    CORS(app, resources={r'/api/v1/*': {'origins': '*'}})

    from recon.models import db, CustomJSONEncoder
    db.init_app(app)
    app.json_encoder = CustomJSONEncoder

    from recon.api import api_module
    app.register_blueprint(api_module, url_prefix='/api')

    @app.errorhandler(Exception)
    def handle_error(error):
        try:
            status_code = error.code
        except AttributeError:
            status_code = 500
        return jsonify(error=str(error)), status_code

    return app


def run_server(app):
    host = os.environ.get('RECON_HOST', '0.0.0.0')
    port = int(os.environ.get('RECON_PORT', 8080))
    app.run(host=host, port=port)
