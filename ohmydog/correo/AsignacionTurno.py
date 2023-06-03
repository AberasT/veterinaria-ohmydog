from .Email import Email

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
