from flask import Blueprint, render_template, request, session, redirect, url_for, flash
import requests
import logging

logging.basicConfig(level=logging.DEBUG)

funds_bp = Blueprint(
    "funds",
    __name__,
    template_folder="templates",
    url_prefix="/funds"
)

# Base URL of the payment service
PAYMENT_SERVICE_URL = 'http://host.docker.internal:8092'

@funds_bp.route('/', methods=['GET'])
def add_funds_form():
    # Fetch available payment methods
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
    channel_id = request.form['channel']

    success_url = url_for('funds.add_funds_success', _external=True)
    error_url = url_for('funds.add_funds_error', _external=True)

    payload = {
        'amount': amount,
        'description': description,
        'email': email,
        'name': name,
        'successPage': success_url,
        'errorPage': error_url
    }
    logging.info(payload)
    resp = requests.post(f"{PAYMENT_SERVICE_URL}/transaction/new", params=payload)


    if resp.is_redirect and 'Location' in resp.headers:
        return redirect(resp.headers['Location'])
    flash('Payment initiation failed.', 'error')
    return redirect(url_for('funds.add_funds_form'))

@funds_bp.route('/success', methods=['GET'])
def add_funds_success():
    amount = request.args.get('amount', type=float)
    session['wallet_balance'] = session.get('wallet_balance', 0.0) + (amount or 0.0)
    flash(f'Successfully added {amount:.2f} PLN!', 'success')
    return redirect(url_for('funds.add_funds_form'))

@funds_bp.route('/error', methods=['GET'])
def add_funds_error():
    flash('Payment was cancelled or failed.', 'error')
    return redirect(url_for('funds.add_funds_form'))

@funds_bp.route('/ping', methods=['GET'])
def ping():
    return 'funds blueprint is active', 200