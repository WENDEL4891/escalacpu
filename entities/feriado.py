from datetime import datetime

class Feriado:
    def __init__(self, data, tipo):
        self.data = datetime.strptime(data, '%d/%m/%Y')
        self.tipo = tipo
    
    @property
    def data(self):
        return self.data

    @property
    def tipo(self):
        return self.tipo
    
    @data.setter
    def data(self, data):
        if not isinstance(data, str):
            raise TypeError('data deve ser string.')
        try:
            self.data = datetime.strptime(data, '%d/%m/%Y')
        except ValueError:
            pass
        try:
            self.data = datetime.strptime(data, '%Y-%m-%d')
        except ValueError:
            raise ValueError('data deve ter um, dentre os dois formatos:\ndd/mm/AAAA\nou\nAAAA-mm-dd')
    
    @data.setter
    def data(self, tipo):
        if not isinstance(tipo, str):
            raise TypeError('tipo deve ser string.')
        self.tipo = tipo

