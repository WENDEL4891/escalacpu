from db import connection
from dbdao import servicodao, feriadodao, cpudao
from entities import filapormodalidade, servico
from services import functions, gerenciadordefilas
import datetime
import config
import sys
import myexceptions

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
        
       
    def escalar_seg_a_dom(self):

        self.escalar_militares_tm()
        
        
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
        servico_para_completar_seg_2t = [_servico for _servico in self.servicos_para_completar_list if _servico.data.weekday() == 0 and _servico.turno == 2]
        servico_para_completar_ter_2t = [_servico for _servico in self.servicos_para_completar_list if _servico.data.weekday() == 1 and _servico.turno == 2]
        servico_para_completar_dom_2t = [_servico for _servico in self.servicos_para_completar_list if _servico.data.weekday() == 6 and _servico.turno == 2]
        if len(servico_para_completar_seg_2t) > 1:
            raise myexceptions.LogicException('A lista Escalar().servicos_para_completar_list deve conter os serviços para serem completados, de segunda a domingo, três turnos por dia. Não pode haver mais de um serviço com dia da semana == segunda-feira e turno == 2. No momento, há {} serviços que atendem estes critérios.'.format(len(servico_para_completar_seg_2t)))
        if len(servico_para_completar_ter_2t) > 1:
            raise myexceptions.LogicException('A lista Escalar().servicos_para_completar_list deve conter os serviços para serem completados, de segunda a domingo, três turnos por dia. Não pode haver mais de um serviço com dia da semana == terça-feira e turno == 2. No momento, há {} serviços que atendem estes critérios.'.format(len(servico_para_completar_ter_2t)))
        if len(servico_para_completar_dom_2t) > 1:
            raise myexceptions.LogicException('A lista Escalar().servicos_para_completar_list deve conter os serviços para serem completados, de segunda a domingo, três turnos por dia. Não pode haver mais de um serviço com dia da semana == domingo e turno == 2. No momento, há {} serviços que atendem estes critérios.'.format(len(servico_para_completar_ter_2t)))

        if len(servico_para_completar_seg_2t) == 1:            
            data_terca_anterior = self.data_terca - datetime.timedelta(days=7)
            servico_terca_anterior = servicodao.ServicoDAO().get_servico(data_terca_anterior, 2)
        
        for f in self.feriados:
            print(f)
        

                
        

        seg_dom_atual = list(filter(lambda data: data.weekday() in (0, 6), self.dias_e_turnos_seg_a_dom_dict))
        ter_atual = list(filter(lambda data: data.weekday() == 1, self.dias_e_turnos_seg_a_dom_dict))                
        
        seg_dom_semana_anterior = list(map(lambda data: data - datetime.timedelta(days=7), seg_dom_atual))
        ter_semana_anterior = list(map(lambda data: data - datetime.timedelta(days=7), ter_atual))
        
                
        servicos_tm_A_semana_anterior = list(map(lambda data: servicodao.ServicoDAO().get_servico(data, 2), seg_dom_semana_anterior))
        servicos_tm_B_semana_anterior = list(map(lambda data: servicodao.ServicoDAO().get_servico(data, 2), ter_semana_anterior))
        
        
