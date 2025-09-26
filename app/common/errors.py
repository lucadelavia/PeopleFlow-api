class EmployeeError(Exception):
    def __init__(self, mensaje, codigo_estado=400):
        self.mensaje = mensaje
        self.codigo_estado = codigo_estado
        super().__init__(self.mensaje)


class EmpleadoNoEncontrado(EmployeeError):
    def __init__(self, empleado_id):
        mensaje = f"Empleado con ID {empleado_id} no encontrado"
        super().__init__(mensaje, 404)


class EmailYaExiste(EmployeeError):
    def __init__(self, email):
        mensaje = f"El email {email} ya esta registrado"
        super().__init__(mensaje, 400)


class DatosInvalidos(EmployeeError):
    def __init__(self, errores):
        if isinstance(errores, list):
            mensaje = "; ".join(errores)
        else:
            mensaje = str(errores)
        super().__init__(f"Datos invalidos: {mensaje}", 400)


class ErrorBaseDatos(EmployeeError):
    def __init__(self, mensaje_original):
        mensaje = f"Error en la base de datos: {mensaje_original}"
        super().__init__(mensaje, 500)


class ErrorConexion(EmployeeError):
    def __init__(self):
        mensaje = "Error de conexión con la base de datos"
        super().__init__(mensaje, 503)


class CamposRequeridos(EmployeeError):
    def __init__(self, campos_faltantes):
        if isinstance(campos_faltantes, list):
            campos = ", ".join(campos_faltantes)
        else:
            campos = str(campos_faltantes)
        mensaje = f"Campos requeridos faltantes: {campos}"
        super().__init__(mensaje, 400)