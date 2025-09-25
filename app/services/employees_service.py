from app.repository.employees_repository import EmployeesRepository
from app.models.employee import Employee
from app.common.errors import DatosInvalidos, EmpleadoNoEncontrado
from datetime import datetime


class EmployeesService:
    
    def __init__(self):
        self.repo = EmployeesRepository()
    
    def crear_empleado(self, datos_request):
        empleado = Employee.from_dict(datos_request)
        
        errores_modelo = empleado.validate()
        if errores_modelo:
            raise DatosInvalidos(errores_modelo)
        
        return self.repo.crear(empleado)
    
    def obtener_empleado(self, empleado_id):
        empleado = self.repo.obtener_por_id(empleado_id)
        if not empleado:
            raise EmpleadoNoEncontrado(empleado_id)
        return empleado
    
    def listar_empleados(self, filtros=None, pagina=1, por_pagina=10):
        pagina = max(int(pagina), 1)
        por_pagina = max(min(int(por_pagina), 100), 1)
        
        empleados = self.repo.obtener_todos(filtros, pagina, por_pagina)
        total = self.repo.contar(filtros)
        
        return {
            'empleados': [empleado.to_dict() for empleado in empleados],
            'total': total,
            'pagina': pagina,
            'por_pagina': por_pagina,
            'total_paginas': (total + por_pagina - 1) // por_pagina
        }
    
    def actualizar_empleado(self, empleado_id, datos_request):
        if 'fecha_ingreso' in datos_request and isinstance(datos_request['fecha_ingreso'], str):
            try:
                datos_request['fecha_ingreso'] = datetime.strptime(datos_request['fecha_ingreso'], '%d/%m/%Y')
            except ValueError:
                raise DatosInvalidos("Formato de fecha invalido. Use dd/mm/yyyy")
        
        return self.repo.actualizar(empleado_id, datos_request)
    
    def eliminar_empleado(self, empleado_id):
        resultado = self.repo.eliminar(empleado_id)
        return {"eliminado": bool(resultado)}
    
    def obtener_estadisticas(self):
        total_empleados = self.repo.contar()
        promedio_salarios = self.calcular_promedio_salarios_empresa()
        
        return {
            'total_empleados': total_empleados,
            'promedio_salarios': promedio_salarios,
            'fecha_reporte': datetime.now().strftime('%d/%m/%Y %H:%M')
        }
    
    def calcular_promedio_salarios_empresa(self):
        try:
            promedio = self.repo.obtener_promedio_salarios_empresa()
            return round(promedio, 2) if promedio else 0.0
        except Exception as e:
            print(f"Error al calcular promedio: {e}")
            return 0.0
    
