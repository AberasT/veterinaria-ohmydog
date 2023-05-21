from .Email import Email

class SolicitudTurno(Email):
    def __init__(self, fecha, email, perro, motivo, detalles):
        Email.__init__(self)
        self.fecha_solicitud = fecha
        self.email_solicitud = email
        self.perro_solicitud = perro
        self.motivo_solicitud = motivo
        self.detalles_solicitud = detalles
        self.asunto = "Nueva solicitud de turno"
        self.para_veterinaria()
        self.de_veterinaria()

    def __str__(self):
        return super().__str__()

    def enviar(self):
        email = (self.toStr() + f"El cliente con email {self.email_solicitud} ha solicitado un turno:\n"
        f"Fecha: {self.fecha_solicitud}\n"
        f"Motivo: {self.motivo_solicitud}\n"
        f"Perro: {self.perro_solicitud}\n"
        f"Detalles: {self.detalles_solicitud}\n")
        with open("emails.txt", "a") as archivo:
            archivo.write(email)

class AsignacionTurno(Email):
    def __init__(self, fecha, hora, email):
        Email.__init__(self)
        self.fecha_asignacion = fecha
        self.email_asignacion = email
        self.hora_asignacion = hora
        self.asunto = "Turno confirmado"
        self.para_cliente(email)
        self.de_veterinaria()

    def __str__(self):
        return super().__str__()

    def enviar(self):
        email = (self.toStr() + f"Se confirmó su turno con los siguientes datos: \n"
        f"Fecha: {self.fecha_asignacion}\n"
        f"Hora: {self.hora_asignacion}\n")
        with open("emails.txt", "a") as archivo:
            archivo.write(email)
