from .Email import Email

class AprobacionContacto(Email):
    def __init__(self, email, contacto_cuidador):
        Email.__init__(self)
        self.email_cliente = email
        self.contacto_cuidador = contacto_cuidador
        self.asunto = "Contacto del cuidador/paseador solicitado"
        self.de_veterinaria()
        self.para_cliente(email)

    def __str__(self):
        return super().__str__()

    def enviar(self):
        email = (self.toStr() + f"Hemos aprobado su solicitud de contacto. El contacto del cuidador/paseador es {self.contacto_cuidador}\n")
        with open("emails.txt", "a") as archivo:
            archivo.write(email)