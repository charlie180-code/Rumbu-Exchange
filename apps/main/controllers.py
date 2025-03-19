from flask import render_template, request, flash, url_for, redirect, current_app
from flask_login import login_required, current_user
from ..models.user import User
from ..models.transaction import Transaction
import os
from ..models.wallet import Wallet
from flask_babel import _
from .utils import fetch_nita_balance
from . import main
from datetime import datetime
from werkzeug.utils import secure_filename
from .. import db
from .forms import UserSettingsForm

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
    
@main.route('/user-settings', methods=['GET', 'POST'])
@login_required
def user_settings():
    form = UserSettingsForm()

    if request.method == 'GET':
        form.first_name.data = current_user.first_name
        form.last_name.data = current_user.last_name
        form.phone_number.data = current_user.phone_number
        form.email.data = current_user.email
        form.gender.data = current_user.gender
        form.date_of_birth.data = current_user.date_of_birth
        

    if form.validate_on_submit():
        current_user.first_name = form.first_name.data
        current_user.last_name = form.last_name.data
        current_user.phone_number = form.phone_number.data
        current_user.email = form.email.data
        current_user.gender = form.gender.data
        current_user.date_of_birth = form.date_of_birth.data

        if 'profile_picture' in request.files:
            profile_picture = request.files['profile_picture']
            if profile_picture.filename != '':
                upload_folder = current_app.config.get('UPLOAD_FOLDER', 'static/uploads')
                if not os.path.exists(upload_folder):
                    os.makedirs(upload_folder)

                filename = secure_filename(profile_picture.filename)
                file_path = os.path.join(upload_folder, filename)
                profile_picture.save(file_path)

                current_user.profile_picture = url_for('static', filename=f'uploads/{filename}')

        db.session.commit()
        flash(_('Vos paramètres ont été mis à jour!'), 'success')
        return redirect(url_for('user.user_settings'))

    return render_template(
        'main/user_settings.html',
        title=_('Paramètres'),
        form=form
    )


@main.route('/terms-and-conditions')
def terms_and_conditions():
    return render_template('main/terms_and_conditions.html', title=_('Termes et Conditions'))
