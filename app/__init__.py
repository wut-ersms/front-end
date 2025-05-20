from flask import Flask
from flask_socketio import SocketIO

# from .config import Config

socketio = SocketIO()


def create_app():
    app = Flask(__name__)
    # app.config.from_object(Config())

    socketio.init_app(app)

    from .views import main, transactions_history, order

    app.register_blueprint(main.bp)
    app.register_blueprint(transactions_history.bp)
    app.register_blueprint(order.bp)

    return app
