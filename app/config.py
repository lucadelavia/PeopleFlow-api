import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    if not SECRET_KEY:
        raise ValueError("SECRET_KEY debe estar definida en las variables de entorno")
    
    MONGO_URI = os.environ.get('MONGODB_URI')
    if not MONGO_URI:
        raise ValueError("MONGODB_URI debe estar definida en las variables de entorno")
    
    DEBUG = os.environ.get('DEBUG', 'False').lower() in ('true', '1', 'yes')
    TESTING = os.environ.get('TESTING', 'False').lower() in ('true', '1', 'yes')
    API_VERSION = os.environ.get('API_VERSION', 'v1')
    DEFAULT_PAGE_SIZE = int(os.environ.get('DEFAULT_PAGE_SIZE', '10'))
    MAX_PAGE_SIZE = int(os.environ.get('MAX_PAGE_SIZE', '100'))

    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', SECRET_KEY)
    EMPRESA_MONEDA = 'ARS'
    FECHA_FORMATO = '%d/%m/%Y'
    FECHA_HORA_FORMATO = '%d/%m/%Y %H:%M'
    