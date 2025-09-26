import pytest
from datetime import datetime
from app.models.employee import Employee
from app.common.errors import DatosInvalidos


class TestEmployeeModel:
    
    def test_crear_empleado_datos_validos(self):
        """Verifica que se puede crear un empleado con todos los datos validos y que se asignen correctamente a las propiedades del objeto"""
        data = {
            'nombre': 'Ana',
            'apellido': 'Garcia',
            'email': 'ana.garcia@test.com',
            'puesto': 'Analista',
            'salario': 400000,
            'fecha_ingreso': '01/09/2025'
        }
        
        employee = Employee.from_dict(data)
        
        assert employee.nombre == 'Ana'
        assert employee.apellido == 'Garcia'
        assert employee.email == 'ana.garcia@test.com'
        assert employee.puesto == 'Analista'
        assert employee.salario == 400000
        assert isinstance(employee.fecha_ingreso, datetime)
    
    def test_empleado_a_diccionario(self):
        """Verifica que un objeto Employee se convierte correctamente a un diccionario con todos los campos necesarios para la API"""
        employee = Employee(
            nombre='Carlos',
            apellido='Rodriguez',
            email='carlos@test.com',
            puesto='Manager',
            salario=600000
        )
        
        result = employee.to_dict()
        
        assert result['nombre'] == 'Carlos'
        assert result['apellido'] == 'Rodriguez'
        assert result['email'] == 'carlos@test.com'
        assert result['puesto'] == 'Manager'
        assert result['salario'] == 600000
        assert 'fecha_ingreso' in result
    
    def test_validacion_campos_requeridos_exitosa(self):
        """Verifica que la validacion pasa correctamente cuando estan todos los campos obligatorios (nombre, apellido, email, salario)"""
        data = {
            'nombre': 'Maria',
            'apellido': 'Lopez',
            'email': 'maria@test.com',
            'salario': 450000
        }
        
        Employee.validar_campos(data, validacion_completa=True)
    
    def test_validacion_falla_campo_faltante(self):
        """Verifica que la validacion arroja DatosInvalidos cuando falta algun campo obligatorio en validacion completa"""
        data = {
            'nombre': 'Pedro',
            'apellido': 'Martinez'
        }
        
        with pytest.raises(DatosInvalidos) as exc_info:
            Employee.validar_campos(data, validacion_completa=True)
        
        assert 'obligatorio' in str(exc_info.value)
    
    def test_validacion_nombre_vacio(self):
        """Verifica que se rechaza un empleado cuando el campo nombre está vacío o contiene solo espacios"""
        data = {
            'nombre': '',
            'apellido': 'Gonzalez',
            'email': 'test@test.com',
            'salario': 300000
        }
        
        with pytest.raises(DatosInvalidos) as exc_info:
            Employee.validar_campos(data)
        
        assert 'nombre' in str(exc_info.value).lower()
        assert 'vacio' in str(exc_info.value)
    
    def test_validacion_nombre_muy_largo(self):
        """Verifica que se rechaza un empleado cuando el nombre excede el limite maximo de 50 caracteres"""
        data = {
            'nombre': 'a' * 51,
            'apellido': 'Test',
            'email': 'test@test.com',
            'salario': 300000
        }
        
        with pytest.raises(DatosInvalidos) as exc_info:
            Employee.validar_campos(data)
        
        assert 'nombre' in str(exc_info.value).lower()
        assert 'superar' in str(exc_info.value)
    
    def test_validacion_email_formato_invalido(self):
        """Verifica que se rechaza un empleado cuando el email no tiene un formato valido (debe contener @ y .)"""
        data = {
            'nombre': 'Test',
            'apellido': 'User',
            'email': 'email_sin_formato_valido',
            'salario': 300000
        }
        
        with pytest.raises(DatosInvalidos) as exc_info:
            Employee.validar_campos(data)
        
        assert 'email' in str(exc_info.value).lower()
    
    def test_validacion_salario_negativo(self):
        """Verifica que se rechaza un empleado cuando el salario es un valor negativo o cero"""
        data = {
            'nombre': 'Test',
            'apellido': 'User',
            'email': 'test@test.com',
            'salario': -1000
        }
        
        with pytest.raises(DatosInvalidos) as exc_info:
            Employee.validar_campos(data)
        
        assert 'salario' in str(exc_info.value).lower()
    
    def test_validacion_salario_tipo_invalido(self):
        """Verifica que se rechaza un empleado cuando el salario no es un numero valido (texto, caracteres especiales)"""
        data = {
            'nombre': 'Test',
            'apellido': 'User', 
            'email': 'test@test.com',
            'salario': 'no_es_numero'
        }
        
        with pytest.raises(DatosInvalidos) as exc_info:
            Employee.validar_campos(data)
        
        assert 'salario' in str(exc_info.value).lower()
        assert 'numero' in str(exc_info.value)
    
    def test_validacion_fecha_futura(self):
        """Verifica que se rechaza un empleado cuando la fecha de ingreso es posterior al día actual"""
        data = {
            'nombre': 'Test',
            'apellido': 'User',
            'email': 'test@test.com',
            'salario': 300000,
            'fecha_ingreso': '01/01/2030'
        }
        
        with pytest.raises(DatosInvalidos) as exc_info:
            Employee.validar_campos(data)
        
        assert 'fecha' in str(exc_info.value).lower()
    
    def test_validacion_formato_fecha_invalido(self):
        """Verifica que se rechaza un empleado cuando la fecha no cumple con el formato argentino dd/mm/yyyy"""
        data = {
            'nombre': 'Test',
            'apellido': 'User',
            'email': 'test@test.com',
            'salario': 300000,
            'fecha_ingreso': '2025-09-15'
        }
        
        with pytest.raises(DatosInvalidos) as exc_info:
            Employee.validar_campos(data)
        
        assert 'fecha' in str(exc_info.value).lower()
    
    def test_validacion_actualizacion_parcial(self):
        """Verifica que se permite validacion parcial cuando se actualiza un empleado (no todos los campos requeridos)"""
        data = {
            'nombre': 'Nuevo Nombre'
        }
        
        Employee.validar_campos(data, validacion_completa=False)