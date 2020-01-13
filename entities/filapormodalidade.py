from dbdao import cpudao
from entities import cpu, servico
import services.functions
import myexceptions
import copy
import datetime


class FilaPorModalidade:

    cpu_dao = cpudao.CpuDAO()

    def __init__(self, modalidade):
        self.modalidade = modalidade      
        self.fila = list()  
        
        
    
    @property
    def modalidades_validas(self):
        self.__modalidades_validas = ('fds', 'semana', 'sem_12','sem_3','qua_2','qui_3','sex_2','sex_3','fds_12','sab_3','dom_3')
        return self.__modalidades_validas
    
    @property
    def modalidade(self):
        return self.__modalidade

    @property
    def cpus(self):
        self.__cpus = copy.copy(self.cpu_dao.cpus)
        return self.__cpus
    
    @property
    def cpus_sem_tm(self):
        self.__cpus_sem_tm = list(filter(lambda _cpu: not _cpu.funcao == 'TM', self.cpus))
        return self.__cpus_sem_tm
    
    @property
    def cpus_tm(self):
        self.__cpus_tm = list(filter(lambda _cpu: _cpu.funcao == 'TM', self.cpus))
        return self.__cpus_tm
    
    @property
    def nomes_de_guerra(self):
        self.__nomes_de_guerra = list(map(lambda _cpu: _cpu.nome_de_guerra, self.cpus_sem_tm))
        return self.__nomes_de_guerra

    @modalidade.setter
    def modalidade(self, modalidade):
        if not isinstance(modalidade, str):

            raise ValueError('O parâmetro modalidade deve receber um argumento do tipo string.')
        if modalidade.lower() not in self.modalidades_validas:
            raise ValueError('Somente são aceitas modalidades dentre as seguintes: {}'.format(', '.join(self.modalidades_validas)))
        self.__modalidade = modalidade.lower()
    
        
    def membro_add_ultimo_para_primeiro(self, _servico):
        if not isinstance(_servico, servico.Servico):        
            raise TypeError('O parâmetro _servico deve receber um objeto do tipo servico.Servico.')                         
        
        if not self.modalidade == 'fds':
            if not _servico.cpu.nome_de_guerra in list(map(lambda _cpu: _cpu.nome_de_guerra, self.fila)):
                self.fila.insert(0, _servico.cpu)
        else:
            cpu_not_in_fila = True
            for _cpu in self.fila:
                if _cpu.nome_de_guerra == _servico.cpu.nome_de_guerra:
                    cpu_not_in_fila = False
                    _cpu.servicos_fds.append(_servico)
                    break
            if cpu_not_in_fila:
                cpu_para_incluir = _servico.cpu
                cpu_para_incluir.servicos_fds.append(_servico)
                self.fila.insert(0, cpu_para_incluir)
        
        
    def fds_add(self, _servico):
        cpu_ja_esta_na_fila_bool = False
        for _cpu in self.fila:
            if _cpu == _servico.cpu:                
                cpu_ja_esta_na_fila_bool = True
                _cpu.ultimo_servico_fds = _servico                
                
        if not cpu_ja_esta_na_fila_bool:            
            cpu_para_incluir = _servico.cpu
            cpu_para_incluir.ultimo_servico_fds = _servico
            cpu_para_incluir.sequencia_servicos_fds = 1
            self.fila.append(cpu_para_incluir)
    
    def membro_add_primeiro_para_ultimo(self, _cpu):
        if not isinstance(_cpu, cpu.Cpu):
            raise TypeError('O parâmetro _cpu deve receber um argumento do tipo cpu.Cpu. Foi passado {}.'.format(str(type(_cpu))))
        self.fila.insert(0, _cpu)
            
    
    def membro_add_final_da_fila(self, nome_de_guerra):
        ultima_posicao = len(self.fila)
        if not isinstance(nome_de_guerra, str):
            raise TypeError('O parâmetro nome_de_guerra deve receber um argumento do tipo string.')        
        if not nome_de_guerra.upper() in self.nomes_de_guerra:
            raise ValueError('O argumento infomado, no parâmetro nome_de_guerra ({}) não está cadastrado.'.format(nome_de_guerra.upper()))        
        if not nome_de_guerra.upper() in self.fila.values():
            final_da_fila = ultima_posicao + 1
            self.fila[final_da_fila] = nome_de_guerra.upper()
        else:                        
            ordem_atual = services.functions.get_value_from_key_in_dict(self.fila, nome_de_guerra.upper())
            for ordem, nome in self.fila.items():
                if ordem > ordem_atual:
                    self.fila[ordem - 1] = nome
            self.fila[ultima_posicao] = nome_de_guerra.upper()
    
    def get_next_membro(self, pula=0):
        qtd_de_membros = len(self.fila)
        if not qtd_de_membros:
            raise myexceptions.LogicException('Não há nenhum membro na fila {}'.format(self.modalidade))
        if not isinstance(pula, int):
            raise TypeError('O parâmetro pula é opcional. Quando for preenchido, deve receber um argumento do tipo int. Foi passado {}'.format(str(type(pula))))
        if pula >= qtd_de_membros:
            raise myexceptions.LogicException('Não é possível pular {} membros, pois o tamanho da fila é de {} membros.'.format(pula, qtd_de_membros))
        index_next_membro = 0 + pula
        next_membro = self.fila.pop(index_next_membro)
        self.fila.append(next_membro)
        return next_membro
    
    def show_next_membro(self, pula=0):
        qtd_de_membros = len(self.fila)
        if not qtd_de_membros:
            raise myexceptions.LogicException('Não há nenhum membro na fila {}'.format(self.modalidade))
        if not isinstance(pula, int):
            raise TypeError('O parâmetro pula é opcional. Quando for preenchido, deve receber um argumento do tipo int. Foi passado {}'.format(str(type(pula))))
        if pula >= qtd_de_membros:
            raise myexceptions.LogicException('Não é possível pular {} membros, pois o tamanho da fila é de {} membros.'.format(pula, qtd_de_membros))
        next_membro = self.fila[0 + pula]
        return next_membro

            
    def __str__(self):
        
        fila_str = 'Fila = {} '.format(self.modalidade) + '{\n'
        for i in range(len(self.fila)):
            if self.modalidade == 'fds':
                fila_str += '\t{:<2}: {:22} | Último serviço: {:10} | Serviços em sequência: {}\n'.format(
                    i + 1,
                    self.fila[i].pg + " " + self.fila[i].nome_de_guerra,
                    datetime.datetime.strftime(max(self.fila[i].servicos_fds).data, '%d/%m/%Y') if len(self.fila[i].servicos_fds) else '---',
                    self.fila[i].get_fds_em_sequencia()
                )
            else:
                fila_str += '\t{:<2}: {:22}\n'.format(i + 1, self.fila[i].pg + " " + self.fila[i].nome_de_guerra)
        fila_str += '}'
        return fila_str