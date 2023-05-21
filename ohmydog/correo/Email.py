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

    def para_cliente(self, email):
        self.para= email

    def toStr(self):
        return ("-"*30 +
            f"\nDe: {self.de}\n"
            f"Para: {self.para}\n"
            f"Asunto: {self.asunto}\n"
            f"Contenido:\n"
            )
        
                
                
                

                