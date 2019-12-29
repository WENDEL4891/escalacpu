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
        for _servico in servicos_para_completar_list:
            print(_servico)
        
        
        dois_meses_antes = max(dias_e_turnos_seg_a_dom_dict) - datetime.timedelta(days=65)
        
        
        gerenciador_de_filas = gerenciadordefilas.GerenciadorDeFilas(dois_meses_antes, max(dias_e_turnos_seg_a_dom_dict))

        now = datetime.datetime.now().date()
        now_str = '28/12/2019'
        

        #print(functions.classifica_servico_por_modalidade(now, 2))
        #print(functions.classifica_servico_por_modalidade(now_str, 3))        
        
        #seg_format = datetime.datetime.strftime(segunda_feira, '%Y-%m-%d')
        #dom_format = datetime.datetime.strftime(domingo, '%Y-%m-%d')
        #feriados_no_periodo = feriadodao.FeriadoDAO().get_feriados(seg_format, dom_format)
        
        #print('dias e turnos:')
        #print(dias_e_turnos_seg_a_dom_dict)
        #print('----------------')

        #print('feriados:')
        #print(feriados_no_periodo)