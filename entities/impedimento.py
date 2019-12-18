from datetime import datetime
from .enums import TipoImpedimentoEnum
from dbdao import cpudao
from services import functions
import myexceptions

cpus = cpudao.CpuDAO().get_cpus()      
nomes_de_guerra = [cpu_instance.nome_de_guerra for cpu_instance in cpus]
tipos = [member.value for name, member in TipoImpedimentoEnum.__members__.items()]


class Impedimento:    
    def __init__(self, nome_de_guerra, tipo, data_inicio, data_fim='', observacao=''):
        self.nome_de_guerra = nome_de_guerra
        self.tipo = tipo
        self.data_inicio = data_inicio
        self.data_fim = data_fim
        self.observacao = observacao    

    @property
    def nome_de_guerra(self):
        return self.__nome_de_guerra
    
    @property
    def tipo(self):
        return self.__tipo
    
    @property
    def data_inicio(self):
        return self.__data_inicio
    
    @property
    def data_fim(self):
        return self.__data_fim
    
    @property
    def observacao(self):
        return self.__observacao
    
    @nome_de_guerra.setter
    def nome_de_guerra(self, nome_de_guerra):
        if not isinstance(nome_de_guerra, str):
            raise TypeError('Nome de guerra deve ser do tipo string.')
        if not nome_de_guerra.upper() in nomes_de_guerra:
            raise ValueError('Nome não cadastrado.')
        self.__nome_de_guerra = nome_de_guerra.upper()
    
    @tipo.setter
    def tipo(self, tipo):
        if not isinstance(tipo, str):
            raise TypeError('Tipo deve ser do tipo string.')        
        if not tipo.upper() in tipos:
            raise ValueError('Tipo não cadastrado.')
        self.__tipo = tipo.upper()
    
    @data_inicio.setter
    def data_inicio(self, data_inicio):        
        self.__data_inicio = functions.date_str_to_datetime(data_inicio)
        
                    
    @data_fim.setter
    def data_fim(self, data_fim):
        if data_fim == '':
            self.__data_fim = self.data_inicio
            return
        data_fim_datetime = functions.date_str_to_datetime(data_fim)
        if self.data_inicio > data_fim_datetime:
            raise myexceptions.LogicException('A data de início não pode ser posterior a data fim.')
        self.__data_fim = data_fim_datetime
    
    @observacao.setter
    def observacao(self, observacao):
        if not isinstance(observacao, str):
            raise TypeError('O atributo observacao deve ser do tipo string.')        
        self.__observacao = observacao.upper()        
        
    def __repr__(self):
        return {'nome_de_guerra': self.nome_de_guerra,
                'tipo': self.tipo,
                'data_inicio': self.data_inicio,
                'data_fim': self.data_fim,
                'observacao': self.observacao}
    
    def __str__(self):
        return 'nome_de_guerra: ' + self.nome_de_guerra +\
                ' tipo: ' + self.tipo +\
                ' data_inicio: ' + datetime.strftime(self.data_inicio, '%d/%m/%Y') +\
                ' data_fim: ' + datetime.strftime(self.data_fim, '%d/%m/%Y') +\
                ' observacao: ' + self.observacao