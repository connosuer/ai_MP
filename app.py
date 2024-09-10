from flask import Flask
from auth import auth_bp
from marketplace import marketplace_bp
from model_composition import composition_bp
from config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(marketplace_bp)
    app.register_blueprint(composition_bp)
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)