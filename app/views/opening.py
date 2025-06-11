from flask import render_template, Blueprint, request, jsonify, session
import json
from .. import socketio
import logging
import random

logging.basicConfig(level=logging.DEBUG)

# Define the case contents and pricing
CASE_CONTENTS = {
    "stocks": {
        "price": 9.99,
        "items": [
            {"name": "AAPL", "type": "Stock", "volume": 0.05, "open": 180, "market_value": 9.0, "prob": 0.25},
            {"name": "MSFT", "type": "Stock", "volume": 0.03, "open": 320, "market_value": 9.6, "prob": 0.20},
            {"name": "GOOGL", "type": "Stock", "volume": 0.003, "open": 2600, "market_value": 7.8, "prob": 0.15},
            {"name": "TSLA", "type": "Stock", "volume": 0.015, "open": 800, "market_value": 12.0, "prob": 0.10},
            {"name": "META", "type": "Stock", "volume": 0.02, "open": 350, "market_value": 7.0, "prob": 0.10},
            {"name": "BRK.B", "type": "Stock", "volume": 0.01, "open": 500, "market_value": 5.0, "prob": 0.05},
            {"name": "AMD", "type": "Stock", "volume": 0.05, "open": 100, "market_value": 5.0, "prob": 0.05},
            {"name": "NIO", "type": "Stock", "volume": 2, "open": 10, "market_value": 20.0, "prob": 0.04},
            {"name": "NVDA", "type": "Stock", "volume": 0.008, "open": 1200, "market_value": 9.6, "prob": 0.05},
            {"name": "AMZN", "type": "Stock", "volume": 0.01, "open": 3000, "market_value": 30.0, "prob": 0.01},
        ]
    },
    "etfs": {
        "price": 6.99,
        "items": [
            {"name": "SPY", "type": "ETF", "volume": 0.01, "open": 450, "market_value": 4.5, "prob": 0.25},
            {"name": "QQQ", "type": "ETF", "volume": 0.04, "open": 370, "market_value": 14.8, "prob": 0.20},
            {"name": "ARKK", "type": "ETF", "volume": 0.07, "open": 90, "market_value": 6.3, "prob": 0.15},
            {"name": "VTI", "type": "ETF", "volume": 0.02, "open": 250, "market_value": 5.0, "prob": 0.10},
            {"name": "DIA", "type": "ETF", "volume": 0.015, "open": 340, "market_value": 5.1, "prob": 0.10},
            {"name": "IWM", "type": "ETF", "volume": 0.04, "open": 200, "market_value": 8.0, "prob": 0.05},
            {"name": "EEM", "type": "ETF", "volume": 1.5, "open": 40, "market_value": 60.0, "prob": 0.05},
            {"name": "XLF", "type": "ETF", "volume": 0.25, "open": 35, "market_value": 8.75, "prob": 0.04},
            {"name": "XLK", "type": "ETF", "volume": 0.03, "open": 160, "market_value": 4.8, "prob": 0.05},
            {"name": "TQQQ", "type": "ETF", "volume": 0.4, "open": 200, "market_value": 80.0, "prob": 0.01},
        ]
    },
    "crypto": {
        "price": 9.99,
        "items": [
            {"name": "BTC", "type": "Crypto", "volume": 0.00015, "open": 50000, "market_value": 7.5, "prob": 0.15},
            {"name": "ETH", "type": "Crypto", "volume": 0.0015, "open": 3000, "market_value": 4.5, "prob": 0.20},
            {"name": "SOL", "type": "Crypto", "volume": 0.07, "open": 100, "market_value": 7.0, "prob": 0.10},
            {"name": "BNB", "type": "Crypto", "volume": 0.015, "open": 300, "market_value": 4.5, "prob": 0.10},
            {"name": "DOGE", "type": "Crypto", "volume": 150, "open": 0.05, "market_value": 7.5, "prob": 0.05},
            {"name": "ADA", "type": "Crypto", "volume": 40, "open": 0.25, "market_value": 10.0, "prob": 0.05},
            {"name": "XRP", "type": "Crypto", "volume": 40, "open": 0.5, "market_value": 20.0, "prob": 0.04},
            {"name": "DOT", "type": "Crypto", "volume": 2, "open": 5, "market_value": 10.0, "prob": 0.05},
            {"name": "SHIB", "type": "Crypto", "volume": 900000, "open": 0.000008, "market_value": 7.2, "prob": 0.05},
            {"name": "LTC", "type": "Crypto", "volume": 1.0, "open": 100, "market_value": 100.0, "prob": 0.01},
        ]
    }
}


bp = Blueprint(
    "opening",
    __name__,
    template_folder="templates",
    static_folder="static",
    url_prefix="/opening",
)


@bp.route("/")
def index():


    return render_template(
        "opening/opening.html"
    )


@bp.route("/open_case", methods=["POST"])
def open_case():
    data = request.get_json()
    case_type = data.get("case_type")

    if case_type not in CASE_CONTENTS:
        return jsonify({"error": "Invalid case type"}), 400

    if case_type == "etfs":
        session['wallet_balance'] = session.get('wallet_balance', 0.0) - 6.99
    else:
        session['wallet_balance'] = session.get('wallet_balance', 0.0) - 9.99

    case = CASE_CONTENTS[case_type]
    items = case["items"]
    probabilities = [item["prob"] for item in items]

    selected_item = random.choices(items, weights=probabilities, k=1)[0]
    response = {
        **selected_item,
        "wallet_balance": session['wallet_balance']
    }
    return jsonify(response)


