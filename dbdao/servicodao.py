import datetime
import db
import entities
import config
import sys


class ServicoDAO:
    def __init__(self):
        self.primeiraDataDeServico = datetime.datetime.strptime(config.primeiraData, '%d/%m/%Y')

    def servicoAdd(self, nome, data, turno):        
        servico = entities.servico.Servico(nome, data, turno)
        connection = db.connection.db.connection.Connection()
        conn = connection.getConnection()
        cursor = conn.cursor()

        insertServico = 'INSERT INTO servicos (nome, data, turno) VALUES (?, ?, ?)'
        cursor.execute(insertServico, (servico.nome, servico.data, servico.turno))
        conn.commit()
        conn.close()
    
    def getServicos(self):
        connection = db.connection.Connection()
        conn = connection.getConnection()
        cursor = conn.cursor()

        getServicosQuery = 'SELECT nome, data, turno FROM servicos'

        cursor.execute(getServicosQuery)
        results = cursor.fetchall()
        conn.close()
        return results
    
    def getQtdDeServicosPorDia(self):
        connection = db.connection.Connection()
        conn = connection.getConnection()
        cursor = conn.cursor()

        getContagem = "SELECT data, SUM(turno), COUNT(data) FROM servicos GROUP BY data;"

        cursor.execute(getContagem)
        qtdServicosPorDiaList = cursor.fetchall()
        conn.close()
        qtdServicosPorDiaDict = dict()        
        for el in qtdServicosPorDiaList:
            qtdServicosPorDiaDict[datetime.datetime.strptime(el[0], '%Y-%m-%d')] = {'somaTurnos':el[1], 'contDatas': el[2]}
        return qtdServicosPorDiaDict
    
    def getServicosToData(self, data):
        data = datetime.datetime.strptime(data, '%d/%m/%Y')
        dataFormat = datetime.datetime.strftime(data, '%Y-%m-%d')
        print(dataFormat)
        connection = db.connection.Connection()
        conn = connection.getConnection()
        cursor = conn.cursor()

        getSericosToDataQuery = "SELECT nome, data, turno FROM servicos WHERE data <= DATE("+ "'" + dataFormat + "'" +")"
        cursor.execute(getSericosToDataQuery)
        print(getSericosToDataQuery)
        servicosInList = cursor.fetchall()
        return servicosInList
        
    def getDataComQtdDeServicosIncompleta(self):        
        data = self.primeiraDataDeServico
        qtdDeServicosPorDiaDict = self.getQtdDeServicosPorDia()
        datasList = list(qtdDeServicosPorDiaDict)
                
        while(True):                        
            if data in datasList:
                if qtdDeServicosPorDiaDict[data]['somaTurnos'] == 6:
                    data += datetime.timedelta(days=1)                    
                else:                    
                    return data
            else:
                return data