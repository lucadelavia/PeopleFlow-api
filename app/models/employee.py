from datetime import datetime
from bson import ObjectId
import re
from app.common.errors import DatosInvalidos


class Employee:
    def __init__(self, nombre, apellido, email, salario, fecha_ingreso=None, puesto=None, _id=None):
        self._id = _id
        self.nombre = nombre
        self.apellido = apellido
        self.email = email
        self.puesto = puesto or "Empleado" 
        self.salario = salario
        self.fecha_ingreso = fecha_ingreso or datetime.now()
    
    def to_dict(self):
        return {
            'id': str(self._id) if self._id else None,
            'nombre': self.nombre,
            'apellido': self.apellido,
            'email': self.email,
            'puesto': self.puesto,
            'salario': self.salario,
            'fecha_ingreso': self.fecha_ingreso.strftime('%d/%m/%Y') if isinstance(self.fecha_ingreso, datetime) else self.fecha_ingreso
        }
    
    def to_mongo_dict(self):
        datos = {
            'nombre': self.nombre,
            'apellido': self.apellido,
            'email': self.email,
            'puesto': self.puesto,
            'salario': self.salario,
            'fecha_ingreso': self.fecha_ingreso
        }
        if self._id:
            datos['_id'] = self._id
        return datos
    
    @classmethod
    def from_dict(cls, datos):
        fecha_ingreso = datos.get('fecha_ingreso')
        if isinstance(fecha_ingreso, str):
            try:
                fecha_ingreso = datetime.strptime(fecha_ingreso, '%d/%m/%Y')
            except ValueError:
                raise ValueError("Formato de fecha invalido. Use dd/mm/yyyy")
        
        return cls(
            _id=datos.get('_id'),
            nombre=datos.get('nombre'),
            apellido=datos.get('apellido'),
            email=datos.get('email'),
            puesto=datos.get('puesto'),
            salario=datos.get('salario'),
            fecha_ingreso=fecha_ingreso
        )
    

    @staticmethod
    def validar_campos(datos, validacion_completa=False):
        if validacion_completa:
            if 'nombre' not in datos: raise DatosInvalidos("El nombre es obligatorio")
            if 'apellido' not in datos: raise DatosInvalidos("El apellido es obligatorio")
            if 'email' not in datos: raise DatosInvalidos("El email es obligatorio")
            if 'salario' not in datos: raise DatosInvalidos("El salario es obligatorio")
        
        if 'nombre' in datos:
            Employee.validar_nombre(datos['nombre'])
        if 'apellido' in datos:
            Employee.validar_apellido(datos['apellido'])
        if 'email' in datos:
            Employee.validar_email(datos['email'])
        if 'puesto' in datos:
            Employee.validar_puesto(datos['puesto'])
        if 'salario' in datos:
            Employee.validar_salario(datos['salario'])
        if 'fecha_ingreso' in datos:
            Employee.validar_fecha(datos['fecha_ingreso'])
    
    @staticmethod
    def validar_nombre(nombre):
        if not nombre or not nombre.strip(): raise DatosInvalidos("El nombre no puede estar vacio")
        if len(nombre.strip()) > 50: raise DatosInvalidos("El nombre no puede superar los 50 caracteres")
    
    @staticmethod
    def validar_apellido(apellido):
        if not apellido or not apellido.strip(): raise DatosInvalidos("El apellido no puede estar vacio")
        if len(apellido.strip()) > 50: raise DatosInvalidos("El apellido no puede superar los 50 caracteres")
    
    @staticmethod
    def validar_email(email):
        if not email or not email.strip(): raise DatosInvalidos("El email no puede estar vacio")
        if '@' not in email or '.' not in email: raise DatosInvalidos("El formato del email no es valido")
    
    @staticmethod
    def validar_puesto(puesto):
        if puesto and len(puesto.strip()) > 100: raise DatosInvalidos("El puesto no puede superar los 100 caracteres")
    
    @staticmethod
    def validar_salario(salario):
        if salario is None or salario == '': raise DatosInvalidos("El salario no puede estar vacio")
        try:
            if float(salario) <= 0: raise DatosInvalidos("El salario debe ser mayor a cero")
        except: raise DatosInvalidos("El salario debe ser un numero valido")
    
    @staticmethod
    def validar_fecha(fecha):
        if fecha:
            try:
                fecha_obj = datetime.strptime(fecha, '%d/%m/%Y')
                if fecha_obj.date() > datetime.now().date(): raise DatosInvalidos("La fecha de ingreso no puede ser futura")
            except: raise DatosInvalidos("La fecha debe tener formato dd/mm/yyyy")
    
