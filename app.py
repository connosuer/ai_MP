from flask import Flask
from config import Config
from extensions import db, init_db
from auth import auth_bp
from marketplace import marketplace_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    init_db(app)
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(marketplace_bp)
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)