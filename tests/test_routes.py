import pytest
import json
from app.models.employee import Employee


class TestEmployeeRoutes:
    
    def test_crear_empleado_exitoso(self, client, sample_employee_data):
        """Verifica que se puede crear un empleado con datos validos y devuelve status 201 con los datos del empleado creado"""
        response = client.post(
            '/api/empleados',
            data=json.dumps(sample_employee_data),
            content_type='application/json'
        )
        
        assert response.status_code == 201
        data = json.loads(response.data)
        assert data['mensaje'] == 'Empleado creado exitosamente'
        assert 'empleado' in data
        assert data['empleado']['nombre'] == sample_employee_data['nombre']
        assert data['empleado']['email'] == sample_employee_data['email']
    
    def test_crear_empleado_sin_datos(self, client):
        """Verifica que se devuelve error 400 cuando se intenta crear un empleado sin proporcionar datos en el request"""
        response = client.post(
            '/api/empleados',
            data=json.dumps({}),
            content_type='application/json'
        )
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data
    
    def test_crear_empleado_datos_invalidos(self, client, invalid_employee_data):
        """Verifica que se devuelve error 400 cuando se intenta crear un empleado con datos que no pasan las validaciones"""
        response = client.post(
            '/api/empleados',
            data=json.dumps(invalid_employee_data),
            content_type='application/json'
        )
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data
        assert 'invalidos' in data['error']
    
    def test_crear_empleado_email_duplicado(self, client, sample_employee_data):
        """Verifica que se devuelve error 409 cuando se intenta crear un empleado con un email que ya existe en la base de datos"""
        client.post(
            '/api/empleados',
            data=json.dumps(sample_employee_data),
            content_type='application/json'
        )
        
        duplicate_data = sample_employee_data.copy()
        duplicate_data['nombre'] = 'Otro Nombre'
        
        response = client.post(
            '/api/empleados',
            data=json.dumps(duplicate_data),
            content_type='application/json'
        )
        
        assert response.status_code == 409
        data = json.loads(response.data)
        assert 'error' in data
        assert 'registrado' in data['error']
    
    def test_obtener_lista_empleados_vacia(self, client):
        """Verifica que se devuelve una respuesta correcta con lista vacia cuando no hay empleados registrados en la base de datos"""
        response = client.get('/api/empleados')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['empleados'] == []
        assert data['total'] == 0
        assert data['pagina'] == 1
        assert data['por_pagina'] == 10
    
    def test_obtener_lista_empleados_con_datos(self, client, sample_employee_data):
        """Verifica que se devuelve correctamente la lista de empleados cuando hay registros en la base de datos"""
        client.post(
            '/api/empleados',
            data=json.dumps(sample_employee_data),
            content_type='application/json'
        )
        
        response = client.get('/api/empleados')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert len(data['empleados']) == 1
        assert data['total'] == 1
        assert data['empleados'][0]['nombre'] == sample_employee_data['nombre']
    
    def test_paginacion_empleados(self, client):
        """Verifica que la paginacion funciona correctamente dividiendo resultados en paginas segun los parametros especificados"""
        for i in range(15):
            employee_data = {
                'nombre': f'Empleado{i}',
                'apellido': 'Test',
                'email': f'empleado{i}@test.com',
                'salario': 300000 + i * 10000
            }
            client.post(
                '/api/empleados',
                data=json.dumps(employee_data),
                content_type='application/json'
            )
        
        response = client.get('/api/empleados?pagina=1&por_pagina=10')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert len(data['empleados']) == 10
        assert data['total'] == 15
        assert data['total_paginas'] == 2
        
        # Test segunda página
        response = client.get('/api/empleados?pagina=2&por_pagina=10')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert len(data['empleados']) == 5
    
    def test_filtrar_empleados_por_nombre(self, client):
        """Verifica que se pueden filtrar empleados por nombre utilizando parametros de consulta en la URL"""
        # Crear empleados con diferentes nombres
        employees = [
            {'nombre': 'Ana', 'apellido': 'Garcia', 'email': 'ana@test.com', 'salario': 400000},
            {'nombre': 'Carlos', 'apellido': 'Lopez', 'email': 'carlos@test.com', 'salario': 500000},
            {'nombre': 'Ana', 'apellido': 'Martinez', 'email': 'ana2@test.com', 'salario': 450000}
        ]
        
        for emp in employees:
            client.post('/api/empleados', data=json.dumps(emp), content_type='application/json')
        
        response = client.get('/api/empleados?nombre=Ana')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert len(data['empleados']) == 2
        assert all(emp['nombre'] == 'Ana' for emp in data['empleados'])
    
    def test_obtener_empleado_por_id_exitoso(self, client, sample_employee_data):
        """Verifica que se puede obtener un empleado especifico utilizando su ID unico de la base de datos"""
        # Crear empleado
        create_response = client.post(
            '/api/empleados',
            data=json.dumps(sample_employee_data),
            content_type='application/json'
        )
        create_data = json.loads(create_response.data)
        employee_id = create_data['empleado']['id']
        
        # Obtener empleado por ID
        response = client.get(f'/api/empleados/{employee_id}')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['nombre'] == sample_employee_data['nombre']
        assert data['email'] == sample_employee_data['email']
    
    def test_obtener_empleado_id_inexistente(self, client):
        """Verifica que se devuelve error 404 cuando se intenta obtener un empleado con un ID que no existe"""
        fake_id = '507f1f77bcf86cd799439011'
        response = client.get(f'/api/empleados/{fake_id}')
        
        assert response.status_code == 404
        data = json.loads(response.data)
        assert 'error' in data
        assert 'no encontrado' in data['error']
    
    def test_actualizar_empleado_exitoso(self, client, sample_employee_data):
        """Verifica que se puede actualizar parcialmente los datos de un empleado existente y devuelve los datos actualizados"""
        create_response = client.post(
            '/api/empleados',
            data=json.dumps(sample_employee_data),
            content_type='application/json'
        )
        create_data = json.loads(create_response.data)
        employee_id = create_data['empleado']['id']
        
        update_data = {'nombre': 'Nombre Actualizado', 'salario': 600000}
        response = client.put(
            f'/api/empleados/{employee_id}',
            data=json.dumps(update_data),
            content_type='application/json'
        )
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['mensaje'] == 'Empleado actualizado exitosamente'
        assert data['empleado']['nombre'] == 'Nombre Actualizado'
        assert data['empleado']['salario'] == 600000
    
    def test_actualizar_empleado_inexistente(self, client):
        """Verifica que se devuelve error 404 cuando se intenta actualizar un empleado que no existe en la base de datos"""
        fake_id = '507f1f77bcf86cd799439011'
        update_data = {'nombre': 'Nuevo Nombre'}
        
        response = client.put(
            f'/api/empleados/{fake_id}',
            data=json.dumps(update_data),
            content_type='application/json'
        )
        
        assert response.status_code == 404
        data = json.loads(response.data)
        assert 'error' in data
    
    def test_actualizar_empleado_email_duplicado(self, client):
        """Verifica que se devuelve error 409 cuando se intenta actualizar un empleado con un email que ya usa otro empleado"""
        # Crear dos empleados
        emp1_data = {'nombre': 'Ana', 'apellido': 'Garcia', 'email': 'ana@test.com', 'salario': 400000}
        emp2_data = {'nombre': 'Carlos', 'apellido': 'Lopez', 'email': 'carlos@test.com', 'salario': 500000}
        
        client.post('/api/empleados', data=json.dumps(emp1_data), content_type='application/json')
        create_response = client.post('/api/empleados', data=json.dumps(emp2_data), content_type='application/json')
        
        emp2_id = json.loads(create_response.data)['empleado']['id']
        
        # Intentar actualizar segundo empleado con email del primero
        response = client.put(
            f'/api/empleados/{emp2_id}',
            data=json.dumps({'email': 'ana@test.com'}),
            content_type='application/json'
        )
        
        assert response.status_code == 409
        data = json.loads(response.data)
        assert 'registrado' in data['error']
    
    def test_eliminar_empleado_exitoso(self, client, sample_employee_data):
        """Verifica que se puede eliminar un empleado existente y que desaparece completamente de la base de datos"""
        # Crear empleado
        create_response = client.post(
            '/api/empleados',
            data=json.dumps(sample_employee_data),
            content_type='application/json'
        )
        create_data = json.loads(create_response.data)
        employee_id = create_data['empleado']['id']
        
        # Eliminar empleado
        response = client.delete(f'/api/empleados/{employee_id}')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['mensaje'] == 'Empleado eliminado exitosamente'
        
        # Verificar que fue eliminado
        get_response = client.get(f'/api/empleados/{employee_id}')
        assert get_response.status_code == 404
    
    def test_eliminar_empleado_inexistente(self, client):
        """Verifica que se devuelve error 404 cuando se intenta eliminar un empleado que no existe"""
        fake_id = '507f1f77bcf86cd799439011'
        response = client.delete(f'/api/empleados/{fake_id}')
        
        assert response.status_code == 404
        data = json.loads(response.data)
        assert 'error' in data
    
    def test_obtener_promedio_salarios(self, client):
        """Verifica que se calcula correctamente el promedio de salarios de todos los empleados de la empresa"""
        # Crear empleados con diferentes salarios
        employees = [
            {'nombre': 'Ana', 'apellido': 'Garcia', 'email': 'ana@test.com', 'salario': 400000},
            {'nombre': 'Carlos', 'apellido': 'Lopez', 'email': 'carlos@test.com', 'salario': 600000},
            {'nombre': 'Maria', 'apellido': 'Martinez', 'email': 'maria@test.com', 'salario': 500000}
        ]
        
        for emp in employees:
            client.post('/api/empleados', data=json.dumps(emp), content_type='application/json')
        
        response = client.get('/api/empleados/promedio-empresa')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'promedio_salarios' in data
        assert data['promedio_salarios'] == 500000.0  # (400k + 600k + 500k) / 3
        assert data['moneda'] == 'ARS'
    
    def test_promedio_salarios_sin_empleados(self, client):
        """Verifica que se devuelve promedio 0 cuando no hay empleados registrados en la empresa"""
        response = client.get('/api/empleados/promedio-empresa')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['promedio_salarios'] == 0
    
    def test_obtener_estadisticas_empleados(self, client):
        """Verifica que se calculan correctamente las estadisticas de la empresa incluyendo total de empleados, promedio salarial y metadatos"""
        employees = [
            {'nombre': 'Ana', 'apellido': 'Garcia', 'email': 'ana@test.com', 'salario': 300000},
            {'nombre': 'Carlos', 'apellido': 'Lopez', 'email': 'carlos@test.com', 'salario': 700000},
            {'nombre': 'Maria', 'apellido': 'Martinez', 'email': 'maria@test.com', 'salario': 500000}
        ]
        
        for emp in employees:
            client.post('/api/empleados', data=json.dumps(emp), content_type='application/json')
        
        response = client.get('/api/empleados/estadisticas')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['total_empleados'] == 3
        assert data['promedio_salarios'] == 500000.0
        assert data['moneda'] == 'ARS'
        assert 'fecha_reporte' in data