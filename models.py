from extensions import db
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    ethereum_address = db.Column(db.String(42), unique=True, nullable=False)
    reputation_score = db.Column(db.Float, default=0.0)
    bio = db.Column(db.Text)
    joined_date = db.Column(db.DateTime, default=db.func.current_timestamp())

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Model(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    price = db.Column(db.Float, nullable=False)
    file_hash = db.Column(db.String(100), nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    owner = db.relationship('User', backref=db.backref('models', lazy=True))
    is_available = db.Column(db.Boolean, default=True)
    average_rating = db.Column(db.Float, default=0.0)
    total_ratings = db.Column(db.Integer, default=0)

    def __repr__(self):
        return f'<Model {self.name}>'