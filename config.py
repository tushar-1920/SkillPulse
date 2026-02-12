# config.py
import os

class Config:
    SECRET_KEY = "skillpulse-secret-key"
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    DATA_DIR = os.path.join(BASE_DIR, "data")
