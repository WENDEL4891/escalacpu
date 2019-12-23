from datetime import datetime
from services import functions

class Feriado:
    def __init__(self, data, tipo):
        self.data = data
        self.tipo = tipo
    
    @property
    def data(self):
        return self.__data

    @property
    def tipo(self):
        return self.__tipo
    
    @data.setter
    def data(self, data):
        self.__data = functions.date_str_to_datetime(data)
    
    @tipo.setter
    def tipo(self, tipo):
        if not isinstance(tipo, str):
            raise TypeError('O parâmetro tipo deve ser string.')
        self.__tipo = tipo
    
    def __str__(self):
        return "{0:6}: {2}\n{1:6}: {3}".format("Data", "Tipo", datetime.strftime(self.data, '%d/%m/%Y'), self.tipo)

    def __eq__(self, other_feriado):
        if other_feriado == None:
            return False
        data_eq = self.data == other_feriado.data
        tipo_eq = self.tipo == other_feriado.tipo
        return data_eq and tipo_eq
    
    def __repr__(self):
        return {
            'data': self.data,
            'tipo': self.tipo
        }
    