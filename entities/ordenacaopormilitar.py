from datetime import datetime
import services
from dbdao import cpudao

nomes_de_guerra = [cpu_instance.nome_de_guerra for cpu_instance in cpudao.CpuDAO().get_cpus()]

class OrdenacaoPorMilitar:
    def __init__(self, nome_de_guerra, seg_12, seg_3, ter_qui_sex_12, qua_12, ter_3, qua_3, qui_3, sex_3, fds_12, sab_3, dom_3):
        self.nome_de_guerra = nome_de_guerra
        self.seg_12 = seg_12
        self.seg_3 = seg_3
        self.ter_qui_sex_12 = ter_qui_sex_12
        self.qua_12 = qua_12
        self.ter_3 = ter_3
        self.qua_3 = qua_3
        self.qui_3 = qui_3
        self.sex_3 = sex_3
        self.fds_12 = fds_12
        self.sab_3 = sab_3
        self.dom_3 = dom_3


    @property
    def nome_de_guerra(self):
        return self.__nome_de_guerra

    @property    
    def seg_12(self):
        return self.__seg_12

    @property    
    def seg_3(self):
        return self.__seg_3

    @property    
    def ter_qui_sex_12(self):
        return self.__ter_qui_sex_12

    @property    
    def qua_12(self):
        return self.__qua_12

    @property    
    def ter_3(self):
        return self.__ter_3

    @property    
    def qua_3(self):
        return self.__qua_3

    @property    
    def qui_3(self):
        return self.__qui_3

    @property    
    def sex_3(self):
        return self.__sex_3

    @property    
    def fds_12(self):
        return self.__fds_12

    @property    
    def sab_3(self):
        return self.__sab_3

    @property    
    def dom_3(self):
        return self.__dom_3


    @nome_de_guerra.setter
    def nome_de_guerra(self, nome_de_guerra):        
        if not isinstance(nome_de_guerra, str):
            raise TypeError('O parâmetro nome_de_guerra deve receber uma string como argumento.')
        if not nome_de_guerra.upper() in nomes_de_guerra:
            raise ValueError('O nome de guerra informado ({}) não está cadastrado no banco de dados.'.format(nome_de_guerra))
        self.__nome_de_guerra = nome_de_guerra.upper()

    @seg_12.setter    
    def seg_12(self, seg_12):
        self.__seg_12 = seg_12

    @seg_3.setter    
    def seg_3(self, seg_3):
        self.__seg_3 = seg_3

    @ter_qui_sex_12.setter    
    def ter_qui_sex_12(self, ter_qui_sex_12):
        self.__ter_qui_sex_12 = ter_qui_sex_12

    @qua_12.setter    
    def qua_12(self, qua_12):
        self.__qua_12 = qua_12

    @ter_3.setter    
    def ter_3(self, ter_3):
        self.__ter_3 = ter_3

    @qua_3.setter    
    def qua_3(self, qua_3):
        self.__qua_3 = qua_3

    @qui_3.setter    
    def qui_3(self, qui_3):
        self.__qui_3 = qui_3

    @sex_3.setter    
    def sex_3(self, sex_3):
        self.__sex_3 = sex_3

    @fds_12.setter    
    def fds_12(self, fds_12):
        self.__fds_12 = fds_12

    @sab_3.setter    
    def sab_3(self, sab_3):
        self.__sab_3 = sab_3

    @dom_3.setter    
    def dom_3(self, dom_3):
        self.__dom_3 = dom_3

    
    
    def __str__(self):
        attrs = (
            'nome_de_guerra: {}'.format(self.nome_de_guerra),
            'seg_12: {}'.format(self.seg_12),
            'seg_3: {}'.format(self.seg_3),
            'ter_qui_sex_12: {}'.format(self.ter_qui_sex_12),
            'qua_12: {}'.format(self.qua_12),
            'ter_3: {}'.format(self.ter_3),
            'qua_3: {}'.format(self.qua_3),
            'qui_3: {}'.format(self.qui_3),
            'sex_3: {}'.format(self.sex_3),
            'fds_12: {}'.format(self.fds_12),
            'sab_3: {}'.format(self.sab_3),
            'dom_3: {}'.format(self.dom_3)
        )
        return ' | '.join(attrs)

    def __eq__(self, other):
        if other == None:
            return False
        nome_de_guerra_eq = self.nome_de_guerra == other.nome_de_guerra
        seg_12_eq = self.seg_12 == other.seg_12
        seg_3_eq = self.seg_3 == other.seg_3
        ter_qui_sex_12_eq = self.ter_qui_sex_12 == other.ter_qui_sex_12
        qua_12_eq = self.qua_12 == other.qua_12
        ter_3_eq = self.ter_3 == other.ter_3
        qua_3_eq = self.qua_3 == other.qua_3
        qui_3_eq = self.qui_3 == other.qui_3
        sex_3_eq = self.sex_3 == other.sex_3
        fds_12_eq = self.fds_12 == other.fds_12
        sab_3_eq = self.sab_3 == other.sab_3
        dom_3_eq = self.dom_3 == other.dom_3
        return  nome_de_guerra_eq == seg_12_eq == seg_3_eq == ter_qui_sex_12_eq == qua_12_eq == ter_3_eq == qua_3_eq == qui_3_eq == sex_3_eq == fds_12_eq == sab_3_eq == dom_3_eq
    """ def __repr__(self):
        return {
            'data': self.data,
            'tipo': self.tipo
        }
    
    def get_difference(self, other_feriado):
        diff = dict()
        diff['data'] = True if self.data != other_feriado.data else False
        diff['tipo'] = True if self.tipo != other_feriado.tipo else False
        return diff """


