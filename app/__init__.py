from flask import Flask, session
from flask_socketio import SocketIO
from flask_dance.contrib.google import make_google_blueprint, google
from .config import Config
import os

# from .config import Config

socketio = SocketIO()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config())
    app.secret_key = "twoj_super_tajny_klucz"

    socketio.init_app(app)

    google_bp = make_google_blueprint(
        client_id=os.environ.get("GOOGLE_OAUTH_CLIENT_ID"),
        client_secret=os.environ.get("GOOGLE_OAUTH_CLIENT_SECRET"),
        scope=[
            "openid",
            "https://www.googleapis.com/auth/userinfo.email",
            "https://www.googleapis.com/auth/userinfo.profile",
        ],
        redirect_to="auth.google_login",
    )
    app.register_blueprint(google_bp)

    from .views import main, transactions_history, order, desktop, auth, opening, funds

    app.register_blueprint(main.bp)
    app.register_blueprint(transactions_history.bp)
    app.register_blueprint(order.bp)
    app.register_blueprint(desktop.bp)
    app.register_blueprint(auth.bp)
    app.register_blueprint(opening.bp)
    app.register_blueprint(funds.funds_bp)

    @app.context_processor
    def inject_user():
        # return {
        #     "user_logged_in": session.get("logged_in", False),
        #     "username": session.get("username", None),
        # }
        user = session.get("user")
        return {
            "user_logged_in": session.get("logged_in", False),
            "username": user["name"] if user else session.get("username"),
            "user_email": user["email"] if user else None,
            "user_picture": user["picture"] if user else None,
             "wallet_balance": session.get("wallet_balance", 0.0),
            "last_amount_added": session.get("last_amount_added", 0.0)
        }

    return app
