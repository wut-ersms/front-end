# config.py
import os

class Config:
    MAIN_SERVICE_URL = os.environ.get("MAIN_SERVICE_URL", "http://main-service:8091")
    PAYMENT_SERVICE_URL = os.environ.get("PAYMENT_SERVICE_URL", "http://payment-service:8092") # for local 'http://host.docker.internal:8092'
