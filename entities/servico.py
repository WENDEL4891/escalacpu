from datetime import datetime
from dbdao import cpudao
from services import functions
import myexceptions
import config

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
        if not isinstance(nome_de_guerra, str):
            raise TypeError('O parâmetro nome_de_guerra deve receber um argumento do tipo string.')
        if not nome_de_guerra.upper() in nomes_de_guerra:
            raise ValueError('Nome de guerra não cadastrado: {}.'.format(nome_de_guerra))
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

    def get_modalidade(self):        
        if self.get_weekday() == 'segunda' and self.turno in (1, 2):
            return 'seg_12'
        if self.get_weekday() == 'segunda' and self.turno == 3:
            return 'seg_3'
        if self.get_weekday() in ('terca', 'quinta', 'sexta') and self.turno in (1, 2):
            return 'ter_qui_sex_12'
        if self.get_weekday() == 'quarta' and self.turno in (1, 2):
            return 'qua_12'
        if self.get_weekday() == 'terca' and self.turno == 3:
            return 'ter_3'
        if self.get_weekday() == 'quarta' and self.turno == 3:
            return 'qua_3'
        if self.get_weekday() == 'quinta' and self.turno == 3:
            return 'qui_3'
        if self.get_weekday() == 'sexta' and self.turno == 3:
            return 'sex_3'
        if self.get_weekday() in ('sabado', 'domingo') and self.turno in (1, 2):
            return 'fds_12'
        if self.get_weekday() == 'sabado' and self.turno == 3:
            return 'sab_3'
        if self.get_weekday() == 'domingo' and self.turno == 3:
            return 'dom_3'
        raise myexceptions.LogicException('O método Servico.get_modalidade() deve retornar alguma modalidade válida, considerando o dia da semana e o turno. Revisar função.')
    
    def get_weekday(self):
        return config.dias_da_semana[self.data.weekday()]
    
    def __str__(self):
        return\
            'Nome de guerra: ' + self.nome_de_guerra +\
            ' | Data: ' + datetime.strftime(self.data, '%d/%m/%Y') +\
            ' | Turno: ' + str(self.turno) +\
            (' | Nome estágio: ' + self.nome_estagio if self.nome_estagio != None else '')
    
    def __repr__(self):
        return {
            'nome_de_guerra': self.nome_de_guerra,
            'data': self.data,
            'turno': self.turno,
            'nome_estagio': self.nome_estagio
        }
    
    def __eq__(self, other_servico):
        if other_servico == None:
            return False
        data_eq = self.data == other_servico.data
        turno_eq = self.turno == other_servico.turno
        nome_de_guerra_eq = self.nome_de_guerra == other_servico.nome_de_guerra
        return data_eq and turno_eq and nomes_de_guerra
