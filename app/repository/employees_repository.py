from bson import ObjectId
from bson.errors import InvalidId
from pymongo.errors import DuplicateKeyError
from app.models.employee import Employee
from app.extensions import mongo
from app.common.errors import EmpleadoNoEncontrado, EmailYaExiste, ErrorBaseDatos


class EmployeesRepository:
    
    def __init__(self):
        self.coleccion = mongo.db.employees
    
    def crear(self, empleado):
        if not empleado or not empleado.email:
            raise ErrorBaseDatos("Empleado o email no valido")
            
        if self._email_existe(empleado.email):
            raise EmailYaExiste(empleado.email)
        
        try:
            datos_mongo = empleado.to_mongo_dict()
            resultado = self.coleccion.insert_one(datos_mongo)
            empleado._id = resultado.inserted_id
            return empleado
        except Exception as e:
            raise ErrorBaseDatos(f"Error al crear empleado: {str(e)}")
    
    def obtener_por_id(self, empleado_id):
        try:
            documento = self.coleccion.find_one({"_id": ObjectId(empleado_id)})
            
            if not documento:
                raise EmpleadoNoEncontrado(empleado_id)
            
            return Employee.from_dict(documento)
        except (InvalidId, ValueError):
            raise EmpleadoNoEncontrado(empleado_id)
    
    def obtener_todos(self, filtros=None, pagina=1, por_pagina=10):
        query = {}
        
        if filtros and 'puesto' in filtros:
            query['puesto'] = filtros['puesto']
        
        pagina = max(1, pagina)
        por_pagina = max(1, min(100, por_pagina))
        
        skip = (pagina - 1) * por_pagina
        cursor = self.coleccion.find(query).skip(skip).limit(por_pagina)
        
        return [Employee.from_dict(doc) for doc in cursor]
    
    def actualizar(self, empleado_id, datos_actualizacion):
        try:
            if 'email' in datos_actualizacion:
                if self._email_existe(datos_actualizacion['email'], excluir_id=empleado_id):
                    raise EmailYaExiste(datos_actualizacion['email'])
            
            resultado = self.coleccion.update_one(
                {"_id": ObjectId(empleado_id)},
                {"$set": datos_actualizacion}
            )
            
            if resultado.matched_count == 0:
                raise EmpleadoNoEncontrado(empleado_id)
            
            return self.obtener_por_id(empleado_id)
        except (InvalidId, ValueError):
            raise EmpleadoNoEncontrado(empleado_id)
    
    def eliminar(self, empleado_id):
        try:
            empleado = self.obtener_por_id(empleado_id)
            
            resultado = self.coleccion.delete_one({"_id": ObjectId(empleado_id)})
            
            if resultado.deleted_count == 0:
                raise EmpleadoNoEncontrado(empleado_id)
            
            return empleado
        except (InvalidId, ValueError):
            raise EmpleadoNoEncontrado(empleado_id)
    
    def contar(self, filtros=None):
        query = {}
        
        if filtros and 'puesto' in filtros:
            query['puesto'] = filtros['puesto']
        
        return self.coleccion.count_documents(query)
    
    def obtener_promedio_salarios_empresa(self):
        try:
            pipeline = [
                {"$group": {
                    "_id": None,
                    "promedio": {"$avg": "$salario"}
                }}
            ]
            
            resultado = list(self.coleccion.aggregate(pipeline))
            
            if not resultado or resultado[0]["promedio"] is None:
                return 0.0
            
            return round(resultado[0]["promedio"], 2)
        except Exception as e:
            raise ErrorBaseDatos(f"Error al calcular promedio: {str(e)}")

    def _email_existe(self, email, excluir_id=None):
        query = {"email": email.lower()}
        
        if excluir_id:
            try:
                query["_id"] = {"$ne": ObjectId(excluir_id)}
            except (InvalidId, ValueError):
                pass
        
        return self.coleccion.count_documents(query) > 0