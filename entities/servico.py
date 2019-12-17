from datetime import datetime
from dbdao import cpudao
from services import functions

cpus = cpudao.CpuDAO().get_cpus()
nomes_de_guerra = [cpu_instance.nomes_de_guerra for cpu_instance in cpus]

class Servico:
    def __init__(self, nome_de_guerra, data, turno):
        self.nome_de_guerra = nome_de_guerra
        self.data = datetime.strptime(data, '%d/%m/%Y').date()
        self.turno = turno

    @property
    def nome_de_guerra(self):
        return self.__nome_de_guerra
    
    @property
    def data(self):
        return self.__data
    
    @property
    def turno(self):
        return self.__turno

    @nome_de_guerra.setter
    def nome_de_guerra(self, nome_de_guerra):
        if not nome_de_guerra in nomes_de_guerra:
            raise ValueError('Nome de guerra não cadastrado.')
        self.__nome_de_guerra = nome_de_guerra.upper()
    
    @data.setter
    def data(self, data):
        self.__data = functions.date_str_to_datetime(data)
    
    @turno.setter
    def turno(self, turno):
        if turno not in (1, 2, 3, '1', '2', '3'):
            raise ValueError('O parâmetro turno só recebe os argumentos 1, 2 ou 3.')
        self.__turno = int(turno)