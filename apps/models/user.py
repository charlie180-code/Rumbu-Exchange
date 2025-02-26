from .. import db
from datetime import datetime



class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    phone_number = db.Column(db.String)
    email = db.Column(db.String)
    password_hash = db.Column(db.String)
    gender = db.Column(db.String)
    date_of_birth = db.Column(db.Date, default=datetime.utcnow)
    member_since = db.Column(db.Date, default=datetime.utcnow)
    transactions = db.relationship('Transaction', backref='user', lazy=True)
    wallets = db.relationship('Wallet', backref='user', lazy=True)
    active = db.Column(db.Boolean, default=True)
    
    @property
    def is_active(self):
        return self.active

    def __repr__(self):
        return f"<User {self.email}>"
    