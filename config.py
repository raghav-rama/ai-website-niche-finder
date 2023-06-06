import os
from dotenv import load_dotenv
from flask import session

# Load environment variables from .env file
load_dotenv()


class Config:
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    APP_SECRET_KEY = os.getenv("APP_SECRET_KEY")
    session = session
