from db import connection
from dbdao import servicodao, feriadodao, cpudao, impedimentodao
from entities import filapormodalidade, servico
from services import functions, gerenciadordefilas
import datetime
import config
import sys
import myexceptions
import pprint

class EscalarSemana:

    def __init__(self):        
        self.dias_e_turnos_seg_a_dom_dict = servicodao.ServicoDAO().get_dias_e_turnos_para_escalar()
        self.servicos_para_completar_list = list()
        for data, turnos in self.dias_e_turnos_seg_a_dom_dict.items():            
            for turno in turnos:
                self.servicos_para_completar_list.append(servico.Servico(data, turno, 'CPU_NONE'))
        
        self.data_segunda = min(self.dias_e_turnos_seg_a_dom_dict)
        self.data_terca = self.data_segunda + datetime.timedelta(days=1)
        self.data_quarta = self.data_terca + datetime.timedelta(days=1)
        self.data_quinta = self.data_quarta + datetime.timedelta(days=1)
        self.data_sexta = self.data_quinta + datetime.timedelta(days=1)
        self.data_sabado = self.data_sexta + datetime.timedelta(days=1)
        self.data_domingo = self.data_sabado + datetime.timedelta(days=1)

        self.servicos_completos_list = servicodao.ServicoDAO().get_servicos(self.data_segunda, self.data_domingo)

        self.cpus = cpudao.CpuDAO().get_cpus()
        self.cpus_tm = list(filter(lambda _cpu: _cpu.funcao == 'TM', self.cpus))
        self.cpus_nao_tm = list(filter(lambda _cpu: _cpu.funcao != 'TM', self.cpus))
        self.gerenciador_de_filas = gerenciadordefilas.GerenciadorDeFilas(self.data_domingo)

        self.feriados = feriadodao.FeriadoDAO().get_feriados(self.data_segunda, self.data_domingo)
        impedimentos = impedimentodao.ImpedimentoDAO().get_impedimentos_from_date(self.data_segunda, self.data_domingo)
        self.impedimentos_por_dia = impedimentos
        self.impedimentos_por_militar = impedimentos


        self.servicos_tm_escalados = list()        
    
    @property
    def impedimentos_por_dia(self):
        return self.__impedimentos_por_dia
    
    @property
    def impedimentos_por_militar(self):
        return self.__impedimentos_por_militar
    
    @impedimentos_por_dia.setter
    def impedimentos_por_dia(self, impedimentos_obj_list):
        '''
            Popula um dicionário, tendo como chaves as datas da semana corrente e como valores uma lista, para cada dia,
            os nomes de guerra dos cpus que tem impedimento naquele dia.
        '''
        impedimentos = dict()
        for data in self.dias_e_turnos_seg_a_dom_dict.keys():
            turnos = dict()
            for i in range(1,4):
                turnos[i] = list()
            impedimentos[data] = turnos
        for impedimento_obj in impedimentos_obj_list:
            data = impedimento_obj.data_inicio
            while data <= impedimento_obj.data_fim:
                if data in self.dias_e_turnos_seg_a_dom_dict.keys():
                    for i in range(1, 4):
                        impedimentos[data][i].append(impedimento_obj.nome_de_guerra)
                data += datetime.timedelta(days=1)
        self.__impedimentos_por_dia = impedimentos

    @impedimentos_por_militar.setter
    def impedimentos_por_militar(self, impedimentos_obj_list):
        '''
            Popula um dicionário, tendo como chaves os nomes dos cpus cadastrados e como valores uma lista, para cada um,
            com as datas em que eles estão com impedimento.
        '''
        impedimentos = dict()
        nomes_de_guerra = list(map(lambda _cpu: _cpu.nome_de_guerra, self.cpus))
        for nome_de_guerra in nomes_de_guerra:
            impedimentos[nome_de_guerra] = dict()            

        #for data in self.dias_e_turnos_seg_a_dom_dict.keys():
        #    turnos = dict()
        #    for i in range(1,4):
        #        turnos[i] = list()
        #    impedimentos[data] = turnos
        for impedimento_obj in impedimentos_obj_list:
            data = impedimento_obj.data_inicio
            while data <= impedimento_obj.data_fim:                
                if data in self.dias_e_turnos_seg_a_dom_dict.keys():
                    if impedimento_obj.nome_de_guerra in nomes_de_guerra:
                        impedimentos[impedimento_obj.nome_de_guerra][data] = list()
                        for i in range(1, 4):
                            impedimentos[impedimento_obj.nome_de_guerra][data].append(i)
                data += datetime.timedelta(days=1)
        self.__impedimentos_por_militar = impedimentos

       
    def escalar_seg_a_dom(self, escalar_tm=True):        


        if escalar_tm:
            logs_escalar_militares_tm = self.escalar_militares_tm()
        
        self.escalar_fds()
    
        #pp = pprint.PrettyPrinter(indent=4)

        #for mens in logs_escalar_militares_tm.items():
        #    pp.pprint(mens)
        
        servicos_para_completar_semana = list(filter(lambda _servico: not _servico.is_weekend(), self.servicos_para_completar_list))
        servicos_para_completar_sem_12 = list(filter(lambda _servico: _servico.get_modalidade() == 'sem_12', self.servicos_para_completar_list))
        servicos_para_completar_sem_3 = list(filter(lambda _servico: _servico.get_modalidade() == 'sem_3', self.servicos_para_completar_list))
        servicos_para_completar_qua_2 = list(filter(lambda _servico: _servico.get_modalidade() == 'qua_2', self.servicos_para_completar_list))
        servicos_para_completar_qui_3 = list(filter(lambda _servico: _servico.get_modalidade() == 'qui_3', self.servicos_para_completar_list))
        servicos_para_completar_sex_2 = list(filter(lambda _servico: _servico.get_modalidade() == 'sex_2', self.servicos_para_completar_list))
        servicos_para_completar_sex_3 = list(filter(lambda _servico: _servico.get_modalidade() == 'sex_3', self.servicos_para_completar_list))
        servicos_para_completar_fds_12 = list(filter(lambda _servico: _servico.get_modalidade() == 'fds_12', self.servicos_para_completar_list))
        servicos_para_completar_sab_3 = list(filter(lambda _servico: _servico.get_modalidade() == 'sab_3', self.servicos_para_completar_list))
        servicos_para_completar_dom_3 = list(filter(lambda _servico: _servico.get_modalidade() == 'dom_3', self.servicos_para_completar_list))

               

        
        #servicos_para_completar_fds = list(filter(lambda _servico: _servico.is_weekend(), self.servicos_para_completar_list))
        #servicos_para_completar_semana = list(filter(lambda _servico: not _servico.is_weekend(), self.servicos_para_completar_list))
        #servicos_para_completar_seg_12 = list(filter(lambda _servico: _servico.get_modalidade() == 'seg_12', self.servicos_para_completar_list))
        #servicos_para_completar_seg_3 = list(filter(lambda _servico: _servico.get_modalidade() == 'seg_3', self.servicos_para_completar_list))
        #servicos_para_completar_ter_qui_sex_12 = list(filter(lambda _servico: _servico.get_modalidade() == 'ter_qui_sex_12', self.servicos_para_completar_list))
        #servicos_para_completar_qua_12 = list(filter(lambda _servico: _servico.get_modalidade() == 'qua_12', self.servicos_para_completar_list))
        #servicos_para_completar_ter_3 = list(filter(lambda _servico: _servico.get_modalidade() == 'ter_3', self.servicos_para_completar_list))
        #servicos_para_completar_qua_3 = list(filter(lambda _servico: _servico.get_modalidade() == 'qua_3', self.servicos_para_completar_list))
        #servicos_para_completar_qui_3 = list(filter(lambda _servico: _servico.get_modalidade() == 'qui_3', self.servicos_para_completar_list))
        #servicos_para_completar_sex_3 = list(filter(lambda _servico: _servico.get_modalidade() == 'sex_3', self.servicos_para_completar_list))
        #servicos_para_completar_fds_12 = list(filter(lambda _servico: _servico.get_modalidade() == 'fds_12', self.servicos_para_completar_list))
        #servicos_para_completar_sab_3 = list(filter(lambda _servico: _servico.get_modalidade() == 'sab_3', self.servicos_para_completar_list))
        #servicos_para_completar_dom_3 = list(filter(lambda _servico: _servico.get_modalidade() == 'dom_3', self.servicos_para_completar_list))
        

    def escalar_militares_tm(self):
        logs_escalar_militares_tm = dict()
        if len(self.cpus_tm) == 0:
            logs_escalar_militares_tm['Militares TM cadastrados'] = "Não há militar cadastrado com função TM."
            return logs_escalar_militares_tm
        else:
            logs_escalar_militares_tm['Militares TM cadastrados'] = "Há {} militar(es) cadastrado(s) com função TM".format(len(self.cpus_tm))
        
        servico_para_completar_seg_2t = [_servico for _servico in self.servicos_para_completar_list if _servico.data.weekday() == 0 and _servico.turno == 2]
        servico_para_completar_ter_2t = [_servico for _servico in self.servicos_para_completar_list if _servico.data.weekday() == 1 and _servico.turno == 2]
        servico_para_completar_dom_2t = [_servico for _servico in self.servicos_para_completar_list if _servico.data.weekday() == 6 and _servico.turno == 2]
        
        if len(servico_para_completar_seg_2t) > 1:
            raise myexceptions.LogicException('A lista Escalar().servicos_para_completar_list deve conter os serviços para serem completados, de segunda a domingo, três turnos por dia. Não pode haver mais de um serviço com dia da semana == segunda-feira e turno == 2. No momento, há {} serviços que atendem estes critérios.'.format(len(servico_para_completar_seg_2t)))
        if len(servico_para_completar_ter_2t) > 1:
            raise myexceptions.LogicException('A lista Escalar().servicos_para_completar_list deve conter os serviços para serem completados, de segunda a domingo, três turnos por dia. Não pode haver mais de um serviço com dia da semana == terça-feira e turno == 2. No momento, há {} serviços que atendem estes critérios.'.format(len(servico_para_completar_ter_2t)))
        if len(servico_para_completar_dom_2t) > 1:
            raise myexceptions.LogicException('A lista Escalar().servicos_para_completar_list deve conter os serviços para serem completados, de segunda a domingo, três turnos por dia. Não pode haver mais de um serviço com dia da semana == domingo e turno == 2. No momento, há {} serviços que atendem estes critérios.'.format(len(servico_para_completar_ter_2t)))

        if len(servico_para_completar_seg_2t) == len(servico_para_completar_ter_2t) == len(servico_para_completar_dom_2t) == 0:
            logs_escalar_militares_tm["Servicos 'TM' para completar"] = "Não há serviços 'TM' para completar."
            return logs_escalar_militares_tm
        else:
            logs_escalar_militares_tm["Servicos 'TM' para completar"] = "Há serviço(s) 'TM' para completar: (seg_2 -> {}); (ter_2 -> {}); (dom_2 -> {}).".format(
                len(servico_para_completar_seg_2t),
                len(servico_para_completar_ter_2t),
                len(servico_para_completar_dom_2t)
            )

        data_segunda_anterior = self.data_segunda - datetime.timedelta(days=7)
        data_terca_anterior = self.data_terca - datetime.timedelta(days=7)
        data_domingo_anterior = self.data_domingo - datetime.timedelta(days=7)

        servico_segunda_anterior_2t = servicodao.ServicoDAO().get_servico(data_segunda_anterior, 2)
        servico_terca_anterior_2t = servicodao.ServicoDAO().get_servico(data_terca_anterior, 2)
        servico_domingo_anterior_2t = servicodao.ServicoDAO().get_servico(data_domingo_anterior, 2)
        
        
        condicao_1_str = "CPU da segunda anterior, 2t, era TM. CPU para terça atual será o mesmo, salvo impedimento."
        condicao_2_str = "CPU do domingo anterior, 2t, era TM, o mesmo da segunda."
        condicao_3_str = "CPU da terça anterior, 2t, era TM. CPU para segunda e domingo atual será o mesmo, salvo impedimento."
        condicao_4_str = "CPU da terça anterior, 2t, era TM e era diferente do CPU no domingo."
        condicao_5_str = "CPU da segunda anterior não era TM, mas do domingo era."
        
        cpu_empenhos_seg_dom = None
        cpu_empenho_ter = None
        
        logs_escalar_militares_tm['Condições'] = dict()
        logs_escalar_militares_tm['Condições']['Cumpridas'] = list()
        logs_escalar_militares_tm['Condições']['Não cumpridas'] = list()

        if servico_segunda_anterior_2t.cpu.funcao == 'TM':
            cpu_empenho_ter = servico_segunda_anterior_2t.cpu
            logs_escalar_militares_tm['Condições']['Cumpridas'].append(condicao_1_str)
            if servico_domingo_anterior_2t.cpu.nome_de_guerra == servico_segunda_anterior_2t.cpu.nome_de_guerra:
                logs_escalar_militares_tm['Condições']['Cumpridas'].append(condicao_2_str)
            else:
                logs_escalar_militares_tm['Condições']['Não cumpridas'].append(condicao_2_str)
        else:
            if servico_domingo_anterior_2t.cpu.funcao == 'TM':
                cpu_empenho_ter = servico_domingo_anterior_2t.cpu
                logs_escalar_militares_tm['Condições']['Cumpridas'].append(condicao_5_str)
            logs_escalar_militares_tm['Condições']['Não cumpridas'].append(condicao_1_str)

        
        if servico_terca_anterior_2t.cpu.funcao == 'TM':            
            cpu_empenhos_seg_dom = servico_terca_anterior_2t.cpu
            logs_escalar_militares_tm['Condições']['Cumpridas'].append(condicao_3_str)
            if servico_terca_anterior_2t.cpu.nome_de_guerra != servico_domingo_anterior_2t.cpu.nome_de_guerra:
                logs_escalar_militares_tm['Condições']['Cumpridas'].append(condicao_4_str)
            else:
                logs_escalar_militares_tm['Condições']['Não cumpridas'].append(condicao_4_str)
        else:
            logs_escalar_militares_tm['Condições']['Não cumpridas'].append(condicao_3_str)
        
        
        if cpu_empenhos_seg_dom != None:                
            if len(servico_para_completar_seg_2t) == 1:
                if cpu_empenhos_seg_dom.nome_de_guerra not in self.impedimentos_por_dia[servico_para_completar_seg_2t[0].data]:
                    servico_para_completar_seg_2t[0].cpu = cpu_empenhos_seg_dom                    
                    
                    self.escalar_e_atualizar_listas(servico_para_completar_seg_2t[0])

                    logs_escalar_militares_tm['seg_2t sucesso'] = True
                    logs_escalar_militares_tm['seg_2t'] = cpu_empenhos_seg_dom.nome_de_guerra
                else:
                    logs_escalar_militares_tm['seg_2t'] = 'O CPU que seria escalado estava com impedimento na data.'                    
                    logs_escalar_militares_tm['seg_2t sucesso'] = False
            else:
                logs_escalar_militares_tm['seg_2t'] = 'Serviço seg_2t já estava preenchido.'
                logs_escalar_militares_tm['seg_2t sucesso'] = False
            
            if len(servico_para_completar_dom_2t) == 1:
                if cpu_empenhos_seg_dom.nome_de_guerra not in self.impedimentos_por_dia[servico_para_completar_dom_2t[0].data]:
                    servico_para_completar_dom_2t[0].cpu = cpu_empenhos_seg_dom                    
                    
                    self.escalar_e_atualizar_listas(servico_para_completar_dom_2t[0])

                    logs_escalar_militares_tm['dom_2t sucesso'] = True
                    logs_escalar_militares_tm['dom_2t'] = cpu_empenhos_seg_dom.nome_de_guerra
                else:
                    logs_escalar_militares_tm['dom_2t'] = 'O CPU que seria escalado estava com impedimento na data.'                    
                    logs_escalar_militares_tm['dom_2t sucesso'] = False
            else:
                logs_escalar_militares_tm['dom_2t'] = 'Serviço dom_2t já estava preenchido.'
                logs_escalar_militares_tm['dom_2t sucesso'] = False

        else:
            logs_escalar_militares_tm['seg_dom_2t'] = 'Não foi possível identificar o próximo CPU no rodízio'
            logs_escalar_militares_tm['seg_2t sucesso'] = False
            logs_escalar_militares_tm['dom_2t sucesso'] = False
        
        if cpu_empenho_ter != None:
            if len(servico_para_completar_ter_2t) == 1:
                if cpu_empenho_ter.nome_de_guerra not in self.impedimentos_por_dia[servico_para_completar_ter_2t[0].data]:
                    servico_para_completar_ter_2t[0].cpu = cpu_empenho_ter
                    
                    self.escalar_e_atualizar_listas(servico_para_completar_ter_2t[0])

                    logs_escalar_militares_tm['ter_2t sucesso'] = True
                    logs_escalar_militares_tm['ter_2t'] = cpu_empenho_ter.nome_de_guerra
                else:
                    logs_escalar_militares_tm['ter_2t'] = 'O CPU que seria escalado estava com impedimento na data.'
                    logs_escalar_militares_tm['ter_2t sucesso'] = False
            else:
                logs_escalar_militares_tm['ter_2t'] = 'Serviço dom_2t já estava preenchido.'
                logs_escalar_militares_tm['ter_2t sucesso'] = False
        else:
            logs_escalar_militares_tm['ter_2t'] = 'Não foi possível identificar o próximo CPU no rodízio'
            logs_escalar_militares_tm['ter_2t sucesso'] = False                
        
        return logs_escalar_militares_tm
    
    def escalar_fds(self):
        servicos_para_completar_fds = list(filter(lambda _servico: _servico.is_weekend(), self.servicos_para_completar_list))
        qtd_servicos_fds_para_completar = len(servicos_para_completar_fds)
        #print(self.impedimentos)
        #for i in self.impedimentos_por_militar.items():
        #    print(i)
        
        impedimentos_por_dia_fds = {data:self.impedimentos_por_dia[data] for data in self.impedimentos_por_dia if data.weekday() in (4, 5, 6)}
        impedimentos_por_dia_fds[self.data_sexta].pop(1)
        impedimentos_por_dia_fds[self.data_sexta].pop(2)

        impedimentos_por_militar_fds = dict()
        for nome_de_guerra, datas in self.impedimentos_por_militar.items():
            impedimentos_por_militar_fds[nome_de_guerra] = dict()
            for data, turnos in datas.items():
                if data.weekday() in (5, 6):
                    impedimentos_por_militar_fds[nome_de_guerra][data] = turnos
                if data.weekday() == 4:
                    if 3 in turnos:
                        impedimentos_por_militar_fds[nome_de_guerra][data] = [3]

        for nome, data_turnos in impedimentos_por_militar_fds.items():
            print(nome, data_turnos)
            for data, turnos in data_turnos.items():
                print(nome, data, turnos)
        
        #for i in impedimentos_por_dia_fds.items():
        #    print(i)
        #print(self.gerenciador_de_filas.filas['qui_3'])

        
        
                
                

        
        
        
        

        servico_para_completar_sab_3 = list(filter(lambda _servico: _servico.get_modalidade() == 'sab_3', self.servicos_para_completar_list))
        if len(servico_para_completar_sab_3):
            sab_3 = servico_para_completar_sab_3[0]
            self.gerenciador_de_filas.filas['fds'].fila.sort(
                key = lambda _cpu: (
                    max(list(map(self.gerenciador_de_filas.number_week_and_year, _cpu.servicos_fds))) if len(_cpu.servicos_fds) else 0,
                    _cpu.get_fds_em_sequencia(),
                    self.gerenciador_de_filas.filas['sab_3'].fila.index(_cpu),
                    max(list(map(lambda _servico: _servico, _cpu.servicos_fds))) if len(_cpu.servicos_fds) else 0
                )
            )
        
            #print(self.gerenciador_de_filas.filas['fds'])
        
        
                
        #servicos_para_completar_fds.sort(
        #    key = lambda _servico: (
        #        _servico.get_ordem_prioridade_fds_para_empenhar(),
        #        _servico.data
        #    )
        #)

        #cpus_empenhos_fds = list()
        #for _cpu in self.gerenciador_de_filas.filas['fds'].fila:
        #    cond1 = _cpu.nome_de_guerra not in self.impedimentos[self.data_sexta]
        #    cond2 = _cpu.nome_de_guerra not in self.impedimentos[self.data_sabado]
        #    cond3 = _cpu.nome_de_guerra not in self.impedimentos[self.data_domingo]

         #   if cond1 or cond2 or cond3:                
         #       cpus_empenhos_fds.append(_cpu)
         #   if len(cpus_empenhos_fds) == 7:
         #       break
        
        #for i in self.impedimentos.items():
        #    print(i)
        
        
        
        #for _servico in self.servicos_para_completar_list:
        #    print(_servico)
        #print('-' * 40 + '\n')

        #for _servico in self.servicos_completos_list:
        #    print(_servico)
        #print('-' * 40 + '\n')
        #

        #print('não completos: {}'.format(len(self.servicos_para_completar_list)))
        #print('completos: {}'.format(len(self.servicos_completos_list)))


        
        
        #for _servico in self.servicos_para_completar_list:            
        #    self.escalar_por_modalidade(_servico)
                
        #print(self.gerenciador_de_filas.filas['fds'])
    
    def escalar_por_modalidade(self, _servico):
        modalidade = _servico.get_modalidade()
        _pula = 0
        next = self.gerenciador_de_filas.filas[modalidade].show_next_membro(pula=_pula)
        while next.nome_de_guerra in self.impedimentos[_servico.data]:
            _pula += 1
            #implementar exceção, para evitar loop infinito
            next = self.gerenciador_de_filas.filas[modalidade].show_next_membro(pula=_pula)
        next = self.gerenciador_de_filas.filas[modalidade].get_next_membro(pula=_pula)
        _servico.cpu = next
        servicodao.ServicoDAO().servico_add(_servico=_servico)
    
    def escalar_por_modalidade_fds(self, _servico):        
        _pula = 0
        next = self.gerenciador_de_filas.filas['fds'].show_next_membro(pula=_pula)
        while next.nome_de_guerra in self.impedimentos[_servico.data]:
            _pula += 1
            #implementar exceção, para evitar loop infinito
            next = self.gerenciador_de_filas.filas[modalidade].show_next_membro(pula=_pula)
        next = self.gerenciador_de_filas.filas['fds'].get_next_membro(pula=_pula)
        index_fila_modalidade = self.gerenciador_de_filas.filas[_servico.get_modalidade()].fila.index(next)

        _servico.cpu = next
        servicodao.ServicoDAO().servico_add(_servico=_servico)
    

            

    def escalar_e_atualizar_listas(self, _servico):
        if not isinstance(_servico, servico.Servico):
            raise TypeError('O argumento deve ser do tipo servico.Servico. Foi passado {}.'.format(str(type(_servico))))
        try:
            index_servico = self.servicos_para_completar_list.index(_servico)
        except ValueError:
            raise myexceptions.LogicException('O método EscalarSemana().escalar_militares_tm() está tentando escalar serviço que já estava completo.')
        servicodao.ServicoDAO().servico_add(_servico=_servico)
        self.servicos_completos_list.append(
            self.servicos_para_completar_list.pop(index_servico)
        )