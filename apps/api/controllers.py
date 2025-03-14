from flask import render_template
from flask_login import login_required
from . import api

@login_required
@api.route('/create_new_wallet')
def add_wallet():
    return render_template('api/create_new_wallet.html')