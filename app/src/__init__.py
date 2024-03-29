from flask import Flask

def init_app():
    app = Flask(__name__)
    app.config['DEBUG'] = True
    app.secret_key = '123456'
    app.config['UPLOAD_FOLDER'] = 'src/uploads/'

    with app.app_context():
        #  =========================================================
        #   
        #   Aquí importar todos los archivos que usen el objeto app
        #   
        #  =========================================================

        from .routes import routes, routes_luis, routes_wendy
        
        return app