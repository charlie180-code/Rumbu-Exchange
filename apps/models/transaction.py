from .. import db
from datetime import datetime

class Transaction(db.Model):
    __tablename__ = 'transactions'
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float)
    nature = db.Column(db.String)
    created_at = db.Column(db.Date, default=datetime.utcnow)
    wallet_id = db.Column(db.ForeignKey('wallets.id'))
    user_id = db.Column(db.ForeignKey('users.id'))
    