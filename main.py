"""
Punto de entrada principal de la aplicación PeopleFlow API
Ejecutar con: python run.py
"""
import os
from app import create_app

app = create_app()

if __name__ == '__main__':

    host = os.environ.get('FLASK_HOST', '127.0.0.1')
    port = int(os.environ.get('FLASK_PORT', 5000))
    debug = os.environ.get('FLASK_DEBUG', 'True').lower() == 'true'
    
    print(f"PeopleFlow API")
    print(f"URL: http://{host}:{port}")
    print(f"Endpoints disponibles:")

    # print(f"   GET  /health          - Estado de la API")
    # print(f"   POST /api/employees   - Crear empleado")
    # print(f"   GET  /api/employees   - Listar empleados")
    # print(f"   GET  /api/employees/id - Obtener empleado")
    # print(f"   PUT  /api/employees/id - Actualizar empleado")
    # print(f"   DELETE /api/employees/id - Eliminar empleado")
    # print(f"   GET  /api/employees/salary-average - Promedio salarial")
    
    app.run(
        host=host,
        port=port,
        debug=debug
    )