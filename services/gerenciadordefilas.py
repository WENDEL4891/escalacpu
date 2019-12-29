from dbdao import servicodao, cpudao
from entities import filapormodalidade


class GerenciadorDeFilas:
    def __init__(self, data_inicio, data_fim):        
        self.servicos = {'data_inicio': data_inicio, 'data_fim': data_fim}

        self.fila_fds = 'fds'
        self.fila_semana = 'semana'
        self.fila_seg_12 = 'seg_12'
        self.fila_seg_3 = 'seg_3'
        self.fila_ter_qui_sex_12 = 'ter_qui_sex_12'
        self.fila_qua_12 = 'qua_12'
        self.fila_ter_3 = 'ter_3'
        self.fila_qua_3 = 'qua_3'
        self.fila_qui_3 = 'qui_3'
        self.fila_sex_3 = 'sex_3'
        self.fila_fds_12 = 'fds_12'
        self.fila_sab_3 = 'sab_3'
        self.fila_dom_3 = 'dom_3'
    
    
    @property
    def servicos(self):
        return self.__servicos

    
    @property
    def fila_fds(self):        
        return self.__fila_fds

    @property    
    def fila_semana(self):        
        return self.__fila_semana

    @property    
    def fila_seg_12(self):        
        return self.__fila_seg_12

    @property    
    def fila_seg_3(self):        
        return self.__fila_seg_3

    @property    
    def fila_ter_qui_sex_12(self):        
        return self.__fila_ter_qui_sex_12

    @property    
    def fila_qua_12(self):        
        return self.__fila_qua_12

    @property    
    def fila_ter_3(self):        
        return self.__fila_ter_3

    @property    
    def fila_qua_3(self):        
        return self.__fila_qua_3

    @property    
    def fila_qui_3(self):        
        return self.__fila_qui_3

    @property    
    def fila_sex_3(self):        
        return self.__fila_sex_3

    @property    
    def fila_fds_12(self):        
        return self.__fila_fds_12

    @property    
    def fila_sab_3(self):        
        return self.__fila_sab_3

    @property    
    def fila_dom_3(self):        
        return self.__fila_dom_3


    @servicos.setter
    def servicos(self, datas_dict):
        servicos = servicodao.ServicoDAO().get_servicos(datas_dict['data_inicio'], datas_dict['data_fim'])
        servicos.sort()        
        self.__servicos = servicos

    
    @fila_fds.setter
    def fila_fds(self, modalidade):        
        servicos_fds = list(filter(lambda _servico: _servico.is_weekend(), self.servicos))
        fila_fds = filapormodalidade.FilaPorModalidade(modalidade)
        for _servico in servicos_fds:
            _cpu = cpudao.CpuDAO().get_cpu(_servico.nome_de_guerra)
            if _cpu.funcao != 'TM':
                fila_fds.membro_add_final_da_fila(_cpu.nome_de_guerra)
        self.__fila_fds = fila_fds        
        
    @fila_semana.setter    
    def fila_semana(self, modalidade):        
        servicos_semana = list(filter(lambda _servico: not _servico.is_weekend(), self.servicos))
        fila_semana = filapormodalidade.FilaPorModalidade(modalidade)
        for _servico in servicos_semana:
            _cpu = cpudao.CpuDAO().get_cpu(_servico.nome_de_guerra)
            if _cpu.funcao != 'TM':
                fila_semana.membro_add_final_da_fila(_cpu.nome_de_guerra)
        self.__fila_semana = fila_semana        
        
    @fila_seg_12.setter    
    def fila_seg_12(self, modalidade):        
        servicos_seg_12 = list(filter(lambda _servico: _servico.get_modalidade() == 'seg_12', self.servicos))
        fila_seg_12 = filapormodalidade.FilaPorModalidade(modalidade)
        for _servico in servicos_seg_12:
            _cpu = cpudao.CpuDAO().get_cpu(_servico.nome_de_guerra)
            if _cpu.funcao != 'TM':
                fila_seg_12.membro_add_final_da_fila(_cpu.nome_de_guerra)
        self.__fila_seg_12 = fila_seg_12        
        
    @fila_seg_3.setter    
    def fila_seg_3(self, modalidade):        
        servicos_seg_3 = list(filter(lambda _servico: _servico.get_modalidade() == 'seg_3', self.servicos))
        fila_seg_3 = filapormodalidade.FilaPorModalidade(modalidade)
        for _servico in servicos_seg_3:
            _cpu = cpudao.CpuDAO().get_cpu(_servico.nome_de_guerra)
            if _cpu.funcao != 'TM':
                fila_seg_3.membro_add_final_da_fila(_cpu.nome_de_guerra)
        self.__fila_seg_3 = fila_seg_3        
        
    @fila_ter_qui_sex_12.setter    
    def fila_ter_qui_sex_12(self, modalidade):        
        servicos_ter_qui_sex_12 = list(filter(lambda _servico: _servico.get_modalidade() == 'ter_qui_sex_12', self.servicos))
        fila_ter_qui_sex_12 = filapormodalidade.FilaPorModalidade(modalidade)
        for _servico in servicos_ter_qui_sex_12:
            _cpu = cpudao.CpuDAO().get_cpu(_servico.nome_de_guerra)
            if _cpu.funcao != 'TM':
                fila_ter_qui_sex_12.membro_add_final_da_fila(_cpu.nome_de_guerra)
        self.__fila_ter_qui_sex_12 = fila_ter_qui_sex_12        
        
    @fila_qua_12.setter    
    def fila_qua_12(self, modalidade):        
        servicos_qua_12 = list(filter(lambda _servico: _servico.get_modalidade() == 'qua_12', self.servicos))
        fila_qua_12 = filapormodalidade.FilaPorModalidade(modalidade)
        for _servico in servicos_qua_12:
            _cpu = cpudao.CpuDAO().get_cpu(_servico.nome_de_guerra)
            if _cpu.funcao != 'TM':
                fila_qua_12.membro_add_final_da_fila(_cpu.nome_de_guerra)
        self.__fila_qua_12 = fila_qua_12        
        
    @fila_ter_3.setter    
    def fila_ter_3(self, modalidade):        
        servicos_ter_3 = list(filter(lambda _servico: _servico.get_modalidade() == 'ter_3', self.servicos))
        fila_ter_3 = filapormodalidade.FilaPorModalidade(modalidade)
        for _servico in servicos_ter_3:
            _cpu = cpudao.CpuDAO().get_cpu(_servico.nome_de_guerra)
            if _cpu.funcao != 'TM':
                fila_ter_3.membro_add_final_da_fila(_cpu.nome_de_guerra)
        self.__fila_ter_3 = fila_ter_3        
        
    @fila_qua_3.setter    
    def fila_qua_3(self, modalidade):        
        servicos_qua_3 = list(filter(lambda _servico: _servico.get_modalidade() == 'qua_3', self.servicos))
        fila_qua_3 = filapormodalidade.FilaPorModalidade(modalidade)
        for _servico in servicos_qua_3:
            _cpu = cpudao.CpuDAO().get_cpu(_servico.nome_de_guerra)
            if _cpu.funcao != 'TM':
                fila_qua_3.membro_add_final_da_fila(_cpu.nome_de_guerra)
        self.__fila_qua_3 = fila_qua_3        
        
    @fila_qui_3.setter    
    def fila_qui_3(self, modalidade):        
        servicos_qui_3 = list(filter(lambda _servico: _servico.get_modalidade() == 'qui_3', self.servicos))
        fila_qui_3 = filapormodalidade.FilaPorModalidade(modalidade)
        for _servico in servicos_qui_3:
            _cpu = cpudao.CpuDAO().get_cpu(_servico.nome_de_guerra)
            if _cpu.funcao != 'TM':
                fila_qui_3.membro_add_final_da_fila(_cpu.nome_de_guerra)
        self.__fila_qui_3 = fila_qui_3        
        
    @fila_sex_3.setter    
    def fila_sex_3(self, modalidade):        
        servicos_sex_3 = list(filter(lambda _servico: _servico.get_modalidade() == 'sex_3', self.servicos))
        fila_sex_3 = filapormodalidade.FilaPorModalidade(modalidade)
        for _servico in servicos_sex_3:
            _cpu = cpudao.CpuDAO().get_cpu(_servico.nome_de_guerra)
            if _cpu.funcao != 'TM':
                fila_sex_3.membro_add_final_da_fila(_cpu.nome_de_guerra)
        self.__fila_sex_3 = fila_sex_3        
        
    @fila_fds_12.setter    
    def fila_fds_12(self, modalidade):        
        servicos_fds_12 = list(filter(lambda _servico: _servico.get_modalidade() == 'fds_12', self.servicos))
        fila_fds_12 = filapormodalidade.FilaPorModalidade(modalidade)
        for _servico in servicos_fds_12:
            _cpu = cpudao.CpuDAO().get_cpu(_servico.nome_de_guerra)
            if _cpu.funcao != 'TM':
                fila_fds_12.membro_add_final_da_fila(_cpu.nome_de_guerra)
        self.__fila_fds_12 = fila_fds_12        
        
    @fila_sab_3.setter    
    def fila_sab_3(self, modalidade):        
        servicos_sab_3 = list(filter(lambda _servico: _servico.get_modalidade() == 'sab_3', self.servicos))
        fila_sab_3 = filapormodalidade.FilaPorModalidade(modalidade)
        for _servico in servicos_sab_3:
            _cpu = cpudao.CpuDAO().get_cpu(_servico.nome_de_guerra)
            if _cpu.funcao != 'TM':
                fila_sab_3.membro_add_final_da_fila(_cpu.nome_de_guerra)
        self.__fila_sab_3 = fila_sab_3        
        
    @fila_dom_3.setter    
    def fila_dom_3(self, modalidade):        
        servicos_dom_3 = list(filter(lambda _servico: _servico.get_modalidade() == 'dom_3', self.servicos))
        fila_dom_3 = filapormodalidade.FilaPorModalidade(modalidade)
        for _servico in servicos_dom_3:
            _cpu = cpudao.CpuDAO().get_cpu(_servico.nome_de_guerra)
            if _cpu.funcao != 'TM':
                fila_dom_3.membro_add_final_da_fila(_cpu.nome_de_guerra)
        self.__fila_dom_3 = fila_dom_3