import datetime
from db import connection
from entities import servico
import config
import sys


class ServicoDAO:
    def __init__(self):
        self.primeiraDataDeServico = datetime.datetime.strptime(config.primeira_data, '%d/%m/%Y')

    def servico_add(self, nome_de_guerra, data, turno, nome_estagio=None):        
        serv_inst = servico.Servico(nome_de_guerra, data, turno, nome_estagio)

        try:
            conn_inst = connection.Connection()
            conn = conn_inst.get_connection()
            cursor = conn.cursor()

            insertServico = 'INSERT INTO servicos VALUES (?, ?, ?, ?)'
            params = (serv_inst.nome_de_guerra, serv_inst.data, serv_inst.turno, serv_inst.nome_estagio)
            cursor.execute(insertServico, params)
            conn.commit()
            if cursor.rowcount == 1:
                print('Serviço inserido no banco de dados com sucesso: ')
                print(serv_inst)
                print('\'' * 40)
            else:
                print('O serviço não foi inserido no banco de dados. Causa não identificada.')
        except:
            print('Erro ao tentar inserir o serviço no Bando de Dados')
            print('Tipo do erro: ', sys.exc_info()[0], sep=' > ')
            print('Descrição do erro: ', sys.exc_info()[1], sep=' > ')
            print(serv_inst)
            print('x' * 40)            
            raise
        finally:
            if 'conn' in locals():
                conn.close()
    
    def get_servicos(self):
        try:
            conn_inst = connection.Connection()
            conn = conn_inst.get_connection()
            cursor = conn.cursor()

            getServicosQuery = 'SELECT * FROM servicos'

            cursor.execute(getServicosQuery)
            results = cursor.fetchall()
            servicos_list = list()
            if len(results):                
                for result in results:
                    serv_inst = servico.Servico(
                        result[0],
                        result[1],
                        result[2],
                        result[3],
                    )
                    servicos_list.append(serv_inst)
            return servicos_list            
        except:
            print('Erro ao tentar buscar serviços no Banco de dados.')
            print('Tipo do erro: ', sys.exc_info()[0], sep=' > ')
            print('Descrição do erro: ', sys.exc_info()[1], sep=' > ')            
            print('x' * 40)            
            raise
        finally:
            if 'conn' in locals():
                conn.close()
    
    def get_qtd_de_servicos_por_dia(self):
        conn_inst = connection.Connection()
        conn = conn_inst.get_connection()
        cursor = conn.cursor()

        getContagem = "SELECT data, SUM(turno), COUNT(data) FROM servicos GROUP BY data;"

        cursor.execute(getContagem)
        qtdServicosPorDiaList = cursor.fetchall()
        conn.close()
        qtdServicosPorDiaDict = dict()        
        for el in qtdServicosPorDiaList:
            qtdServicosPorDiaDict[datetime.datetime.strptime(el[0], '%Y-%m-%d')] = {'somaTurnos':el[1], 'contDatas': el[2]}
        return qtdServicosPorDiaDict
    
    def get_servicos_from_data(self, data):
        data = datetime.datetime.strptime(data, '%d/%m/%Y')
        dataFormat = datetime.datetime.strftime(data, '%Y-%m-%d')
        print(dataFormat)
        conn_inst = connection.Connection()
        conn = conn_inst.get_connection()
        cursor = conn.cursor()

        getSericosToDataQuery = "SELECT nome, data, turno FROM servicos WHERE data <= DATE("+ "'" + dataFormat + "'" +")"
        cursor.execute(getSericosToDataQuery)
        print(getSericosToDataQuery)
        servicosInList = cursor.fetchall()
        return servicosInList
        
    def get_data_com_qtde_de_servicos_incompleta(self):        
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