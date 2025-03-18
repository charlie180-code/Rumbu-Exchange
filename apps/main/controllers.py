from flask import render_template, request
from flask_login import login_required, current_user
from ..models.user import User
from ..models.transaction import Transaction
from ..models.wallet import Wallet
from flask_babel import _
from .utils import fetch_nita_balance
from . import main
from datetime import datetime

@main.route('/')
@login_required
def home():
    # Fetch the selected wallet for the current user
    selected_wallet = Wallet.query.filter_by(user_id=current_user.id, selected=True).first()

    if selected_wallet:
        balance = selected_wallet.balance
    else:
        balance = 0.0  # Default balance if no wallet is selected

    # Fetch the latest 5 transactions for the current user
    latest_transactions = Transaction.query.filter_by(user_id=current_user.id).order_by(Transaction.created_at.desc()).limit(5).all()

    if current_user.first_name:
        name = current_user.first_name
        if current_user.last_name:
            name += ' ' + current_user.last_name
    elif current_user.last_name:
        name = current_user.last_name
    elif current_user.email:
        name = current_user.email.split('@')[0]
    else:
        name = current_user.phone_number

    # Fetch user information (e.g., name, profile picture, balance)
    user_info = {
        'name': name,
        'profile_pic': current_user.profile_picture,
        'balance': balance,
        'currency': selected_wallet.currency
    }

    return render_template(
        'main/home.html',
        title=_('Accueil'),
        user_info=user_info,
        latest_transactions=latest_transactions,
        year=datetime.now().year
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
        title=_('Portefeuilles'),
        year=datetime.now().year
    )

@main.route('/transactions')
@login_required
def transactions():
    page = request.args.get('page', 1, type=int)
    per_page = 10

    transactions_pagination = Transaction.query.filter_by(user_id=current_user.id).order_by(Transaction.created_at.desc()).paginate(page=page, per_page=per_page)

    return render_template(
        'main/transactions.html',
        title=_('Transactions'),
        transactions=transactions_pagination,
        year=datetime.now().year
    )
    
    

@main.route('/terms-and-conditions')
def terms_and_conditions():
    return render_template('main/terms_and_conditions.html', title=_('Termes et Conditions'))
