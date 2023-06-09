from .Email import Email

class SolicitudContacto(Email):
    def __init__(self, email, cuidador):
        Email.__init__(self)
        self.email_solicitud = email
        self.nombre_cuidador = cuidador
        self.asunto = "Nueva solicitud de contacto con cuidador/paseador"
        self.para_veterinaria()
        self.de_veterinaria()

    def __str__(self):
        return super().__str__()

    def enviar(self):
        email = (self.toStr() + f"El cliente con email {self.email_solicitud} ha solicitado el contacto del cuidador/paseador {self.nombre_cuidador}")
        with open("emails.txt", "a") as archivo:
            archivo.write(email)