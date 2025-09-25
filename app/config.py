import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    MONGO_URI = os.environ.get('MONGODB_URI')
    DEBUG = True
    DEFAULT_PAGE_SIZE = 10
    MAX_PAGE_SIZE = 100