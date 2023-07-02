from .Email import Email

class CancelarMiTurno(Email):
    def __init__(self, turno):
        Email.__init__(self)
        self.fecha_solicitud = turno.fecha
        self.email_solicitud = turno.perro.responsable.email
        self.perro_solicitud = turno.perro.nombre
        self.motivo_solicitud = turno.motivo
        self.asunto = "Un turno ha sido cancelado"
        self.para_veterinaria()
        self.de_veterinaria()

    def __str__(self):
        return super().__str__()

    def enviar(self):
        email = (self.toStr() + f"El cliente con email {self.email_solicitud} ha cancelado el siguiente turno:\n"
        f"Fecha: {self.fecha_solicitud}\n"
        f"Motivo: {self.motivo_solicitud}\n"
        f"Perro: {self.perro_solicitud}\n")
        with open("emails.txt", "a") as archivo:
            archivo.write(email)
