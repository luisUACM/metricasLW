from flask import Flask

def init_app():
    app = Flask(__name__)
    app.config['DEBUG'] = True
    app.secret_key = '123456'

    with app.app_context():
        from . import routes
        return app