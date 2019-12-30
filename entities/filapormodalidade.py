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
        self.ultimo_servico_da_fila = None
        
    
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
    
    @property
    def cpus_tm(self):
        self.__cpus_tm = list(filter(lambda _cpu: _cpu.funcao == 'TM', self.cpus))
        return self.__cpus_tm
    
    @property
    def nomes_de_guerra(self):
        self.__nomes_de_guerra = list(map(lambda _cpu: _cpu.nome_de_guerra, self.cpus_sem_tm))
        return self.__nomes_de_guerra


    
    def membro_add_ultimo_para_primeiro(self, _servico):
        if not isinstance(_servico.cpu, cpu.Cpu):        
            raise TypeError('O parâmetro _servico deve receber um objeto do tipo servico.Servico.')
        
        nomes_de_guerra_fila = list(map(lambda _cpu: _cpu.nome_de_guerra, self.fila.values()))
        if not _servico.cpu.nome_de_guerra in nomes_de_guerra_fila:
            ordem = len(self.cpus_sem_tm) - len(self.fila)
            self.fila[ordem] = _servico.cpu
            if ordem == 1:
                self.ultimo_servico_da_fila = _servico


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
        for ordem, cpu in self.fila.items():
            aux += '\t{}: {} {}\n'.format(ordem, cpu.pg, cpu.nome_de_guerra)
        aux += '}'
        return aux