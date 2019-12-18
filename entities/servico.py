from datetime import datetime
from dbdao import cpudao
from services import functions
import myexceptions

cpus = cpudao.CpuDAO().get_cpus()
nomes_de_guerra = [cpu_instance.nome_de_guerra for cpu_instance in cpus]

class Servico:
    def __init__(self, nome_de_guerra, data, turno, nome_estagio=None):
        self.nome_de_guerra = nome_de_guerra
        self.data = data
        self.turno = turno
        self.nome_estagio = nome_estagio

    @property
    def nome_de_guerra(self):
        return self.__nome_de_guerra
    
    @property
    def data(self):
        return self.__data
    
    @property
    def turno(self):
        return self.__turno
    
    @property
    def nome_estagio(self):
        return self.__nome_estagio

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
    
    @nome_estagio.setter
    def nome_estagio(self, nome_estagio):
        if nome_estagio == None:
            self.__nome_estagio = None
        else:            
            if not isinstance(nome_estagio, str):
                raise TypeError('O parâmetro nome_estagio dever receber um argumento do tipo string.')
            if len(nome_estagio):
                self.__nome_estagio = nome_estagio.upper()
            else:                
                self.__nome_estagio = None
    
    def __str__(self):
        return\
            'Nome de guerra: ' + self.nome_de_guerra +\
            ' | Data: ' + datetime.strftime(self.data, '%d/%m/%Y') +\
            ' | Turno: ' + str(self.turno) +\
            ' | Nome estágio: ' + self.nome_estagio\
                if self.nome_estagio != None\
                else\
            'Nome de guerra: ' + self.nome_de_guerra +\
            ' | Data: ' + datetime.strftime(self.data, '%d/%m/%Y') +\
            ' | Turno: ' + str(self.turno)