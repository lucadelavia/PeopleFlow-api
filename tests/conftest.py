import pytest
import os
from dotenv import load_dotenv
from app import create_app
from pymongo import MongoClient

load_dotenv()


@pytest.fixture
def app():
    """Crear app de Flask para testing"""
    os.environ['TESTING'] = 'True'
    app = create_app()
    app.config['TESTING'] = True
    
    main_uri = os.environ.get('MONGODB_URI')
    if not main_uri:
        raise ValueError("MONGODB_URI debe estar definida en las variables de entorno")
    
    app.config['MONGO_URI'] = main_uri
    
    return app


@pytest.fixture
def client(app):
    """Cliente de pruebas Flask"""
    return app.test_client()


@pytest.fixture
def runner(app):
    """Runner de comandos CLI"""
    return app.test_cli_runner()


@pytest.fixture(autouse=True)
def clean_db():
    """Limpiar base de datos antes y despues de cada test"""
    main_uri = os.environ.get('MONGODB_URI')
    if not main_uri:
        raise ValueError("MONGODB_URI debe estar definida en las variables de entorno")
    
    if '/' in main_uri:
        base_uri = main_uri.rsplit('/', 1)[0]
        db_name = main_uri.rsplit('/', 1)[1]
    else:
        base_uri = main_uri
        db_name = 'peopleflow'
    
    client = MongoClient(base_uri)
    db = client[db_name]
    
    # Limpiar antes del test
    db.empleados.delete_many({})
    
    yield
    
    # Limpiar despues del test
    db.empleados.delete_many({})
    client.close()


@pytest.fixture
def sample_employee_data():
    """Datos de empleado de ejemplo para tests"""
    return {
        'nombre': 'Juan',
        'apellido': 'Perez',
        'email': 'juan.perez@test.com',
        'puesto': 'Desarrollador',
        'salario': 500000,
        'fecha_ingreso': '15/09/2025'
    }


@pytest.fixture
def invalid_employee_data():
    """Datos inválidos para tests de validación"""
    return {
        'nombre': '',  # Vacío
        'apellido': 'Perez',
        'email': 'email_invalido',  # Sin formato válido
        'salario': -1000
    }