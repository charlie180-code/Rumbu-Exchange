from flask import render_template
from flask_login import login_required
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
    return render_template('main/wallet.html', title=_('Portefeuilles'))

@main.route('/transactions')
@login_required
def transactions():
    return render_template('main/transactions.html', title=_('Transactions'))


@main.route('/terms-and-conditions')
def terms_and_conditions():
    return render_template('main/terms_and_conditions.html', title=_('Termes et Conditions'))
