from flask import render_template, Blueprint, request, jsonify

# from ..models import Product
import json

# from ..map_utils import choose_sector_image, choose_total_image, get_free_tables_per_sector
from .. import socketio
import logging

# Ustawienie poziomu logowania na DEBUG (lub inny poziom według potrzeb)
logging.basicConfig(level=logging.DEBUG)

bp = Blueprint(
    "transactions_history",
    __name__,
    template_folder="templates",
    static_folder="static",
    url_prefix="/",
)


@bp.route("/transaction_history", methods=["POST", "GET"])
def main():
    return render_template("main/main.html")
