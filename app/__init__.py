from flask import Flask
from flask_socketio import SocketIO

# from .config import Config
# from .views import cart, products, timer

# from .database import db

socketio = SocketIO()  # Tworzymy globalną instancję SocketIO


def create_app():
    app = Flask(__name__)
    # app.config.from_object(Config())
    # from .views import main, cart, products, start

    # db.init_app(app)

    # with app.app_context():
    #     db.create_all()
    socketio.init_app(app)

    from .views import main

    # app.register_blueprint(start.bp)
    app.register_blueprint(main.bp)
    # app.register_blueprint(cart.bp)
    # app.register_blueprint(products.bp)
    # app.register_blueprint(timer.bp)

    return app
