from flask import Flask, session
from flask_socketio import SocketIO

# from .config import Config

socketio = SocketIO()


def create_app():
    app = Flask(__name__)
    # app.config.from_object(Config())
    app.secret_key = "twoj_super_tajny_klucz"

    socketio.init_app(app)

    from .views import main, transactions_history, order, desktop, auth

    app.register_blueprint(main.bp)
    app.register_blueprint(transactions_history.bp)
    app.register_blueprint(order.bp)
    app.register_blueprint(desktop.bp)
    app.register_blueprint(auth.bp)

    @app.context_processor
    def inject_user():
        return {
            "user_logged_in": session.get("logged_in", False),
            "username": session.get("username", None),
        }

    return app
