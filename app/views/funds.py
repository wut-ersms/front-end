from flask import Blueprint, render_template, request, session, redirect, url_for, flash, current_app
import requests
import logging

from sqlalchemy.cyextension.processors import to_float

logging.basicConfig(level=logging.DEBUG)

funds_bp = Blueprint(
    "funds",
    __name__,
    template_folder="templates",
    url_prefix="/funds"
)



# Base URL of the payment service
PAYMENT_SERVICE_URL = "http://host.docker.internal:8092"  # current_app.config['PAYMENT_SERVICE_URL']

@funds_bp.route('/', methods=['GET'])
def add_funds_form():
    # Fetch available payment methods
    logging.info(f"Adding funds to {session.get('wallet_balance', 0.0)}")
    try:
        logging.info(f"{PAYMENT_SERVICE_URL}/channel/all")
        resp = requests.get(f"{PAYMENT_SERVICE_URL}/channel/all", timeout=5)
        resp.raise_for_status()
        data = resp.json()
        logging.info(data)
    except Exception:
        flash('Unable to load payment methods.', 'error')
        channels = []
    else:
        channels = data.get('channels', []) if data.get('result') == 'success' else []
    return render_template('funds/add_funds.html', channels=channels)

@funds_bp.route('/', methods=['POST'])
def submit_add_funds():
    amount = request.form['amount']
    description = request.form.get('description', 'Add funds')
    email = session.get("user", {}).get("email")
    name = session.get("user", {}).get("name")

    success_url = url_for('funds.confirmation', _external=True)
    error_url = url_for('funds.add_funds_error', _external=True)

    payload = {
        'amount': amount,
        'description': description,
        'email': email,
        'name': name,
        'successPage': success_url,
        'errorPage': error_url
    }
    logging.info("Hello")
    logging.info(payload)
    resp = requests.post(f"{PAYMENT_SERVICE_URL}/transaction/new", params=payload)

    logging.info(resp.headers)

    if resp.is_redirect and 'Location' in resp.headers:
        session['wallet_balance'] = session.get('wallet_balance', 0.0) + to_float(amount)
        return redirect(resp.headers['Location'])
    flash('Payment initiation failed.', 'error')
    return redirect(url_for('funds.add_funds_form'))
    # session['wallet_balance'] = session.get('wallet_balance', 0.0) + to_float(amount)
    #
    # return redirect(url_for('funds.confirmation'))


@funds_bp.route('/confirmation', methods=['GET'])
def confirmation():
    balance = session.get('wallet_balance', 0.0)
    return render_template('funds/confirmation.html',
                           new_balance=balance)

@funds_bp.route('/error', methods=['GET'])
def add_funds_error():
    flash('Payment was cancelled or failed.', 'error')
    return redirect(url_for('funds.add_funds_form'))