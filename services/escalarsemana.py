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

        self.feriados = feriadodao.FeriadoDAO().get_feriados(self.data_segunda, self.data_domingo)
        self.impedimentos_da_semana = impedimentodao.ImpedimentoDAO().get_impedimentos_from_date(self.data_segunda, self.data_domingo)
        
        self.cpus = cpudao.CpuDAO().get_cpus()
        self.cpus_tm = list(filter(lambda _cpu: _cpu.funcao == 'TM', self.cpus))
        self.cpus_nao_tm = list(filter(lambda _cpu: _cpu.funcao != 'TM', self.cpus))

        self.servicos_tm_escalados = list()
    
    @property
    def impedimentos_da_semana(self):
        return self.__impedimentos_da_semana
    
    @impedimentos_da_semana.setter
    def impedimentos_da_semana(self, impedimentos_obj_list):
        impedimentos_da_semana = dict()
        for impedimento_obj in impedimentos_obj_list:
            data = impedimento_obj.data_inicio
            while data <= impedimento_obj.data_fim:
                if data in self.dias_e_turnos_seg_a_dom_dict.keys():
                    if data in impedimentos_da_semana.keys():
                        impedimentos_da_semana[data].append(impedimento_obj.nome_de_guerra)
                    else:
                        impedimentos_da_semana[data] = [impedimento_obj.nome_de_guerra]
                data += datetime.timedelta(days=1)
        self.__impedimentos_da_semana = impedimentos_da_semana

       
    def escalar_seg_a_dom(self, escalar_tm=True):

        if escalar_tm:
            logs_escalar_militares_tm = self.escalar_militares_tm()
        
        pp = pprint.PrettyPrinter(indent=4)

        for mens in logs_escalar_militares_tm.items():
            pp.pprint(mens)
        
        servicos_para_completar_fds = list(filter(lambda _servico: _servico.is_weekend(), self.servicos_para_completar_list))
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
        
        dois_meses_antes = max(self.dias_e_turnos_seg_a_dom_dict) - datetime.timedelta(days=65)
        gerenciador_de_filas = gerenciadordefilas.GerenciadorDeFilas(dois_meses_antes, max(self.dias_e_turnos_seg_a_dom_dict))

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
            logs_escalar_militares_tm["Servicos 'TM' para completar"] = "Há serviço(s) 'TM' para completar: {} seg_2; {} ter_2; {} dom_2".format(
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
        
        
        # CPU da segunda anterior, 2t, era TM. CPU para terça atual será o mesmo, salvo impedimento.
        condicao_1 = servico_segunda_anterior_2t.cpu.funcao == 'TM'

        # CPU do domingo anterior, 2t, era TM, o mesmo da segunda.
        condicao_2 = condicao_1 and servico_domingo_anterior_2t.cpu.nome_de_guerra == servico_segunda_anterior_2t.cpu.nome_de_guerra


        # CPU da terça anterior, 2t, era TM. CPU para segunda e domingo atual será o mesmo, salvo impedimento.
        condicao_3 = servico_terca_anterior_2t.cpu.funcao == 'TM'

        # CPU da terça anterior, 2t, era TM e era diferente do CPU no domingo.
        condicao_4 = condicao_3 and servico_terca_anterior_2t.cpu.nome_de_guerra != servico_domingo_anterior_2t.cpu.nome_de_guerra

        condicao_1_str = "CPU da segunda anterior, 2t, era TM. CPU para terça atual será o mesmo, salvo impedimento."
        condicao_2_str = "CPU do domingo anterior, 2t, era TM, o mesmo da segunda."
        condicao_3_str = "CPU da terça anterior, 2t, era TM. CPU para segunda e domingo atual será o mesmo, salvo impedimento."
        condicao_4_str = "CPU da terça anterior, 2t, era TM e era diferente do CPU no domingo."
        
        cpu_empenhos_seg_dom = None
        cpu_empenho_ter = None
        
        logs_escalar_militares_tm['Condições'] = dict()
        logs_escalar_militares_tm['Condições']['Cumpridas'] = list()
        logs_escalar_militares_tm['Condições']['Não cumpridas'] = list()

        if condicao_1:            
            cpu_empenho_ter = servico_segunda_anterior_2t.cpu
            logs_escalar_militares_tm['Condições']['Cumpridas'].append(condicao_1_str)
        else:
            logs_escalar_militares_tm['Condições']['Não cumpridas'].append(condicao_1_str)

        
        if condicao_2:
            logs_escalar_militares_tm['Condições']['Cumpridas'].append(condicao_2_str)
        else:
            logs_escalar_militares_tm['Condições']['Não cumpridas'].append(condicao_2_str)
        
        if condicao_3:            
            cpu_empenhos_seg_dom = servico_terca_anterior_2t.cpu
            logs_escalar_militares_tm['Condições']['Cumpridas'].append(condicao_3_str)
        else:
            logs_escalar_militares_tm['Condições']['Não cumpridas'].append(condicao_3_str)

        if condicao_4:            
            logs_escalar_militares_tm['Condições']['Cumpridas'].append(condicao_4_str)
        else:
            logs_escalar_militares_tm['Condições']['Não cumpridas'].append(condicao_4_str)
        
        
        if len(servico_para_completar_seg_2t) == 1:
            if cpu_empenhos_seg_dom != None:
                if cpu_empenhos_seg_dom.nome_de_guerra not in self.impedimentos_da_semana[servico_para_completar_seg_2t[0].data]:
                    servico_para_completar_seg_2t[0].cpu = cpu_empenhos_seg_dom                    
                    servicodao.ServicoDAO().servico_add(_servico=servico_para_completar_seg_2t[0])
                    logs_escalar_militares_tm['seg_2t sucesso'] = True
                else:
                    logs_escalar_militares_tm['seg_2t'] = 'O CPU que seria escalado estava com impedimento na data.'                    
                    logs_escalar_militares_tm['seg_2t sucesso'] = False
            else:
                logs_escalar_militares_tm['seg_2t'] = 'Não foi possível identificar o próximo CPU no rodízio'
                logs_escalar_militares_tm['seg_2t sucesso'] = False
        else:
            logs_escalar_militares_tm['seg_2t'] = 'Serviço seg_2t já estava preenchido.'
            logs_escalar_militares_tm['seg_2t sucesso'] = False
        
        return logs_escalar_militares_tm

        
        #for data, nome_de_guerra in self.impedimentos_da_semana.items():
        #    print(config.dias_da_semana[data.weekday()], nome_de_guerra)
        
        

        