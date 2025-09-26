import pytest
import json
from app.models.employee import Employee


class TestIntegration:
    
    def test_ciclo_vida_completo_empleado(self, client, sample_employee_data):
        """Verifica el flujo completo de operaciones CRUD de un empleado: crear, listar, obtener, actualizar y eliminar"""
        create_response = client.post(
            '/api/empleados',
            data=json.dumps(sample_employee_data),
            content_type='application/json'
        )
        assert create_response.status_code == 201
        
        create_data = json.loads(create_response.data)
        employee_id = create_data['empleado']['id']
        
        list_response = client.get('/api/empleados')
        assert list_response.status_code == 200
        list_data = json.loads(list_response.data)
        assert list_data['total'] == 1
        assert list_data['empleados'][0]['id'] == employee_id
        
        get_response = client.get(f'/api/empleados/{employee_id}')
        assert get_response.status_code == 200
        get_data = json.loads(get_response.data)
        assert get_data['nombre'] == sample_employee_data['nombre']
        
        # 4. Actualizar empleado
        update_data = {'salario': 550000, 'apellido': 'Apellido Actualizado'}
        update_response = client.put(
            f'/api/empleados/{employee_id}',
            data=json.dumps(update_data),
            content_type='application/json'
        )
        assert update_response.status_code == 200
        
        # 5. Verificar actualización
        get_updated_response = client.get(f'/api/empleados/{employee_id}')
        updated_data = json.loads(get_updated_response.data)
        assert updated_data['salario'] == 550000
        assert updated_data['apellido'] == 'Apellido Actualizado'
        
        # 6. Eliminar empleado
        delete_response = client.delete(f'/api/empleados/{employee_id}')
        assert delete_response.status_code == 200
        
        get_deleted_response = client.get(f'/api/empleados/{employee_id}')
        assert get_deleted_response.status_code == 404
        
        final_list_response = client.get('/api/empleados')
        final_data = json.loads(final_list_response.data)
        assert final_data['total'] == 0
    
    def test_operaciones_multiples_empleados(self, client):
        """Verifica que se pueden realizar operaciones complejas con multiples empleados incluyendo filtros, estadisticas y actualizaciones"""
        employees_data = [
            {'nombre': 'Ana', 'apellido': 'Garcia', 'email': 'ana@test.com', 'salario': 400000},
            {'nombre': 'Carlos', 'apellido': 'Lopez', 'email': 'carlos@test.com', 'salario': 500000},
            {'nombre': 'Maria', 'apellido': 'Martinez', 'email': 'maria@test.com', 'salario': 600000}
        ]
        
        created_ids = []
        
        for emp_data in employees_data:
            response = client.post(
                '/api/empleados',
                data=json.dumps(emp_data),
                content_type='application/json'
            )
            assert response.status_code == 201
            created_ids.append(json.loads(response.data)['empleado']['id'])
        
        list_response = client.get('/api/empleados')
        list_data = json.loads(list_response.data)
        assert list_data['total'] == 3
        
        # Verificar estadísticas
        stats_response = client.get('/api/empleados/estadisticas')
        stats_data = json.loads(stats_response.data)
        assert stats_data['total_empleados'] == 3
        assert stats_data['promedio_salarios'] == 500000.0
        
        # Filtrar por nombre
        filter_response = client.get('/api/empleados?nombre=Ana')
        filter_data = json.loads(filter_response.data)
        assert len(filter_data['empleados']) == 1
        assert filter_data['empleados'][0]['nombre'] == 'Ana'
        
        # Actualizar salario de uno
        update_response = client.put(
            f'/api/empleados/{created_ids[1]}',
            data=json.dumps({'salario': 700000}),
            content_type='application/json'
        )
        assert update_response.status_code == 200
        
        # Verificar cambios en estadísticas
        new_stats_response = client.get('/api/empleados/estadisticas')
        new_stats_data = json.loads(new_stats_response.data)
        assert new_stats_data['promedio_salarios'] == 566666.67
    
    def test_manejo_errores_flujo_completo(self, client):
        """Verifica que todos los tipos de errores se manejan correctamente en diferentes escenarios (datos invalidos, duplicados, inexistentes)"""
        # Intentar obtener empleado inexistente
        response = client.get('/api/empleados/507f1f77bcf86cd799439011')
        assert response.status_code == 404
        
        # Crear empleado con datos inválidos
        invalid_data = {'nombre': '', 'email': 'invalid-email'}
        response = client.post(
            '/api/empleados',
            data=json.dumps(invalid_data),
            content_type='application/json'
        )
        assert response.status_code == 400
        
        # Crear empleado válido
        valid_data = {
            'nombre': 'Test',
            'apellido': 'User',
            'email': 'test@example.com',
            'salario': 400000
        }
        create_response = client.post(
            '/api/empleados',
            data=json.dumps(valid_data),
            content_type='application/json'
        )
        assert create_response.status_code == 201
        employee_id = json.loads(create_response.data)['empleado']['id']
        
        # Intentar crear otro con mismo email
        duplicate_response = client.post(
            '/api/empleados',
            data=json.dumps(valid_data),
            content_type='application/json'
        )
        assert duplicate_response.status_code == 409
        
        # Intentar actualizar con datos inválidos
        invalid_update = {'salario': -1000}
        update_response = client.put(
            f'/api/empleados/{employee_id}',
            data=json.dumps(invalid_update),
            content_type='application/json'
        )
        assert update_response.status_code == 400
        
        # Intentar actualizar empleado inexistente
        update_nonexistent = client.put(
            '/api/empleados/507f1f77bcf86cd799439011',
            data=json.dumps({'nombre': 'Test'}),
            content_type='application/json'
        )
        assert update_nonexistent.status_code == 404
        
        # Intentar eliminar empleado inexistente
        delete_nonexistent = client.delete('/api/empleados/507f1f77bcf86cd799439011')
        assert delete_nonexistent.status_code == 404
    
    def test_integracion_estadisticas_tiempo_real(self, client):
        """Verifica que las estadisticas se actualizan correctamente en tiempo real cuando se agregan, modifican o eliminan empleados"""
        # Estado inicial - sin empleados
        stats_response = client.get('/api/empleados/estadisticas')
        stats_data = json.loads(stats_response.data)
        assert stats_data['total_empleados'] == 0
        
        # Agregar primer empleado
        emp1_data = {'nombre': 'Ana', 'apellido': 'Garcia', 'email': 'ana@test.com', 'salario': 400000}
        create1_response = client.post('/api/empleados', data=json.dumps(emp1_data), content_type='application/json')
        emp1_id = json.loads(create1_response.data)['empleado']['id']
        
        stats_response = client.get('/api/empleados/estadisticas')
        stats_data = json.loads(stats_response.data)
        assert stats_data['total_empleados'] == 1
        assert stats_data['promedio_salarios'] == 400000.0
        
        # Agregar segundo empleado
        emp2_data = {'nombre': 'Carlos', 'apellido': 'Lopez', 'email': 'carlos@test.com', 'salario': 600000}
        client.post('/api/empleados', data=json.dumps(emp2_data), content_type='application/json')
        
        stats_response = client.get('/api/empleados/estadisticas')
        stats_data = json.loads(stats_response.data)
        assert stats_data['total_empleados'] == 2
        assert stats_data['promedio_salarios'] == 500000.0
        
        # Actualizar salario del primer empleado
        client.put(f'/api/empleados/{emp1_id}', data=json.dumps({'salario': 500000}), content_type='application/json')
        
        stats_response = client.get('/api/empleados/estadisticas')
        stats_data = json.loads(stats_response.data)
        assert stats_data['promedio_salarios'] == 550000.0
        
        # Eliminar un empleado
        client.delete(f'/api/empleados/{emp1_id}')
        
        stats_response = client.get('/api/empleados/estadisticas')
        stats_data = json.loads(stats_response.data)
        assert stats_data['total_empleados'] == 1
        assert stats_data['promedio_salarios'] == 600000.0