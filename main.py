import os
from dotenv import load_dotenv
from app import create_app

load_dotenv()
app = create_app()

if __name__ == '__main__':
    debug_mode = os.getenv('DEBUG', 'True').lower() == 'true'
    port = int(os.getenv('PORT', 5000))
    host = os.getenv('HOST', '127.0.0.1')
    
    print("PeopleFlow API")
    print(f"URL: http://{host}:{port}")
    print("\nEndpoints:")
    print(f"   POST   /api/empleados")
    print(f"   GET    /api/empleados")
    print(f"   GET    /api/empleados/{{id}}")
    print(f"   PUT    /api/empleados/{{id}}")
    print(f"   DELETE /api/empleados/{{id}}")
    print(f"   GET    /api/empleados/promedio-empresa")
    print("-" * 40)
    
    app.run(host=host, port=port, debug=debug_mode)