from dbdao import ServicoDAO, FeriadoDAO
from db import Connection
import datetime
import config

class Escalar:
    def getDiasETurnosParaEscalar(self):
        servicoDao = ServicoDAO()        
        primeiraDataIncompleta = servicoDao.getDataComQtdDeServicosIncompleta()        
        diaDaSemanaNum = primeiraDataIncompleta.weekday() # 0 para segunda até 6 para domingo
        
        segNoPeriodo = primeiraDataIncompleta - datetime.timedelta(days=diaDaSemanaNum)
        domNoPeriodo = segNoPeriodo + datetime.timedelta(days=6)
        todasAsDatasDoPeriodo = list()

        for num in range(7):            
            todasAsDatasDoPeriodo.append(segNoPeriodo + datetime.timedelta(days=num))
        
        connection = Connection()
        conn = connection.getConnection()
        cursor = conn.cursor()

        getTurnosParaEscalarQuery = "SELECT data, SUM(turno), COUNT(data) FROM servicos WHERE data BETWEEN '" +\
            datetime.datetime.strftime(segNoPeriodo, '%Y-%m-%d') +\
            "' AND '" + datetime.datetime.strftime(domNoPeriodo, '%Y-%m-%d') + "' GROUP BY data"
        
        cursor.execute(getTurnosParaEscalarQuery)
        results = cursor.fetchall()
        turnosParaEscalarPorData = dict()
        for result in results:
            turnosParaEscalarPorData[datetime.datetime.strptime(result[0], '%Y-%m-%d')] = self.getDiasParaEscalar(result[1], result[2])
        
        for data in todasAsDatasDoPeriodo:            
            if data not in turnosParaEscalarPorData:
                turnosParaEscalarPorData[data] = [1, 2, 3]        
        
        return turnosParaEscalarPorData

    def getDiasParaEscalar(self, somaTurnos, contDatas):        
        if somaTurnos == 0:
            return [1, 2, 3]

        elif somaTurnos == 1:
            return [2, 3]

        elif somaTurnos == 2:
            return [1, 3]

        elif somaTurnos == 3:
            if contDatas == 1:
                return [1, 2]
            elif contDatas == 2:
                return [3]            

        elif somaTurnos == 4:
            return [2]

        elif somaTurnos == 5:
            return [1]
        
        elif somaTurnos == 6:
            return[]
       
    def escalarSeg_Sex(self):
        diasETurnosDict = self.getDiasETurnosParaEscalar()
        
        feriadoDao = FeriadoDAO()
        apenasDias = list(diasETurnosDict)
        feriadosNoPeriodo = feriadoDao.getFeriadosEmPeriodo(min(apenasDias), max(apenasDias))
        
        print('dias e turnos:')
        print(diasETurnosDict)
        print('----------------')

        print('feriados:')
        print(feriadosNoPeriodo)