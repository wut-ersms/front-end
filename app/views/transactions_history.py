from flask import render_template, Blueprint, request, jsonify
import json
from .. import socketio
import logging

logging.basicConfig(level=logging.DEBUG)

bp = Blueprint(
    "transactions_history",
    __name__,
    template_folder="templates",
    static_folder="static",
    url_prefix="/transaction_history",
)


@bp.route("/")
def index():
    transactions = [
        {
            "type": "buy",
            "volume": 10,
            "market_value": 1200.00,
            "open_price": 115.00,
            "close_price": 120.00,
            "net_profit": 50.00,
        },
        {
            "type": "sell",
            "volume": 5,
            "market_value": 600.00,
            "open_price": 125.00,
            "close_price": 115.00,
            "net_profit": -50.00,
        },
    ]

    return render_template(
        "transaction_history/history.html", transactions=transactions
    )
