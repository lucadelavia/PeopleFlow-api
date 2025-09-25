from flask import Blueprint, request, jsonify
from datetime import datetime
from app.services.employees_service import EmployeesService
from app.common.errors import EmpleadoNoEncontrado, EmailYaExiste, DatosInvalidos, ErrorBaseDatos

employees_bp = Blueprint('employees', __name__, url_prefix='/api/empleados')
service = EmployeesService()


@employees_bp.route('', methods=['POST'])
def crear_empleado():
    """
    Crear un nuevo empleado
    Campos requeridos: nombre, apellido, email, salario
    Campos opcionales: fecha_ingreso (formato dd/mm/yyyy), puesto
    Ejemplo: POST /api/empleados
    """
    try:
        datos = request.json
        if not datos:
            return jsonify({'error': 'No se proporcionaron datos'}), 400
            
        empleado = service.crear_empleado(datos)
        
        return jsonify({
            'mensaje': 'Empleado creado exitosamente',
            'empleado': empleado.to_dict()
        }), 201
        
    except EmailYaExiste as e:
        return jsonify({
            'error': str(e)
        }), 409
        
    except (DatosInvalidos, ErrorBaseDatos) as e:
        return jsonify({
            'error': str(e)
        }), 400
    
    except Exception as e:
        return jsonify({
            'error': 'Error interno del servidor'
        }), 500


@employees_bp.route('', methods=['GET'])
def listar_empleados():
    """
    Listar empleados con paginación y filtros
    Ejemplo: GET /api/empleados?nombre=Juan&email=juan@ejemplo.com&puesto=CFO&page=1&per_page=10
    """
    try:
        try:
            pagina = int(request.args.get('page', request.args.get('pagina', 1)))
            por_pagina = int(request.args.get('per_page', request.args.get('por_pagina', 10)))
        except ValueError:
            return jsonify({'error': 'Parámetros de paginación inválidos'}), 400
            
        nombre = request.args.get('nombre')
        apellido = request.args.get('apellido') 
        email = request.args.get('email')
        puesto = request.args.get('puesto')
            
        resultado = service.listar_empleados(
            pagina=pagina,
            por_pagina=por_pagina,
            nombre=nombre,
            apellido=apellido,
            email=email,
            puesto=puesto
        )
        
        return jsonify(resultado), 200
        
    except DatosInvalidos as e:
        return jsonify({
            'error': str(e)
        }), 400
        
    except Exception as e:
        return jsonify({
            'error': 'Error interno del servidor'
        }), 500


@employees_bp.route('/<string:empleado_id>', methods=['GET'])
def obtener_empleado(empleado_id):
    """
    Obtener un empleado por ID
    Ejemplo: GET /api/empleados/507f1f77bcf86cd799439011
    """
    try:
        empleado = service.obtener_empleado(empleado_id)
        return jsonify(empleado.to_dict()), 200
        
    except EmpleadoNoEncontrado as e:
        return jsonify({
            'error': str(e)
        }), 404
        
    except Exception as e:
        return jsonify({
            'error': 'Error interno del servidor'
        }), 500


@employees_bp.route('/<string:empleado_id>', methods=['PUT'])
def actualizar_empleado(empleado_id):
    """
    Actualizar un empleado existente
    Ejemplo: PUT /api/empleados/507f1f77bcf86cd799439011
    """
    try:
        datos = request.json
        if not datos:
            return jsonify({'error': 'No se proporcionaron datos'}), 400
            
        empleado = service.actualizar_empleado(empleado_id, datos)
        
        return jsonify({
            'mensaje': 'Empleado actualizado exitosamente',
            'empleado': empleado.to_dict()
        }), 200
        
    except EmpleadoNoEncontrado as e:
        return jsonify({
            'error': str(e)
        }), 404
        
    except EmailYaExiste as e:
        return jsonify({
            'error': str(e)
        }), 409
        
    except (DatosInvalidos, ErrorBaseDatos) as e:
        return jsonify({
            'error': str(e)
        }), 400
    
    except Exception as e:
        return jsonify({
            'error': 'Error interno del servidor'
        }), 500


@employees_bp.route('/<string:empleado_id>', methods=['DELETE'])
def eliminar_empleado(empleado_id):
    """
    Eliminar un empleado
    Ejemplo: DELETE /api/empleados/507f1f77bcf86cd799439011
    """
    try:
        empleado_eliminado = service.eliminar_empleado(empleado_id)
        
        return jsonify({
            'mensaje': 'Empleado eliminado exitosamente',
            'empleado': empleado_eliminado.to_dict()
        }), 200
            
    except EmpleadoNoEncontrado as e:
        return jsonify({
            'error': str(e)
        }), 404
        
    except Exception as e:
        return jsonify({
            'error': 'Error interno del servidor'
        }), 500


@employees_bp.route('/estadisticas', methods=['GET'])
def obtener_estadisticas():
    """
    Obtener estadísticas generales de empleados
    Ejemplo: GET /api/empleados/estadisticas
    """
    try:
        estadisticas = service.obtener_estadisticas()
        return jsonify(estadisticas), 200
        
    except Exception as e:
        return jsonify({
            'error': 'Error interno del servidor'
        }), 500


@employees_bp.route('/promedio-empresa', methods=['GET'])
def promedio_salarios_empresa():
    """
    Calcular promedio de salarios de TODA LA EMPRESA
    Ejemplo: GET /api/empleados/promedio-empresa
    """
    try:
        promedio = service.calcular_promedio_salarios_empresa()
        
        return jsonify({
            'promedio_salarios': promedio,
            'descripcion': 'Promedio salarial de toda la empresa',
            'moneda': 'ARS',
            'fecha_calculo': datetime.now().strftime('%d/%m/%Y %H:%M')
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': 'Error interno del servidor'
        }), 500


@employees_bp.errorhandler(404)
def no_encontrado(error):
    return jsonify({
        'error': 'Recurso no encontrado'
    }), 404


@employees_bp.errorhandler(405)
def metodo_no_permitido(error):
    return jsonify({
        'error': 'Método no permitido'
    }), 405