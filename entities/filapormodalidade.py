from dbdao import cpudao
from entities import cpu
import services.functions
import myexceptions
import copy


class FilaPorModalidade:

    cpu_dao = cpudao.CpuDAO()

    def __init__(self, modalidade):
        if not isinstance(modalidade, str):
            raise ValueError('O parâmetro modalidade deve receber um argumento do tipo string.')
        if modalidade.lower() not in self.modalidades_validas:
            raise ValueError('Somente são aceitas modalidades dentre as seguintes: {}'.format(', '.join(self.modalidades_validas)))
        self.modalidade = modalidade.lower()
        self.fila = dict()
        
    
    @property
    def modalidades_validas(self):
        self.__modalidades_validas = ('fds', 'semana', 'seg_12','seg_3','ter_qui_sex_12','qua_12','ter_3','qua_3','qui_3','sex_3','fds_12','sab_3','dom_3')
        return self.__modalidades_validas
    
    @property
    def cpus(self):
        self.__cpus = copy.copy(self.cpu_dao.cpus)
        return self.__cpus
    
    @property
    def cpus_sem_tm(self):
        self.__cpus_sem_tm = list(filter(lambda _cpu: not _cpu.funcao == 'TM', self.cpus))
        return self.__cpus_sem_tm
    
    def cpus_tm(self):
        self.__cpus_tm = list(filter(lambda _cpu: _cpu.funcao == 'TM', self.cpus))
        return self.__cpus_tm

    
    def membro_add_ultimo_para_primeiro(self, _cpu):
        if isinstance(_cpu, cpu.Cpu):
            cpu_Cpu = _cpu
        elif isinstance(_cpu, str):
            cpu_Cpu = self.cpu_dao.get_cpu(_cpu)
            if cpu_Cpu = None:
                raise ValueError('O argumento informado ({}) não é um nome de guerra cadastrado.'.format(_cpu))
        else:
            raise TypeError('O parâmetro _cpu deve receber um argumento do tipo cpu.CPU ou uma string, com um nome de guerra já cadastrado.')
        
        qtd_membros = len(self.cpus_sem_tm)        
        #IMPLEMENTAR A PARTIR DAQUI
        #if not nome_de_guerra.upper() in self.fila.values():
        #    final_da_fila = ultima_posicao + 1
        #    self.fila[final_da_fila] = nome_de_guerra.upper()
        #else:                        
        #    ordem_atual = services.functions.get_value_from_key_in_dict(self.fila, nome_de_guerra.upper())
        #    for ordem, nome in self.fila.items():
        #        if ordem > ordem_atual:
        #            self.fila[ordem - 1] = nome
        #    self.fila[ultima_posicao] = nome_de_guerra.upper()
    
    def membro_add_final_da_fila(self, nome_de_guerra):
        ultima_posicao = len(self.fila)
        if not isinstance(nome_de_guerra, str):
            raise TypeError('O parâmetro nome_de_guerra deve receber um argumento do tipo string.')        
        if not nome_de_guerra.upper() in nomes_de_guerra:
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
            raise TypeError('O parâmetro pula deve receber um argumento do tipo inteiro')
        if pula >= qtd_de_membros:
            raise myexceptions.LogicException('Não é possível pular {} membros, pois o tamanho da fila é de {} membros.'.format(pula, qtd_de_membros))
        next_membro = self.fila[1 + pula]
        for ordem, nome in self.fila.items():
            if ordem > (1 + pula):
                self.fila[ordem -1] = nome
        self.fila[qtd_de_membros] = next_membro
        return next_membro
    
    def __str__(self):
        self.fila = dict(sorted(self.fila.items()))
        aux = 'Fila = {} '.format(self.modalidade) + '{\n'
        for ordem, militar in self.fila.items():
            aux += '\t{}: {}\n'.format(ordem, militar)
        aux += '}'
        return aux