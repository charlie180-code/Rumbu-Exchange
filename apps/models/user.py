from flask_login import UserMixin
from .. import db
from datetime import datetime

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    phone_number = db.Column(db.String)
    email = db.Column(db.String, unique=True, nullable=False)
    password_hash = db.Column(db.String, nullable=False)
    profile_picture = db.Column(db.String)
    gender = db.Column(db.String)
    date_of_birth = db.Column(db.Date, default=datetime.utcnow)
    member_since = db.Column(db.Date, default=datetime.utcnow)
    transactions = db.relationship('Transaction', backref='user', lazy=True)
    wallets = db.relationship('Wallet', backref='user', lazy=True)
    active = db.Column(db.Boolean, default=True)

    def get_id(self):
        return str(self.id)

    def __repr__(self):
        return f"<User {self.email}>"
