from dbdao import servicodao, feriadodao
from db import Connection
import datetime
import config

class Escalar:
    def get_dias_e_turnos_para_escalar(self):
        servicodao_instance = servicodao.ServicoDAO()        
        primeira_data_incompleta = servicodao_instance.get_data_com_qtde_de_servicos_incompleta()
        dia_da_semana_num = primeira_data_incompleta.weekday() # 0 para segunda até 6 para domingo
        
        seg_no_periodo = primeira_data_incompleta - datetime.timedelta(days=dia_da_semana_num)
        dom_no_periodo = seg_no_periodo + datetime.timedelta(days=6)
        todas_as_datas_do_periodo = list()

        for num in range(7):            
            todas_as_datas_do_periodo.append(seg_no_periodo + datetime.timedelta(days=num))
        
        connection = Connection()
        conn = connection.getConnection()
        cursor = conn.cursor()

        get_turnos_para_escalar_query = "SELECT data, SUM(turno), COUNT(data) FROM servicos WHERE data BETWEEN '" +\
            datetime.datetime.strftime(seg_no_periodo, '%Y-%m-%d') +\
            "' AND '" + datetime.datetime.strftime(dom_no_periodo, '%Y-%m-%d') + "' GROUP BY data"
        
        cursor.execute(get_turnos_para_escalar_query)
        results = cursor.fetchall()
        turnos_para_escalar_por_data = dict()
        for result in results:
            turnos_para_escalar_por_data[datetime.datetime.strptime(result[0], '%Y-%m-%d')] = self.get_turnos_para_escalar(result[1], result[2])
        
        for data in todas_as_datas_do_periodo:            
            if data not in turnos_para_escalar_por_data:
                turnos_para_escalar_por_data[data] = [1, 2, 3]        
        
        return turnos_para_escalar_por_data

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
        diasETurnosDict = self.get_dias_e_turnos_para_escalar()
        
        feriadodao_instance = feriadodao.FeriadoDAO()
        apenasDias = list(diasETurnosDict)
        feriadosNoPeriodo = feriadoDao.getFeriadosEmPeriodo(min(apenasDias), max(apenasDias))
        
        print('dias e turnos:')
        print(diasETurnosDict)
        print('----------------')

        print('feriados:')
        print(feriadosNoPeriodo)