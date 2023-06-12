from .Email import Email

class RechazoContacto(Email):
    def __init__(self, email):
        Email.__init__(self)
        self.email_cliente = email
        self.asunto = "Contacto del cuidador/paseador rechazado"
        self.de_veterinaria()
        self.para_cliente(email)

    def __str__(self):
        return super().__str__()

    def enviar(self):
        email = (self.toStr() + f"Lamentablemente hemos rechazado su solicitud de contacto. Puede realizar otra solicitud para intentarlo nuevamente. \n")
        with open("emails.txt", "a") as archivo:
            archivo.write(email)