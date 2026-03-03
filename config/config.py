# config.py
import os

SECRET_KEY: str = os.getenv("SECRET_KEY", "fallback-secret-key")
