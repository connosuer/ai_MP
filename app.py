from flask import Flask
from config import Config
from extensions import db

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    db.init_app(app)
    
    with app.app_context():
        from auth import auth_bp
        from marketplace import marketplace_bp
        
        app.register_blueprint(auth_bp)
        app.register_blueprint(marketplace_bp)
        
        db.create_all()
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)