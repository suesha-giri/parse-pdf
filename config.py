import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # media storage
    UPLOAD_FOLDER = os.getenv("UPLOAD_FOLDER", "uploads")
    RESULT_FOLDER = os.getenv("RESULT_FOLDER", "results")

    # database
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "postgresql+pg8000://user:password@db:5432/pdf_db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # celery
    broker_url = os.getenv("broker_url", "redis://redis:6379/0")
    result_backend = os.getenv("result_backend", "redis://redis:6379/0")
    include = ('tasks',)

