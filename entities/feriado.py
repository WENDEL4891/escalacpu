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

