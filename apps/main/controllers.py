from flask import render_template
from flask_login import login_required, current_user
from ..models.user import User
from ..models.transaction import Transaction
from ..models.wallet import Wallet
from flask_babel import _
from . import main

@main.route('/')
@login_required
def home():
    return render_template(
        'main/home.html', 
        title= _('Accueil')
    )

@main.route('/wallet')
@login_required
def wallet():
    wallets = Wallet.query.filter_by(user_id=current_user.id).all()
    selected_wallet = Wallet.query.filter_by(selected=True).first()
    return render_template(
        'main/wallet.html',
        wallets=wallets,
        selected_wallet=selected_wallet,
        title=_('Portefeuilles')
    )

@main.route('/transactions')
@login_required
def transactions():
    return render_template('main/transactions.html', title=_('Transactions'))


@main.route('/terms-and-conditions')
def terms_and_conditions():
    return render_template('main/terms_and_conditions.html', title=_('Termes et Conditions'))
