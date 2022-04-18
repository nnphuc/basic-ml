import os

from flask import Flask
import flask


def create_app(test_config=None):

    # create and configure the app
    app = Flask(__name__, instance_relative_config=False)

    if test_config is None:
        # Load the instance config, if it exists, when not testing

        app.config.from_pyfile('config.py', silent=False)
        app.logger.info('load test config is None')
        app.logger.info("root_path %s", app.root_path)
        app.logger.info(app.config)


    else:
        # Load the test config if passed in
        app.logger.info('load from test config')
        app.config.from_mapping(test_config)

    # ensure the instance floder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    app.logger.error("static " + app._static_folder)

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    from . import db
    db.init_app(app)

    from . import auth
    app.register_blueprint(auth.bp)

    return app
