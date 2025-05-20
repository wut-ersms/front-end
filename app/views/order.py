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
    url_prefix="/",
)


@bp.route("/order", methods=["GET"])
def index():
    return render_template("order/order.html")
