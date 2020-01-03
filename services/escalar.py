from db import connection
from dbdao import servicodao, feriadodao, cpudao
from entities import filapormodalidade, servico
from services import functions, gerenciadordefilas
import datetime
import config
import sys

class Escalar:
    def get_dias_e_turnos_para_escalar(self):        
        primeira_data_incompleta = servicodao.ServicoDAO().get_data_com_qtde_de_servicos_incompleta()        
        dia_da_semana_num = primeira_data_incompleta.weekday() # 0 para segunda até 6 para domingo        
        seg_no_periodo = primeira_data_incompleta - datetime.timedelta(days=dia_da_semana_num)
        dom_no_periodo = seg_no_periodo + datetime.timedelta(days=6)
        todas_as_datas_do_periodo_in_list = list()

        for num in range(7):            
            todas_as_datas_do_periodo_in_list.append(seg_no_periodo + datetime.timedelta(days=num))
        
        try:        
            _connection = connection.Connection()
            conn = _connection.get_connection()
            cursor = conn.cursor()

            seg_no_periodo_format = datetime.datetime.strftime(seg_no_periodo, '%Y-%m-%d')
            dom_no_periodo_format = datetime.datetime.strftime(dom_no_periodo, '%Y-%m-%d')

            get_turnos_para_escalar_query = """
            SELECT
                data,
                SUM(turno),
                COUNT(data)
            FROM servicos
            WHERE
                data BETWEEN '{}' AND '{}'
            GROUP BY data
            ORDER BY data
            """.format(seg_no_periodo_format, dom_no_periodo_format)
            
            cursor.execute(get_turnos_para_escalar_query)
            results = cursor.fetchall()
        except:
            erros = sys.exc_info()
            for i in range(len(erros) - 1):
                print(erros[i])
                raise
        finally:
            if 'conn' in locals():
                conn.close()
        turnos_para_escalar_por_data_dict = dict()
        for result in results:
            data = functions.date_str_to_datetime(result[0])
            soma_turnos = result[1]
            conta_servicos = result[2]
            turnos_para_escalar_por_data_dict[data] = self.get_turnos_para_escalar(soma_turnos, conta_servicos)
        
        for data in todas_as_datas_do_periodo_in_list:            
            if data not in turnos_para_escalar_por_data_dict:
                turnos_para_escalar_por_data_dict[data] = [1, 2, 3]        
        return turnos_para_escalar_por_data_dict

    def get_turnos_para_escalar(self, soma_turnos, cont_datas):        
        if soma_turnos == 0:
            return [1, 2, 3]

        elif soma_turnos == 1:
            return [2, 3]

        elif soma_turnos == 2:
            return [1, 3]

        elif soma_turnos == 3:
            if cont_datas == 1:
                return [1, 2]
            elif cont_datas == 2:
                return [3]            

        elif soma_turnos == 4:
            return [2]

        elif soma_turnos == 5:
            return [1]
        
        elif soma_turnos == 6:
            return[]
       
    def escalar_seg_a_dom(self):
        dias_e_turnos_seg_a_dom_dict = self.get_dias_e_turnos_para_escalar()
        servicos_para_completar_list = list()
        for data, turnos in dias_e_turnos_seg_a_dom_dict.items():
            for turno in turnos:
                servicos_para_completar_list.append(servico.Servico(data, turno))
        
        #for s in servicos_para_completar_list:
        #    servicodao.ServicoDAO().servico_add(s.data, s.turno, 'MADUREIRA')

        
        seg_dom_atual = list(filter(lambda data: data.weekday() in (0, 6), dias_e_turnos_seg_a_dom_dict))
        ter_atual = list(filter(lambda data: data.weekday() == 1, dias_e_turnos_seg_a_dom_dict))                
        
        seg_dom_semana_anterior = list(map(lambda data: data - datetime.timedelta(days=7), seg_dom_atual))
        ter_semana_anterior = list(map(lambda data: data - datetime.timedelta(days=7), ter_atual))
        
                
        servicos_tm_A_semana_anterior = list(map(lambda data: servicodao.ServicoDAO().get_servico(data, 2), seg_dom_semana_anterior))
        servicos_tm_B_semana_anterior = list(map(lambda data: servicodao.ServicoDAO().get_servico(data, 2), ter_semana_anterior))

        
        #servicos_para_completar_fds = list(filter(lambda _servico: _servico.is_weekend(), servicos_para_completar_list))
        #servicos_para_completar_semana = list(filter(lambda _servico: not _servico.is_weekend(), servicos_para_completar_list))
        #servicos_para_completar_seg_12 = list(filter(lambda _servico: _servico.get_modalidade() == 'seg_12', servicos_para_completar_list))
        #servicos_para_completar_seg_3 = list(filter(lambda _servico: _servico.get_modalidade() == 'seg_3', servicos_para_completar_list))
        #servicos_para_completar_ter_qui_sex_12 = list(filter(lambda _servico: _servico.get_modalidade() == 'ter_qui_sex_12', servicos_para_completar_list))
        #servicos_para_completar_qua_12 = list(filter(lambda _servico: _servico.get_modalidade() == 'qua_12', servicos_para_completar_list))
        #servicos_para_completar_ter_3 = list(filter(lambda _servico: _servico.get_modalidade() == 'ter_3', servicos_para_completar_list))
        #servicos_para_completar_qua_3 = list(filter(lambda _servico: _servico.get_modalidade() == 'qua_3', servicos_para_completar_list))
        #servicos_para_completar_qui_3 = list(filter(lambda _servico: _servico.get_modalidade() == 'qui_3', servicos_para_completar_list))
        #servicos_para_completar_sex_3 = list(filter(lambda _servico: _servico.get_modalidade() == 'sex_3', servicos_para_completar_list))
        #servicos_para_completar_fds_12 = list(filter(lambda _servico: _servico.get_modalidade() == 'fds_12', servicos_para_completar_list))
        #servicos_para_completar_sab_3 = list(filter(lambda _servico: _servico.get_modalidade() == 'sab_3', servicos_para_completar_list))
        #servicos_para_completar_dom_3 = list(filter(lambda _servico: _servico.get_modalidade() == 'dom_3', servicos_para_completar_list))
        
        dois_meses_antes = max(dias_e_turnos_seg_a_dom_dict) - datetime.timedelta(days=65)
        gerenciador_de_filas = gerenciadordefilas.GerenciadorDeFilas(dois_meses_antes, max(dias_e_turnos_seg_a_dom_dict))

        servicos = sorted(gerenciador_de_filas.servicos_em_ordem_decrescente)
        for s in servicos:
            print(s)
            print(s.get_modalidade())
            print('-' * 40)
                
        #for c in gerenciador_de_filas.fila_fds.fila:
        #    print(c.nome_de_guerra, c.fds_em_sequencia)
        
        #for _cpu in gerenciador_de_filas.fila_fds.fila:
        #    print('{:10} | fds em sequencia > {}'.format(_cpu.nome_de_guerra, _cpu.get_fds_em_sequencia()))
        #    print(max(_cpu.servicos_fds) if len(_cpu.servicos_fds) else '---')
        #    print('-' * 40)
        #print(gerenciador_de_filas.fila_fds)
        #print(gerenciador_de_filas.fila_fds.show_next_membro())

        


        

            
        


        
        #count1 = 0
        #count2 = 0
        #print('servicos_para_completar_fds')
        #count1 += len(servicos_para_completar_fds)
        #for s in servicos_para_completar_fds:
        #    print(s)
        #print('-' * 30)
        #print('\n')
        #print('servicos_para_completar_semana')
        #count1 += len(servicos_para_completar_semana)
        #for s in servicos_para_completar_semana:
        #    print(s)
        #print('-' * 30)
        #print('\n')
        #print('servicos_para_completar_seg_12')
        #count2 += len(servicos_para_completar_seg_12)
        #for s in servicos_para_completar_seg_12:
        #    print(s)
        #print('-' * 30)
        #print('\n')
        #print('servicos_para_completar_seg_3')
        #count2 += len(servicos_para_completar_seg_3)
        #for s in servicos_para_completar_seg_3:
        #    print(s)
        #print('-' * 30)
        #print('\n')
        #print('servicos_para_completar_ter_qui_sex_12')
        #count2 += len(servicos_para_completar_ter_qui_sex_12)
        #for s in servicos_para_completar_ter_qui_sex_12:
        #    print(s)
        #print('-' * 30)
        #print('\n')
        #print('servicos_para_completar_qua_12')
        #count2 += len(servicos_para_completar_qua_12)
        #for s in servicos_para_completar_qua_12:
        #    print(s)
        #print('-' * 30)
        #print('\n')
        #print('servicos_para_completar_ter_3')
        #count2 += len(servicos_para_completar_ter_3)
        #for s in servicos_para_completar_ter_3:
        #    print(s)
        #print('-' * 30)
        #print('\n')
        #print('servicos_para_completar_qua_3')
        #count2 += len(servicos_para_completar_qua_3)
        #for s in servicos_para_completar_qua_3:
        #    print(s)
        #print('-' * 30)
        #print('\n')
        #print('servicos_para_completar_qui_3')
        #count2 += len(servicos_para_completar_qui_3)
        #for s in servicos_para_completar_qui_3:
        #    print(s)
        #print('-' * 30)
        #print('\n')
        #print('servicos_para_completar_sex_3')
        #count2 += len(servicos_para_completar_sex_3)
        #for s in servicos_para_completar_sex_3:
        #    print(s)
        #print('-' * 30)
        #print('\n')
        #print('servicos_para_completar_fds_12')
        #count2 += len(servicos_para_completar_fds_12)
        #for s in servicos_para_completar_fds_12:
        #    print(s)
        #print('-' * 30)
        #print('\n')
        #print('servicos_para_completar_sab_3')
        #count2 += len(servicos_para_completar_sab_3)
        #for s in servicos_para_completar_sab_3:
        #    print(s)
        #print('-' * 30)
        #print('\n')
        #print('servicos_para_completar_dom_3')
        #count2 += len(servicos_para_completar_dom_3)
        #for s in servicos_para_completar_dom_3:
        #    print(s)
        #print('-' * 30)
        #print('\n')
        #print('count1: {}'.format(count1))
        #print('count2: {}'.format(count2))
        
        
        

        
        
        #seg_format = datetime.datetime.strftime(segunda_feira, '%Y-%m-%d')
        #dom_format = datetime.datetime.strftime(domingo, '%Y-%m-%d')
        #feriados_no_periodo = feriadodao.FeriadoDAO().get_feriados(seg_format, dom_format)
        
        #print('dias e turnos:')
        #print(dias_e_turnos_seg_a_dom_dict)
        #print('----------------')

        #print('feriados:')
        #print(feriados_no_periodo)