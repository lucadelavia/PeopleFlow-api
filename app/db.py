import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

def get_database():
    main_uri = os.environ.get('MONGODB_URI')
    if not main_uri:
        raise ValueError("MONGODB_URI debe estar definida en las variables de entorno")
    
    client = MongoClient(main_uri)
    db_name = main_uri.split('/')[-1] if '/' in main_uri else 'peopleflow'
    return client[db_name]