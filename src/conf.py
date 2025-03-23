import os

from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv('API_KEY')
MODEL = os.getenv('MODEL', "gpt-4o")
BASE_URL = os.getenv('BASE_URL', "https://api.openai.com/v1")
ENV = os.getenv('ENV', "localhost")
