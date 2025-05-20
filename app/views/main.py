from flask import render_template, Blueprint, request, jsonify

# from ..models import Product
import json

# from ..map_utils import choose_sector_image, choose_total_image, get_free_tables_per_sector
from .. import socketio
import logging

# Ustawienie poziomu logowania na DEBUG (lub inny poziom według potrzeb)
logging.basicConfig(level=logging.DEBUG)

bp = Blueprint(
    "main",
    __name__,
    template_folder="templates",
    static_folder="static",
    url_prefix="/",
)


@bp.route("/", methods=["GET"])
def index():
    stocks = [
        {
            "name": "NVIDIA",
            "description": "High performance GPUs and AI leader.",
            "image": "images/NVIDIA_logo.jpg",
        },
        {
            "name": "Apple",
            "description": "Innovative consumer electronics and software.",
            "image": "images/Apple_logo.png",
        },
        {
            "name": "Tesla",
            "description": "Electric vehicles and clean energy.",
            "image": "images/tesla_logo.png",
        },
    ]
    return render_template("main/main.html", stocks=stocks)


@bp.route("/pedro")
def pedro():
    return render_template("main/pedro.html")


# @bp.route("/main")
# def main():
#     return render_template("main/main.html")


@bp.route("/hazard", methods=["GET"])
def hazard():
    return render_template("main/hazard.html")


# @bp.route("/transaction_history", methods=["GET", "POST"])
# def history():
#     return render_template("transaction_history/history.html")


# @bp.route("/map", methods=["GET", "POST"])
# def map():
#     return render_template("main/mapa.html", table_status=table_status)


# @bp.route("/sector1")
# def sector1():
#     sector1_status = {
#         table: info for table, info in table_status.items() if info["sector"] == 1
#     }
#     return render_template("main/sector1.html", table_status=sector1_status)


# @bp.route("/sector2")
# def sector2():
#     sector2_status = {
#         table: info for table, info in table_status.items() if info["sector"] == 2
#     }
#     return render_template("main/sector2.html", table_status=sector2_status)


# @bp.route("/get_table_status", methods=["GET"])
# def get_table_status():
#     return jsonify(table_status)


# @bp.route("/update_tables", methods=["POST"])
# def update_tables():
#     data = request.json
#     logging.debug("Received data: %s", data)  # Logowanie przy użyciu modułu logging

#     if not data or "table_number" not in data or "status" not in data:
#         logging.error("Invalid data provided")
#         return jsonify({"error": "Invalid data provided"}), 400

#     table_number = data.get("table_number")
#     status = data.get("status")

#     if table_number not in table_status:
#         logging.error("Invalid table number")
#         return jsonify({"error": "Invalid table number"}), 400

#     table_status[table_number]["status"] = status
#     logging.debug("Table status updated: %s", table_status)
#     # Aktualizacja mapy na podstawie stanu stolików
#     sector = table_status[table_number]["sector"]
#     free_tables = [
#         table_number
#         for table_number, info in table_status.items()
#         if info["status"] == "free" and info["sector"] == sector
#     ]
#     image_file = choose_sector_image(free_tables, sector)
#     logging.debug(
#         "Image file: %s", "/static/images/maps/" + image_file
#     )  # Logowanie URL obrazu

#     socketio.emit(
#         f"update_map_s{sector}", {"image_file": "/static/images/maps/" + image_file}
#     )

#     free_tables_per_sector = get_free_tables_per_sector(table_status)
#     image_file = choose_total_image(free_tables_per_sector)
#     logging.debug(
#         "Total image file: %s", "/static/images/maps/" + image_file
#     )  # Logowanie URL obrazu
#     socketio.emit("update_map", {"image_file": "/static/images/maps/" + image_file})
#     return jsonify({"success": True}), 200
