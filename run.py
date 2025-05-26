# run.py or similar
from app import create_app, socketio
from dotenv import load_dotenv
import os

load_dotenv()
app = create_app()

if __name__ == "__main__":
    socketio.run(app, host=os.getenv("FLASK_RUN_HOST", "0.0.0.0") , port=os.getenv("FLASK_RUN_PORT", "5000") , debug=os.getenv("DEBUG", False))
