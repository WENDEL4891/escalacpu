import datetime
from dbdao import cpudao
from services import functions
import myexceptions
import config
from entities import cpu


class Servico:
    cpus = cpudao.CpuDAO().get_cpus()
    nomes_de_guerra = list(map(lambda _cpu: _cpu.nome_de_guerra, cpus))

    def __init__(self, data, turno, _cpu='DEFAULT', nome_estagio=None):
        self.data = data
        self.turno = turno
        self.cpu = _cpu
        self.nome_estagio = nome_estagio
    
    @property
    def data(self):
        return self.__data
    
    @property
    def turno(self):
        return self.__turno

    @property
    def cpu(self):
        return self.__cpu
    
    @property
    def nome_estagio(self):
        return self.__nome_estagio

    
    @data.setter
    def data(self, data):
        if isinstance(data, datetime.datetime):
            self.__data = data.date()
        elif isinstance(data, datetime.date):
            self.__data = data            
        else:
            self.__data = functions.date_str_to_datetime(data)
    
    @turno.setter
    def turno(self, turno):
        if turno not in (1, 2, 3, '1', '2', '3'):
            raise ValueError('O parâmetro turno só recebe os argumentos 1, 2 ou 3.')
        self.__turno = int(turno)
    
    @cpu.setter
    def cpu(self, _cpu):
        if isinstance(_cpu, cpu.Cpu):            
            self.__cpu = _cpu
        elif isinstance(_cpu, str):
            if _cpu.upper() == 'CPU_NONE':
                self.__cpu = None
            elif _cpu.upper() in self.nomes_de_guerra:
                self.__cpu = cpudao.CpuDAO().get_cpu(_cpu.upper())
            else:
                raise ValueError('Nome de guerra não cadastrado: {}.'.format(_cpu.upper()))
        else:    
            raise TypeError("O parâmetro _cpu deve receber um argumento do tipo string ou um objeto da classe cpu.Cpu. Foi passado {}".format(str(type(_cpu))))
        
    
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
        sem_12 = ('seg', 'ter', 'qua', 'qui', 'sex')
        sem_2 = ('seg', 'ter', 'qui')
        if ( self.get_weekday() in sem_12 and self.turno == 1 ) or ( self.get_weekday() in sem_2 and self.turno == 2 ):
            return 'sem_12'        
        if self.get_weekday() in ('seg', 'ter', 'qua') and self.turno == 3:
            return 'sem_3'
        if self.get_weekday() == 'qua' and self.turno == 2:
            return 'qua_2'
        if self.get_weekday() == 'qui' and self.turno == 3:
            return 'qui_3'
        if self.get_weekday() == 'sex' and self.turno == 2:
            return 'sex_2'
        if self.get_weekday() == 'sex' and self.turno == 3:
            return 'sex_3'
        if self.get_weekday() in ('sab', 'dom') and self.turno in (1, 2):
            return 'fds_12'
        if self.get_weekday() == 'sab' and self.turno == 3:
            return 'sab_3'
        if self.get_weekday() == 'dom' and self.turno == 3:
            return 'dom_3'
        raise myexceptions.LogicException('O método Servico.get_modalidade() deve retornar alguma modalidade válida, considerando o dia da semana e o turno. Revisar função.')
            
    def is_weekend(self):
        weekend = ('sab', 'dom')
        weekday = ('seg', 'ter', 'qua', 'qui', 'sex')
        if (self.get_weekday() in weekend) or self.is_sex_3():
            return True
        if self.get_weekday() in weekday:
            return False
        raise myexceptions.LogicException('O método is_weekend() está retornando algum valor inapropriado.')
    
    def get_weekday(self):
        return config.dias_da_semana[self.data.weekday()]

    def is_sex_3(self):
        if (self.data.weekday() == 4) and (self.turno == 3):
            return True
        return False
    
    def get_ordem_prioridade_fds_para_empenhar(self):
        if not self.is_weekend():
            raise myexceptions.LogicException('O serviço não é fds.')
        if self.get_modalidade() == 'sab_3':
            return 0
        if self.get_modalidade() == 'sex_3':
            return 1
        if self.get_modalidade() == 'dom_3':
            return 2
        if self.get_modalidade() == 'fds_12':
            return 3
        
    
    def __str__(self):
        return 'Data: {} | Turno: {} | P/G Nome de guerra: {}{}'.format(
            datetime.datetime.strftime(self.data, '%d/%m/%Y'),
            str(self.turno),
            ('{} {}'.format(self.cpu.pg, self.cpu.nome_de_guerra) if self.cpu != None else 'CPU_NONE'),
            (' | Nome estágio: ' + self.nome_estagio if self.nome_estagio != None else '')    
        ) 
        
    
    def __repr__(self):
        return {
            'data': self.data,
            'turno': self.turno,
            'cpu': self.cpu,
            'nome_estagio': self.nome_estagio
        }
    
    def __eq__(self, other_servico):
        if other_servico == None:
            return False
        data_eq = self.data == other_servico.data
        turno_eq = self.turno == other_servico.turno        
        return data_eq and turno_eq

    def __gt__(self, other_servico):
        if self.data == other_servico.data:
            return self.turno > other_servico.turno
        return self.data > other_servico.data
