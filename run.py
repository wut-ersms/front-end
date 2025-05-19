# run.py or similar
from app import create_app, socketio  # Załóżmy, że twoje funkcje importujące są poprawne

app = create_app()

if __name__ == "__main__":
    socketio.run(app, host='0.0.0.0', debug=True)
