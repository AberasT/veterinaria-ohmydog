class Email:
    def __init__(self, de="de", para="para"):
        self.asunto = "asunto"
        self.para = para
        self.de = de
        self.contenido = "contenido"

    def de_veterinaria(self):
        self.de = "ohmydog@mail.com"

    def para_veterinaria(self):
        self.para = "ohmydog@mail.com"

    def toStr(self):
        return f"""
                -------------------------------------------------------
                De: {self.de}
                Para: {self.para}
                Asunto: {self.asunto}

                Contenido:
                """