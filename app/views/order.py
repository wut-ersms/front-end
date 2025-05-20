from flask import render_template, Blueprint, request, jsonify
import json
from .. import socketio
import logging

logging.basicConfig(level=logging.DEBUG)

bp = Blueprint(
    "order",
    __name__,
    template_folder="templates",
    static_folder="static",
    url_prefix="/order"
)

# Dummy instrument data – później pobierzesz z mikroserwisu
INSTRUMENT_DATA = {
    "AAPL.US": {"price": 189.55, "type": "Stock", "holdings": 5},
    "NVDA.US": {"price": 915.60, "type": "Stock", "holdings": 10},
    "BTC.USD": {"price": 67000, "type": "Cryptocurrency", "holdings": 0.5},
    "SPY.US": {"price": 520.00, "type": "ETF", "holdings": 0},
    "GOLD.USD": {"price": 2400, "type": "Commodity", "holdings": 2}
}


@bp.route("/", methods=["GET"])
def index():
    return render_template("order/order.html", instrument_list=list(INSTRUMENT_DATA.keys()))


@bp.route("/get_instrument_data", methods=["POST"])
def get_instrument_data():
    data = request.get_json()
    symbol = data.get("symbol", "").upper()
    instrument = INSTRUMENT_DATA.get(symbol)

    if instrument:
        return jsonify({
            "symbol": symbol,
            "price": instrument["price"],
            "type": instrument["type"],
            "holdings": instrument["holdings"]
        })
    return jsonify({"error": "Instrument not found"}), 404


@bp.route("/submit_order", methods=["POST"])
def submit_order():
    data = request.get_json()
    # Tu można dodać logikę komunikacji z mikroserwisem zleceń
    print("Order submitted:", data)
    return jsonify({"status": "success", "message": "Order received"})