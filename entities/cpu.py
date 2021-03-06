import datetime
from entities import enums, servico

postos_e_graduacoes = [member.value for name, member in enums.PgEnum.__members__.items()]
funcoes = [member.value for name, member in enums.FuncaoEnum.__members__.items()]
cursos = [member.value for name, member in enums.CursoEnum.__members__.items()]

class Cpu:
    def __init__(self, pg, nome_completo, nome_de_guerra, funcao, curso, ano_base):        
        self.pg = pg
        self.nome_completo = nome_completo
        self.nome_de_guerra = {'nome_de_guerra': nome_de_guerra, 'nome_completo': nome_completo}
        self.funcao = funcao
        self.curso = curso
        self.ano_base = ano_base
        self.servicos_fds = None        
        
    
    @property
    def pg(self):
        return self.__pg

    @property
    def nome_completo(self):
        return self.__nome_completo
    
    @property
    def nome_de_guerra(self):
        return self.__nome_de_guerra
    
    @property
    def funcao(self):
        return self.__funcao
    
    @property
    def curso(self):
        return self.__curso
    
    @property
    def ano_base(self):
        return self.__ano_base
    
    @property
    def servicos_fds(self):
        return self.__servicos_fds
    
    
    @pg.setter
    def pg(self, pg):
        if not isinstance(pg, str):
            raise TypeError('pg deve ser string.')
        if not pg.upper() in postos_e_graduacoes:
            raise ValueError('pg deve receber um dos valores seguintes: ' + ', '.join(postos_e_graduacoes) + '.')
        self.__pg = pg.upper()
        

    @nome_completo.setter
    def nome_completo(self, nome_completo):
        if not isinstance(nome_completo, str):
            raise TypeError('Nome completo deve ser do tipo string.')
        if len(nome_completo.split()) < 2:
            raise ValueError('Nome completo deve ter ao menos 2 nomes.')
        self.__nome_completo = nome_completo.upper()        

    @nome_de_guerra.setter
    def nome_de_guerra(self, dict_nomes):
        if not isinstance(dict_nomes['nome_de_guerra'], str) and isinstance(dict_nomes['nome_completo'], str):
            raise ValueError('Nomes devem ser do tipo string.')
        nome_de_guerra = dict_nomes['nome_de_guerra'].upper()
        nome_completo = dict_nomes['nome_completo'].upper()        
        if not len(set(nome_de_guerra.split(' ')).intersection(self.nome_completo.split(' '))):
            print(nome_completo)
            print(nome_de_guerra)
            raise ValueError('O nome de guerra deve estar contindo no nome completo.')
        self.__nome_de_guerra = nome_de_guerra.upper()        

    @funcao.setter
    def funcao(self, funcao):
        if not isinstance(funcao, str):
            raise TypeError('Função deve ser do tipo string.')
        if not funcao.upper() in funcoes:
            raise ValueError('O parâmetro funcao deve receber um dos valores seguintes: ' + ', '.join(funcoes) + '.')
        self.__funcao = funcao.upper()

    @curso.setter
    def curso(self, curso):
        if not isinstance(curso, str):
            raise TypeError('Curso deve ser do tipo string.')
        if not curso.upper() in cursos:
            raise ValueError('curso deve receber um dos valores seguintes: ' + ', '.join(cursos) + '.')
        self.__curso = curso.upper()        

    @ano_base.setter
    def ano_base(self, ano_base):
        if ano_base == None or ano_base == '':
            self.__ano_base = None
            return
        try:
            ano_base = int(ano_base)
        except TypeError:
            raise TypeError('O parâmetro ano_base deve receber um valor numérico.')        
        if not 1980 <= ano_base <= datetime.datetime.now().year:
            raise ValueError('Ano base inválido.')
        self.__ano_base = ano_base
    
    @servicos_fds.setter
    def servicos_fds(self, aux_not_used):
        self.__servicos_fds = list()
    
    def get_fds_em_sequencia(self):                
        fds_em_sequencia = 0
        if not len(self.servicos_fds):
            return fds_em_sequencia
        
        number_year_and_week_todos_os_servicos = list(map(lambda _servico: _servico.data.isocalendar()[:2], self.servicos_fds))
        number_year_and_week_todos_os_servicos.sort(reverse=True, key= lambda l: (l[0], l[1]))
        data_ultimo_servico = max(list(map(lambda _servico: _servico.data, self.servicos_fds)))
        
        
        year_and_week_ultima_semana = data_ultimo_servico.isocalendar()[:2]
        for year_and_week in number_year_and_week_todos_os_servicos:            
            if year_and_week == year_and_week_ultima_semana:
                fds_em_sequencia += 1
            else:
                data_ultimo_servico -= datetime.timedelta(days=7)
                year_and_week_ultima_semana = data_ultimo_servico.isocalendar()[:2]
                if year_and_week == year_and_week_ultima_semana:
                    fds_em_sequencia += 1
                else:
                    break
        return fds_em_sequencia
        
  
    def __eq__(self, other_cpu):
        if other_cpu == None:
            return False
        pg_eq = self.pg == other_cpu.pg
        nome_completo_eq = self.nome_completo == other_cpu.nome_completo
        nome_de_guerra_eq = self.nome_de_guerra == other_cpu.nome_de_guerra
        funcao_eq = self.funcao == other_cpu.funcao
        curso_eq = self.curso == other_cpu.curso
        ano_base_eq = self.ano_base == other_cpu.ano_base        
        return  pg_eq and nome_completo_eq and nome_de_guerra_eq and funcao_eq and curso_eq and ano_base_eq

    def __repr__(self):
        return {
            'pg': self.pg,
            'nome_completo': self.nome_completo,
            'nome_de_guerra': self.nome_de_guerra,
            'funcao': self.funcao,
            'curso': self.curso,
            'ano_base': self.ano_base
        }

    def __str__(self):
        return\
            "{}: {:8} |".format('P/G', self.pg) +\
            "{}: {:16} |".format('Nome de Guerra', self.nome_de_guerra) +\
            "{}: {:32} |".format('Nome Completo', self.nome_completo) +\
            "{}: {:4} |".format('Função', self.funcao) +\
            "{}: {:4} |".format('Curso', self.curso) +\
            "{}: {:4} |".format('Ano base', self.ano_base)
            
            
            
            
            
            
            
            
            