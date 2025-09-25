from datetime import datetime
from bson import ObjectId
import re


class Employee:
    def __init__(self, nombre, apellido, email, puesto, salario, fecha_ingreso=None, _id=None):
        self._id = _id
        self.nombre = nombre
        self.apellido = apellido
        self.email = email
        self.puesto = puesto
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
                fecha_ingreso = datetime.now()
        
        return cls(
            _id=datos.get('_id'),
            nombre=datos.get('nombre'),
            apellido=datos.get('apellido'),
            email=datos.get('email'),
            puesto=datos.get('puesto'),
            salario=datos.get('salario'),
            fecha_ingreso=fecha_ingreso
        )
    
    def validate(self):
        errores = []
        
        if not self.nombre or not self.nombre.strip():
            errores.append("Nombre es requerido")
        elif len(self.nombre.strip()) > 50:
            errores.append("Nombre no puede tener más de 50 caracteres")
        
        if not self.apellido or not self.apellido.strip():
            errores.append("Apellido es requerido")
        elif len(self.apellido.strip()) > 50:
            errores.append("Apellido no puede tener más de 50 caracteres")
        
        if not self.email or not self.email.strip():
            errores.append("Email es requerido")
        else:
            patron_email = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            if not re.match(patron_email, self.email.strip()):
                errores.append("Email no tiene un formato valido")
        
        if not self.puesto or not self.puesto.strip():
            errores.append("Puesto es requerido")
        elif len(self.puesto.strip()) > 100:
            errores.append("Puesto no puede tener mas de 100 caracteres")
        
        if self.salario is None:
            errores.append("Salario es requerido")
        elif not isinstance(self.salario, (int, float)):
            errores.append("Salario debe ser un número")
        elif self.salario <= 0:
            errores.append("Salario debe ser mayor a 0")
        
        if self.fecha_ingreso and isinstance(self.fecha_ingreso, datetime):
            if self.fecha_ingreso.date() > datetime.now().date():
                errores.append("Fecha de ingreso no puede ser futura")
        
        return errores
    
    def validar_email_unico(self, emails_existentes, excluir_id=None):
        if self.email and self.email.lower().strip() in [email.lower() for email in emails_existentes]:
            if excluir_id is None or self._id != excluir_id:
                return ["El email ya esta registrado"]
        return []