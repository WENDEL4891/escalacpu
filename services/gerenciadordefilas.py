from dbdao import servicodao, cpudao
from entities import filapormodalidade, servico
import datetime


class GerenciadorDeFilas:
    cpu_dao = cpudao.CpuDAO()

    def __init__(self, data_fim):        
        self.servicos_em_ordem_decrescente = data_fim
        self.servicos_em_ordem_decrescente_sem_tm = self.servicos_em_ordem_decrescente

        self.filas_setter()

        self.fila_fds = 'fds'
        self.fila_semana = 'semana'
        self.fila_sem_12 = 'sem_12'
        self.fila_sem_3 = 'sem_3'        
        self.fila_qua_2 = 'qua_2'
        self.fila_qui_3 = 'qui_3'
        self.fila_sex_2 = 'sex_2'
        self.fila_sex_3 = 'sex_3'
        self.fila_fds_12 = 'fds_12'
        self.fila_sab_3 = 'sab_3'
        self.fila_dom_3 = 'dom_3'
    
    
    @property
    def servicos_em_ordem_decrescente(self):
        return self.__servicos_em_ordem_decrescente
    
    @property
    def servicos_em_ordem_decrescente_sem_tm(self):
        return self.__servicos_em_ordem_decrescente_sem_tm
    
    @property
    def filas(self):
        return self.__filas

    @property
    def fila_fds(self):        
        return self.__fila_fds
    

            
    @property    
    def fila_semana(self):        
        return self.__fila_semana

    @property    
    def fila_sem_12(self):        
        return self.__fila_sem_12

    @property    
    def fila_sem_3(self):        
        return self.__fila_sem_3

    @property    
    def fila_qua_2(self):        
        return self.__fila_qua_2

    @property    
    def fila_qui_3(self):        
        return self.__fila_qui_3

    @property    
    def fila_sex_2(self):        
        return self.__fila_sex_2
    
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


    @servicos_em_ordem_decrescente.setter
    def servicos_em_ordem_decrescente(self, data_fim):        
        data_inicio = data_fim - datetime.timedelta(days=190)
        servicos_em_ordem_decrescente = servicodao.ServicoDAO().get_servicos(data_inicio, data_fim)
        servicos_em_ordem_decrescente.sort(reverse=True)
        self.__servicos_em_ordem_decrescente = servicos_em_ordem_decrescente
    
    
    @servicos_em_ordem_decrescente_sem_tm.setter
    def servicos_em_ordem_decrescente_sem_tm(self, servicos):        
        self.__servicos_em_ordem_decrescente_sem_tm = list(filter(lambda _servico: _servico.cpu.funcao != 'TM', servicos))


    def filas_setter(self):
        filas = dict()
        filas['fds'] = filapormodalidade.FilaPorModalidade('fds')
        filas['sem_12'] = filapormodalidade.FilaPorModalidade('sem_12')
        filas['sem_3'] = filapormodalidade.FilaPorModalidade('sem_3')
        filas['qua_2'] = filapormodalidade.FilaPorModalidade('qua_2')
        filas['qui_3'] = filapormodalidade.FilaPorModalidade('qui_3')
        filas['sex_2'] = filapormodalidade.FilaPorModalidade('sex_2')
        filas['sex_3'] = filapormodalidade.FilaPorModalidade('sex_3')
        filas['fds_12'] = filapormodalidade.FilaPorModalidade('fds_12')
        filas['sab_3'] = filapormodalidade.FilaPorModalidade('sab_3')
        filas['dom_3'] = filapormodalidade.FilaPorModalidade('dom_3')


        servicos_fds = list(filter(lambda _servico: _servico.is_weekend(), self.servicos_em_ordem_decrescente_sem_tm))
        
        for _servico in servicos_fds:            
            filas['fds'].membro_add_ultimo_para_primeiro(_servico)
        
        filas['fds'].fila.sort(
            key = lambda _cpu: (
                max(list(map(self.number_week_and_year, _cpu.servicos_fds))),
                _cpu.get_fds_em_sequencia(),
                max(list(map(lambda _servico: _servico, _cpu.servicos_fds)))
            )
        )

        if len(filas['fds'].fila) < len(self.cpu_dao.cpus_sem_tm):            
            for _cpu in self.cpu_dao.cpus_sem_tm:
                if _cpu.nome_de_guerra not in list(map(lambda _cpu: _cpu.nome_de_guerra, filas['fds'].fila)):
                    filas['fds'].membro_add_primeiro_para_ultimo(_cpu)
        

        servicos_sem_12 = list(filter(lambda _servico: not _servico.is_weekend(), self.servicos_em_ordem_decrescente_sem_tm))        
        for _servico in servicos_sem_12:                        
            filas['sem_12'].membro_add_ultimo_para_primeiro(_servico)
        
        if len(filas['sem_12'].fila) < len(self.cpu_dao.cpus_sem_tm):            
            for _cpu in self.cpu_dao.cpus_sem_tm:
                if _cpu.nome_de_guerra not in list(map(lambda _cpu: _cpu.nome_de_guerra, filas['sem_12'].fila)):
                    filas['sem_12'].membro_add_primeiro_para_ultimo(_cpu)


        servicos_sem_3 = list(filter(lambda _servico: not _servico.is_weekend(), self.servicos_em_ordem_decrescente_sem_tm))        
        for _servico in servicos_sem_3:                        
            filas['sem_3'].membro_add_ultimo_para_primeiro(_servico)
        
        if len(filas['sem_3'].fila) < len(self.cpu_dao.cpus_sem_tm):            
            for _cpu in self.cpu_dao.cpus_sem_tm:
                if _cpu.nome_de_guerra not in list(map(lambda _cpu: _cpu.nome_de_guerra, filas['sem_3'].fila)):
                    filas['sem_3'].membro_add_primeiro_para_ultimo(_cpu)




        self.__filas = filas
    
    
    
    @fila_fds.setter
    def fila_fds(self, modalidade):        
        servicos_fds = list(filter(lambda _servico: _servico.is_weekend(), self.servicos_em_ordem_decrescente_sem_tm))

        fila_fds = filapormodalidade.FilaPorModalidade(modalidade)        
        for _servico in servicos_fds:            
            fila_fds.membro_add_ultimo_para_primeiro(_servico)
        
        fila_fds.fila.sort(
            key = lambda _cpu: (
                max(list(map(self.number_week_and_year, _cpu.servicos_fds))),
                _cpu.get_fds_em_sequencia(),
                max(list(map(lambda _servico: _servico, _cpu.servicos_fds)))
            )
        )

        if len(fila_fds.fila) < len(self.cpu_dao.cpus_sem_tm):            
            for _cpu in self.cpu_dao.cpus_sem_tm:
                if _cpu.nome_de_guerra not in list(map(lambda _cpu: _cpu.nome_de_guerra, fila_fds.fila)):
                    fila_fds.membro_add_primeiro_para_ultimo(_cpu)        
        self.__fila_fds = fila_fds


    def number_week_and_year(self, _servico):
        if not isinstance(_servico, servico.Servico):
            raise TypeError('O parâmetro _servico deve receber um argumento do tipo servico.Servico. Foi passado {}.'.format(str(type(_servico))))
        
        number_year_and_week = _servico.data.isocalendar()[:2]
        year_str = str(number_year_and_week[0])
        week_str = str(number_year_and_week[1]) if number_year_and_week[1] > 9 else '0{}'.format(number_year_and_week[1])
        year_mais_week_str = year_str + week_str
        year_mais_week_int = int(year_mais_week_str)
        return year_mais_week_int           
                
        
        
        
    @fila_semana.setter
    def fila_semana(self, modalidade):        
        servicos_semana = list(filter(lambda _servico: not _servico.is_weekend(), self.servicos_em_ordem_decrescente_sem_tm))
        fila_semana = filapormodalidade.FilaPorModalidade(modalidade)
        for _servico in servicos_semana:                        
            fila_semana.membro_add_ultimo_para_primeiro(_servico)
        
        if len(fila_semana.fila) < len(self.cpu_dao.cpus_sem_tm):            
            for _cpu in self.cpu_dao.cpus_sem_tm:
                if _cpu.nome_de_guerra not in list(map(lambda _cpu: _cpu.nome_de_guerra, fila_semana.fila)):
                    fila_semana.membro_add_primeiro_para_ultimo(_cpu)
        self.__fila_semana = fila_semana
        
    @fila_sem_12.setter
    def fila_sem_12(self, modalidade):
        servicos_sem_12 = list(filter(lambda _servico: _servico.get_modalidade() == 'sem_12', self.servicos_em_ordem_decrescente_sem_tm))        
        fila_sem_12 = filapormodalidade.FilaPorModalidade(modalidade)
        for _servico in servicos_sem_12:                        
            fila_sem_12.membro_add_ultimo_para_primeiro(_servico)

        if len(fila_sem_12.fila) < len(self.cpu_dao.cpus_sem_tm):            
            for _cpu in self.cpu_dao.cpus_sem_tm:
                if _cpu.nome_de_guerra not in list(map(lambda _cpu: _cpu.nome_de_guerra, fila_sem_12.fila)):
                    fila_sem_12.membro_add_primeiro_para_ultimo(_cpu)
        self.__fila_sem_12 = fila_sem_12
        
    @fila_sem_3.setter
    def fila_sem_3(self, modalidade):        
        servicos_sem_3 = list(filter(lambda _servico: _servico.get_modalidade() == 'sem_3', self.servicos_em_ordem_decrescente_sem_tm))        
        fila_sem_3 = filapormodalidade.FilaPorModalidade(modalidade)
        for _servico in servicos_sem_3:                        
            fila_sem_3.membro_add_ultimo_para_primeiro(_servico)
        
        if len(fila_sem_3.fila) < len(self.cpu_dao.cpus_sem_tm):            
            for _cpu in self.cpu_dao.cpus_sem_tm:
                if _cpu.nome_de_guerra not in list(map(lambda _cpu: _cpu.nome_de_guerra, fila_sem_3.fila)):
                    fila_sem_3.membro_add_primeiro_para_ultimo(_cpu)
        self.__fila_sem_3 = fila_sem_3        
         
        
    @fila_qua_2.setter
    def fila_qua_2(self, modalidade):        
        servicos_qua_2 = list(filter(lambda _servico: _servico.get_modalidade() == 'qua_2', self.servicos_em_ordem_decrescente_sem_tm))
        fila_qua_2 = filapormodalidade.FilaPorModalidade(modalidade)
        for _servico in servicos_qua_2:                        
            fila_qua_2.membro_add_ultimo_para_primeiro(_servico)

        if len(fila_qua_2.fila) < len(self.cpu_dao.cpus_sem_tm):            
            for _cpu in self.cpu_dao.cpus_sem_tm:
                if _cpu.nome_de_guerra not in list(map(lambda _cpu: _cpu.nome_de_guerra, fila_qua_2.fila)):
                    fila_qua_2.membro_add_primeiro_para_ultimo(_cpu)
        self.__fila_qua_2 = fila_qua_2        
          
        
    @fila_sex_2.setter
    def fila_sex_2(self, modalidade):        
        servicos_sex_2 = list(filter(lambda _servico: _servico.get_modalidade() == 'sex_2', self.servicos_em_ordem_decrescente_sem_tm))
        fila_sex_2 = filapormodalidade.FilaPorModalidade(modalidade)
        for _servico in servicos_sex_2:                        
            fila_sex_2.membro_add_ultimo_para_primeiro(_servico)
        
        if len(fila_sex_2.fila) < len(self.cpu_dao.cpus_sem_tm):            
            for _cpu in self.cpu_dao.cpus_sem_tm:
                if _cpu.nome_de_guerra not in list(map(lambda _cpu: _cpu.nome_de_guerra, fila_sex_2.fila)):
                    fila_sex_2.membro_add_primeiro_para_ultimo(_cpu)
        self.__fila_sex_2 = fila_sex_2        
        
    @fila_qui_3.setter
    def fila_qui_3(self, modalidade):        
        servicos_qui_3 = list(filter(lambda _servico: _servico.get_modalidade() == 'qui_3', self.servicos_em_ordem_decrescente_sem_tm))
        fila_qui_3 = filapormodalidade.FilaPorModalidade(modalidade)
        for _servico in servicos_qui_3:                        
            fila_qui_3.membro_add_ultimo_para_primeiro(_servico)

        if len(fila_qui_3.fila) < len(self.cpu_dao.cpus_sem_tm):            
            for _cpu in self.cpu_dao.cpus_sem_tm:
                if _cpu.nome_de_guerra not in list(map(lambda _cpu: _cpu.nome_de_guerra, fila_qui_3.fila)):
                    fila_qui_3.membro_add_primeiro_para_ultimo(_cpu)
        self.__fila_qui_3 = fila_qui_3        
        
    @fila_sex_3.setter
    def fila_sex_3(self, modalidade):        
        servicos_sex_3 = list(filter(lambda _servico: _servico.get_modalidade() == 'sex_3', self.servicos_em_ordem_decrescente_sem_tm))
        fila_sex_3 = filapormodalidade.FilaPorModalidade(modalidade)
        for _servico in servicos_sex_3:                        
            fila_sex_3.membro_add_ultimo_para_primeiro(_servico)

        if len(fila_sex_3.fila) < len(self.cpu_dao.cpus_sem_tm):            
            for _cpu in self.cpu_dao.cpus_sem_tm:
                if _cpu.nome_de_guerra not in list(map(lambda _cpu: _cpu.nome_de_guerra, fila_sex_3.fila)):
                    fila_sex_3.membro_add_primeiro_para_ultimo(_cpu)
        self.__fila_sex_3 = fila_sex_3        
        
    @fila_fds_12.setter
    def fila_fds_12(self, modalidade):        
        servicos_fds_12 = list(filter(lambda _servico: _servico.get_modalidade() == 'fds_12', self.servicos_em_ordem_decrescente_sem_tm))
        fila_fds_12 = filapormodalidade.FilaPorModalidade(modalidade)
        for _servico in servicos_fds_12:                        
            fila_fds_12.membro_add_ultimo_para_primeiro(_servico)
        
        if len(fila_fds_12.fila) < len(self.cpu_dao.cpus_sem_tm):            
            for _cpu in self.cpu_dao.cpus_sem_tm:
                if _cpu.nome_de_guerra not in list(map(lambda _cpu: _cpu.nome_de_guerra, fila_fds_12.fila)):
                    fila_fds_12.membro_add_primeiro_para_ultimo(_cpu)
        self.__fila_fds_12 = fila_fds_12        
        
    @fila_sab_3.setter
    def fila_sab_3(self, modalidade):        
        servicos_sab_3 = list(filter(lambda _servico: _servico.get_modalidade() == 'sab_3', self.servicos_em_ordem_decrescente_sem_tm))
        fila_sab_3 = filapormodalidade.FilaPorModalidade(modalidade)
        for _servico in servicos_sab_3:                        
            fila_sab_3.membro_add_ultimo_para_primeiro(_servico)
        
        if len(fila_sab_3.fila) < len(self.cpu_dao.cpus_sem_tm):            
            for _cpu in self.cpu_dao.cpus_sem_tm:
                if _cpu.nome_de_guerra not in list(map(lambda _cpu: _cpu.nome_de_guerra, fila_sab_3.fila)):
                    fila_sab_3.membro_add_primeiro_para_ultimo(_cpu)
        self.__fila_sab_3 = fila_sab_3        
        
    @fila_dom_3.setter
    def fila_dom_3(self, modalidade):        
        servicos_dom_3 = list(filter(lambda _servico: _servico.get_modalidade() == 'dom_3', self.servicos_em_ordem_decrescente_sem_tm))
        fila_dom_3 = filapormodalidade.FilaPorModalidade(modalidade)
        for _servico in servicos_dom_3:                        
            fila_dom_3.membro_add_ultimo_para_primeiro(_servico)
        
        if len(fila_dom_3.fila) < len(self.cpu_dao.cpus_sem_tm):            
            for _cpu in self.cpu_dao.cpus_sem_tm:
                if _cpu.nome_de_guerra not in list(map(lambda _cpu: _cpu.nome_de_guerra, fila_dom_3.fila)):
                    fila_dom_3.membro_add_primeiro_para_ultimo(_cpu)
        self.__fila_dom_3 = fila_dom_3