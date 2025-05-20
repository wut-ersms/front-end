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
    instruments = ["AAPL.US", "BTC.USD", "NVDA.US", "GOLD.USD"]
    return jsonify(instruments)


@bp.route("/api/chart_data/<instrument>", methods=["GET"])
def get_chart_data(instrument):
    labels = [
        "2024-05-10", "2024-05-11", "2024-05-12", "2024-05-13", "2024-05-14",
        "2024-05-15", "2024-05-16", "2024-05-17", "2024-05-18", "2024-05-19"
    ]
    prices = [100, 101, 102, 101.5, 103, 104, 103.5, 105, 106, 107]

    macd_line = [0.5, 0.7, 0.4, 0.6, 0.9, 1.0, 1.1, 1.0, 0.8, 0.9]
    signal_line = [0.4, 0.5, 0.45, 0.5, 0.6, 0.85, 1.0, 0.95, 0.75, 0.85]
    histogram = [m - s for m, s in zip(macd_line, signal_line)]

    volume = [1000, 1500, 1700, 1300, 2100, 2000, 2500, 2200, 2600, 2400]

    return jsonify({
        "labels": labels,
        "price": prices,
        "macd_line": macd_line,
        "signal_line": signal_line,
        "histogram": histogram,
        "volume": volume
    })