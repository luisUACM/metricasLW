from flask import Flask

def init_app():
    app = Flask(__name__)
    app.config['DEBUG'] = True

    with app.app_context():
        from . import routes
        return app