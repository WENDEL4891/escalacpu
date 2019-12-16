from datetime import datetime

class Servico:
    def __init__(self, nome, data, turno):
        self.nome = nome
        self.data = datetime.strptime(data, '%d/%m/%Y').date()
        self.turno = turno        