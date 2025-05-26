from flask import render_template, Blueprint, request, jsonify
import json
from .. import socketio
import logging
from flask import current_app
import requests

logging.basicConfig(level=logging.DEBUG)

bp = Blueprint(
    "desktop",
    __name__,
    template_folder="templates",
    static_folder="static",
    url_prefix="/desktop",
)


@bp.route("/", methods=["GET"])
def index():
    return render_template("desktop/desktop.html")


@bp.route("/api/portfolio", methods=["GET"])
def get_portfolio():
    # Docelowo dane będą pobierane z mikroserwisu
    data = {
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
    return jsonify(data)


@bp.route("/api/instrument_list", methods=["GET"])
def get_instruments():
    instruments = ["AAPL", "BTC", "NVDA", "GOLD"]
    return jsonify(instruments)


@bp.route("/api/chart_data/<instrument>", methods=["GET"])
def get_chart_data(instrument):
    url = f"{current_app.config['MAIN_SERVICE_URL']}/stock_data/{instrument}/1h"
    print(url)
    resp = requests.get(url, timeout=5)
    resp.raise_for_status()
    return resp.json()