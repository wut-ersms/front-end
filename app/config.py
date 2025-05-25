# config.py
import os

class Config:
    MAIN_SERVICE_URL = os.environ.get("MAIN_SERVICE_URL", "http://host.docker.internal:8091")
