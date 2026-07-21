"""
config.py
---------
Central configuration for the Farmer Consumer Interaction (FCI) Flask app.
Update the DB_* values below to match your local MySQL setup.
"""

import os

# ---- Flask ----
SECRET_KEY = "change-this-secret-key-in-production"

# ---- MySQL connection settings ----
DB_HOST = os.environ.get("FCI_DB_HOST", "localhost")
DB_PORT = int(os.environ.get("FCI_DB_PORT", 3306))
DB_USER = os.environ.get("FCI_DB_USER", "root")
DB_PASSWORD = os.environ.get("FCI_DB_PASSWORD", "MYsql@123")   # <-- change to your MySQL password
DB_NAME = os.environ.get("FCI_DB_NAME", "farmer_consumer")

# ---- File uploads ----
UPLOAD_FOLDER = os.path.join("static", "images")
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "webp"}
MAX_CONTENT_LENGTH = 5 * 1024 * 1024  # 5 MB
