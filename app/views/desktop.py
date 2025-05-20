from flask import render_template, Blueprint, request, jsonify
import json
from .. import socketio
import logging

logging.basicConfig(level=logging.DEBUG)

bp = Blueprint(
    "desktop",
    __name__,
    template_folder="templates",
    static_folder="static",
    url_prefix="/desktop",
)


# Dummy data (będziesz potem podmieniał z mikroserwisu)
MOCK_PORTFOLIO = {
    "positions": [
        {
            "symbol": "AAPL.US",
            "type": "Long",
            "open_date": "2025-04-10",
            "open_price": 180.50,
            "current_price": 190.75,
            "volume": 10,
        },
        {
            "symbol": "BTC.USD",
            "type": "Short",
            "open_date": "2025-04-20",
            "open_price": 68000,
            "current_price": 67000,
            "volume": 0.2,
        },
    ],
    "summary": {
        "invested": 5000,
        "free_cash": 2000,
        "total": 7000,
        "profit": 320.50,
        "profit_pct": 4.8
    }
}

@bp.route("/", methods=["GET"])
def index():
    return render_template("desktop/desktop.html")

@bp.route("/get_portfolio_data", methods=["GET"])
def get_portfolio_data():
    return jsonify(MOCK_PORTFOLIO)