import os
import json
from dotenv import load_dotenv
from flask import session

# Load environment variables from .env file
load_dotenv()


class Config:
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    APP_SECRET_KEY = os.getenv("APP_SECRET_KEY")
    AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY")
    AWS_SECRET_KEY = os.getenv("AWS_SECRET_KEY")
    AWS_REGION = os.getenv("AWS_REGION")
    FROM_EMAIL = os.getenv("FROM_EMAIL")
    TO_EMAILS = json.loads(os.getenv("TO_EMAILS"))

    session = session
