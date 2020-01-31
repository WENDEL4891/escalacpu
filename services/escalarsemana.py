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
        
        #print(self.gerenciador_de_filas.filas['fds'])
        #print(self.gerenciador_de_filas.filas['sab_3'])
        #print(self.gerenciador_de_filas.filas['dom_3'])

        #print(self.gerenciador_de_filas.filas['sex_3'])
        #print(self.gerenciador_de_filas.filas['dom_3'])
        #print(self.gerenciador_de_filas.filas['fds_12'])
        
        self.escalar_fds()
        #JÁ ESTÁ DEFININDO OS EMPENHOS EM UM DICIONÁRIO. AGORA, BASTA INSERIR NO BANCO DE DADOS
            

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
                
        nomes_disponiveis_fds_em_combinacoes_validas_dicts = self.get_nomes_fds_em_combinacoes_validas()
        combinacao_possivel = nomes_disponiveis_fds_em_combinacoes_validas_dicts[0]

        def escalar_fds_por_dia_turno(
            dia_turno,
            nomes_disponiveis_fds_em_combinacoes_validas_dicts,
            combinacao_possivel
        ):
                        
            if dia_turno in ('sex_3', 'sab_3', 'dom_3'):
                modalidade = dia_turno
            elif dia_turno in ('sab_1', 'sab_2', 'dom_1', 'dom_2'):
                modalidade = 'fds_12'
            else:
                raise myexceptions.LogicException(
                'O o argumento passado não é válido, nesse contexto. A parâmetro dia_turno só recebe algum, dentre os valores: {}.'.format(
                        ', '.join(['sex_3', 'sab_1', 'sab_2', 'sab_3', 'dom_1', 'dom_2', 'dom_3'])
                    )
            )
                                        
            if dia_turno in combinacao_possivel:
                dia_turno_list = [combinacao[dia_turno] for combinacao in nomes_disponiveis_fds_em_combinacoes_validas_dicts]
                dia_turno_list = list(set(dia_turno_list))       
                for _cpu in self.gerenciador_de_filas.filas[modalidade].fila:
                    if _cpu.nome_de_guerra in dia_turno_list:
                        nome_dia_turno = _cpu.nome_de_guerra                                                
                        nova_lista_nomes_disponiveis_fds_em_combinacoes_validas_dicts = list(filter(lambda combinacao: combinacao[dia_turno] == nome_dia_turno, nomes_disponiveis_fds_em_combinacoes_validas_dicts))
                        nova_lista_nomes_disponiveis_fds_em_combinacoes_validas_dicts.sort(key=lambda combinacao: combinacao[list(combinacao)[0]])
                                                
                        while nova_lista_nomes_disponiveis_fds_em_combinacoes_validas_dicts != nomes_disponiveis_fds_em_combinacoes_validas_dicts:
                            for combinacao in nomes_disponiveis_fds_em_combinacoes_validas_dicts:
                                if combinacao not in nova_lista_nomes_disponiveis_fds_em_combinacoes_validas_dicts:
                                    nomes_disponiveis_fds_em_combinacoes_validas_dicts.remove(combinacao)
                            nomes_disponiveis_fds_em_combinacoes_validas_dicts.sort(key=lambda combinacao: combinacao[list(combinacao)[0]])
                        break

            
        # Esta ordem é que será seguida, na atribuição de empenhos
        dias_turnos_ordenados = ['sab_3', 'dom_3', 'sex_3', 'sab_1', 'sab_2', 'dom_1', 'dom_2']
        
        for dia_turno in dias_turnos_ordenados:
            if dia_turno not in combinacao_possivel:
                dias_turnos_ordenados.remove(dia_turno)
       
        for dia_turno in dias_turnos_ordenados:
            escalar_fds_por_dia_turno(
                dia_turno,
                nomes_disponiveis_fds_em_combinacoes_validas_dicts,
                combinacao_possivel
            )
        
        for combinacao in nomes_disponiveis_fds_em_combinacoes_validas_dicts:
            print(combinacao)

    
    def get_nomes_fds_em_combinacoes_validas(self):
        '''
            Retorna os nomes para serem empregados no fim de semana. Usa duas funções declaradas dentro do próprio método.
        '''        
        
        servicos_para_completar_fds = list(filter(lambda _servico: _servico.is_weekend(), self.servicos_para_completar_list))        
        qtd_servicos_para_completar_fds = len(servicos_para_completar_fds)
        
        
        def get_nomes_por_dia_turno_fds(retirar_1=False):
            '''
            Obtém os nomes, buscando na fila de fim de semana, na quantidade necessária, de acordo com a quantidade de serviços que precisam ser completados.
            '''
            
            fila_fds_nomes = list(map(lambda _cpu: _cpu.nome_de_guerra, self.gerenciador_de_filas.filas['fds'].fila))
            total_membros_fila_fds = len(fila_fds_nomes)

            if len(fila_fds_nomes) < qtd_servicos_para_completar_fds:                
                raise myexceptions.LogicException("Não é possível completar os serviços da semana com os militares disponíveis.")

            nomes_selecionados_fds = list(filter(lambda nome: fila_fds_nomes.index(nome) < qtd_servicos_para_completar_fds, fila_fds_nomes))
                        
            def qtd_impedimentos(nome):
                '''
                Retorna a quantidade de impedimentos que o nome possui, de acordo com o atributo self.impediementos_por_militar.
                A função é usada para ordenar os nomes disponíveis, quando é necessário tirar um da fila.
                O nome que tiver mais impedimentos deve ficar no final da lista, para ser substituído.
                '''
                impedimentos = self.impedimentos_por_militar[nome]
                qtd = 0
                for turnos in impedimentos.values():
                    qtd += len(turnos)
                return qtd            


            def get_ordem_fila_fds(nome):
                '''
                Retorna a ordem em que o nome está, na fila de fds, obtida pela estrutura self.gerenciador_de_filas.filas['fds'].
                A função é usada para ordenar os nomes disponíveis, quando é necessário tirar um da fila.
                O primeiro critério de ordenação é a quantidade de impediementos.
                A ordem na fila é o segundo critério, pois, dentre os militares com a mesma quantidade de impedimentos, deve ser substituído aquele que tem maior ordem na fila. Ou seja, que estaria mais longe de ser escalado.
                '''                
                return fila_fds_nomes.index(nome)

            if retirar_1:
                nomes_selecionados_fds.sort(key=lambda nome: (qtd_impedimentos(nome), get_ordem_fila_fds(nome)))                

                nome_retirado = nomes_selecionados_fds.pop(-1)
                self.gerenciador_de_filas.filas['fds'].fila.remove(cpudao.CpuDAO().get_cpu(nome_retirado))
                fila_fds_nomes.remove(nome_retirado)
                nomes_selecionados_fds.append(fila_fds_nomes[qtd_servicos_para_completar_fds -1])            
                        
                                  
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
            
            dias_turnos_list = list(nomes_disponiveis_por_dia_turno_fds)
                       
            combinacoes_validas_list = list()

            for nomes in nomes_disponiveis_por_dia_turno_fds.items():
                if not len(nomes):
                    return combinacoes_validas_list

            combinacoes_possiveis = itertools.product(
                nomes_disponiveis_por_dia_turno_fds['sex_3'] if 'sex_3' in dias_turnos_list else ['aux'],
                nomes_disponiveis_por_dia_turno_fds['sab_1'] if 'sab_1' in dias_turnos_list else ['aux'],
                nomes_disponiveis_por_dia_turno_fds['sab_2'] if 'sab_2' in dias_turnos_list else ['aux'],
                nomes_disponiveis_por_dia_turno_fds['sab_3'] if 'sab_3' in dias_turnos_list else ['aux'],
                nomes_disponiveis_por_dia_turno_fds['dom_1'] if 'dom_1' in dias_turnos_list else ['aux'],
                nomes_disponiveis_por_dia_turno_fds['dom_2'] if 'dom_2' in dias_turnos_list else ['aux'],
                nomes_disponiveis_por_dia_turno_fds['dom_3'] if 'dom_3' in dias_turnos_list else ['aux'],

            )            
            dias_turnos_ordenados = ['sex_3', 'sab_1', 'sab_2', 'sab_3', 'dom_1', 'dom_2', 'dom_3']
            for dia_turno in dias_turnos_ordenados:
                if dia_turno not in dias_turnos_list:
                    dias_turnos_ordenados.remove(dia_turno)
            
            for combinacao in combinacoes_possiveis:
                combinacao_list = list(combinacao)                                
                for nome in combinacao_list:
                    if nome == 'aux':
                        combinacao_list.remove(nome)                        

                combinacao_set = set(combinacao_list)
                
                if len(set(combinacao_set)) == qtd_servicos_para_completar_fds:
                    combinacao_valida = dict()
                    for i in range(len(combinacao_list)):
                        combinacao_valida[dias_turnos_ordenados[i]] = combinacao_list[i]
                    combinacoes_validas_list.append(combinacao_valida)
                        
            return combinacoes_validas_list

                
        nomes_fds = get_nomes_por_dia_turno_fds()      
        
        combinacoes_validas_list = get_combinacoes(nomes_fds)
        
        while len(combinacoes_validas_list) == 0:            
            nomes_fds = get_nomes_por_dia_turno_fds(retirar_1=True)
            combinacoes_validas_list = get_combinacoes(nomes_fds)            
        
        return combinacoes_validas_list
               
    
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