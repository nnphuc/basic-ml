import os

from flask import Flask

def create_app(test_config=None):
    print("ok")
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # Load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
        app.logger.info('load test config is None')
        app.logger.info(app.root_path)
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

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    from . import db
    db.init_app(app)

    from . import auth
    app.register_blueprint(auth.bp)

    return app