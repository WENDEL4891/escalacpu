from db import connection
from dbdao import servicodao, feriadodao, cpudao, impedimentodao
from entities import filapormodalidade, servico
from services import functions, gerenciadordefilas
import datetime
import config
import sys
import myexceptions
import pprint
import itertools
import functools

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
        

        #pp = pprint.PrettyPrinter(indent=4)

        #for mens in logs_escalar_militares_tm.items():
        #    pp.pprint(mens)
        
        self.escalar_fds()
    
        
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

        #impedimentos_por_militar_fds = dict()
        #for nome_de_guerra, datas in self.impedimentos_por_militar.items():
        #    impedimentos_por_militar_fds[nome_de_guerra] = dict()
        #    for data, turnos in datas.items():
        #        if data.weekday() in (5, 6):
        #            impedimentos_por_militar_fds[nome_de_guerra][data] = turnos
        #        if data.weekday() == 4:
        #            if 3 in turnos:
        #                impedimentos_por_militar_fds[nome_de_guerra][data] = [3]
                
              
       
        nomes_combinacoes = self.get_nomes_fds()
        #for n in nomes_combinacoes:
        #    print(n)        
    
    def get_nomes_fds(self):
        '''
            Retorna os nomes para serem empregados no fim de semana. Usa duas funções declaradas dentro do próprio método.
        '''
        #print(self.gerenciador_de_filas.filas['fds'])
        
        servicos_para_completar_fds = list(filter(lambda _servico: _servico.is_weekend(), self.servicos_para_completar_list))
        modalidades_para_completar_fds = list(map(lambda _servico: _servico.get_modalidade(), servicos_para_completar_fds))
        qtd_servicos_para_completar_fds = len(servicos_para_completar_fds)
        
        fila_fds_nome = list(map(lambda _cpu: _cpu.nome_de_guerra, self.gerenciador_de_filas.filas['fds'].fila))
        total_membros_fila_fds = len(fila_fds_nome)
        
        def get_nomes_por_dia_turno_fds(substituicao=0):            
            if qtd_servicos_para_completar_fds + substituicao > total_membros_fila_fds:
                print('subs', substituicao)
                raise myexceptions.LogicException('Há apenas {} nomes na fila de fds. Não há membro de índice {} ou superior.'.format(total_membros_fila_fds, total_membros_fila_fds))

            nomes_selecionados_fds = list(filter(lambda nome: fila_fds_nome.index(nome) < qtd_servicos_para_completar_fds, fila_fds_nome))
                        
            def qtd_impedimentos(nome):
                '''
                Retorna a quantidade de impedimentos que o nome possui, de acordo com o atributo self.impediementos_por_militar.
                '''
                impedimentos = self.impedimentos_por_militar[nome]
                qtd = 0
                for turnos in impedimentos.values():
                    qtd += len(turnos)
                return qtd            


            def get_ordem_fila_fds(nome):
                '''
                Retorna a ordem em que o nome está, na fila de fds, obtida pela estrutura self.gerenciador_de_filas.filas['fds']
                '''                
                return fila_fds_nome.index(nome)

            if substituicao != 0:
                nomes_selecionados_fds.sort(key=lambda nome: (qtd_impedimentos(nome), get_ordem_fila_fds(nome)))

                nomes_selecionados_fds.pop(-1)
                nomes_selecionados_fds.append(fila_fds_nome[qtd_servicos_para_completar_fds -1 + substituicao])
                        
                                  
            impedimentos_por_dia_turno_fds = dict()
            for data, dict_turnos in self.impedimentos_por_dia.items():            
                if data.weekday() == 4:
                    for turno, nomes_de_guerra in dict_turnos.items():
                        if turno == 3:
                            impedimentos_por_dia_turno_fds['{}_{}'.format(config.dias_da_semana[data.weekday()], turno)] = nomes_de_guerra
                if data.weekday() in (5, 6):
                    for turno, nomes_de_guerra in dict_turnos.items():
                        impedimentos_por_dia_turno_fds['{}_{}'.format(config.dias_da_semana[data.weekday()], turno)] = nomes_de_guerra
                        
            nomes_disponiveis_por_dia_turno_fds = {
                dia_turno:list(set(nomes_selecionados_fds) - set(nomes)) for dia_turno, nomes in impedimentos_por_dia_turno_fds.items() if dia_turno in list(map(lambda _servico: "{}_{}".format(config.dias_da_semana[_servico.data.weekday()], _servico.turno), self.servicos_para_completar_list))
            }
            
            return nomes_disponiveis_por_dia_turno_fds
                
        def get_combinacoes(nomes_disponiveis_por_dia_turno_fds):
           
            dias_turnos_para_completar_list = list(nomes_disponiveis_por_dia_turno_fds)            
            qtd_dias_turno_para_completar = len(dias_turnos_para_completar_list)

            combinacoes = list()
            for i in range(qtd_dias_turno_para_completar):
                if i == 1:
                    combinacao = list()
                for nome in nomes_disponiveis_por_dia_turno_fds[dias_turnos_para_completar_list[i]]:
                    
                    

                for nomes in nomes_disponiveis_por_dia_turno_fds[dias_turnos_para_completar_list[i]]:

            
            """  for modalidade, nomes in nomes_disponiveis_por_dia_turno_fds.items():
                if 'combinacao' not in locals():
                    combinacao = list()
                   

                print(modalidade, nomes)
                
            print('#' * 40) """

            
            return combinacoes
        
               
        total_membros_fila_fds = len(self.gerenciador_de_filas.filas['fds'].fila)
        nomes_fds = get_nomes_por_dia_turno_fds()
        #for n in nomes_fds.items():
        #    print(n)    
        #print('-' * 40)
        combinacoes = get_combinacoes(nomes_fds)
        substituicao = 0
        while len(combinacoes) == 0:
            substituicao += 1
            nomes_fds = get_nomes_por_dia_turno_fds(substituicao)
            combinacoes = get_combinacoes(nomes_fds)
                
        #print('substituição: {}'.format(substituicao))
        #print(self.gerenciador_de_filas.filas['fds'])
        return nomes_fds


        
        
        
        
        """ count = 0
        for combinacao in itertools.product(
            nomes_disponiveis_por_dia_turno["sex_3"],
            nomes_disponiveis_por_dia_turno["sab_1"],
            nomes_disponiveis_por_dia_turno["sab_2"],
            nomes_disponiveis_por_dia_turno["sab_3"],
            nomes_disponiveis_por_dia_turno["dom_1"],
            nomes_disponiveis_por_dia_turno["dom_2"],
            nomes_disponiveis_por_dia_turno["dom_3"]
        ):
            count += 1
            print(len(set(combinacao)), combinacao)
            if len(set(combinacao)) == 7:
                print("count: {}.".format(count))
                combinacoes_nao_suficientes = False
                break """
        
        
    
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