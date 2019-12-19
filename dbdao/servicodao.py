from datetime import datetime
from db import connection
from entities import servico
import config
import sys
from services import functions
import myexceptions


class ServicoDAO:
    def __init__(self):
        self.primeiraDataDeServico = datetime.strptime(config.primeira_data, '%d/%m/%Y')

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
            print('Erro ao tentar inserir o serviço no banco de dados')
            print('Tipo do erro: ', sys.exc_info()[0], sep=' > ')
            print('Descrição do erro: ', sys.exc_info()[1], sep=' > ')
            print(serv_inst)
            print('x' * 40)            
            raise
        finally:
            if 'conn' in locals():
                conn.close()
    
    def get_servico(self, data, turno):
        data_datetime = functions.date_str_to_datetime(data)
        data_format = datetime.strftime(data_datetime, '%Y-%m-%d')
        if turno not in (1, 2, 3, '1', '2', '3'):
            raise ValueError('O parâmetro turno deve receber o valor 1, 2 ou 3.')
        turno_format = str(turno)
        try:
            connection_conn = connection.Connection()
            conn = connection_conn.get_connection()
            cursor = conn.cursor()

            select_query = "SELECT * FROM servicos WHERE data = '" + data_format + "' and turno = '" + turno_format + "'"

            cursor.execute(select_query)
            result = cursor.fetchall()            
            if len(result):
                servico_instance = servico.Servico(result[0][0], result[0][1], result[0][2], result[0][3])
                return servico_instance
            else:
                return None
        except:
            print('Erro ao tentar obter servico no banco de dados: ')
            print('Tipo do erro: ', sys.exc_info()[0])
            print('Descrição: ', sys.exc_info()[1])
            raise
        finally:            
            if 'conn' in locals():
                conn.close()   

    def servico_remove(self, data, turno):
        servico_para_ser_removido = self.get_servico(data, turno)
        if servico_para_ser_removido == None:
            raise ValueError('Não há serviço com a data e turno informados, (' + data + ', ' + str(turno) +  'º turno), para remoção.')
        try:
            connection_conn = connection.Connection()
            conn = connection_conn.get_connection()
            cursor = conn.cursor()

            data_format = datetime.strftime(servico_para_ser_removido.data, '%Y-%m-%d')

            rm_query = "DELETE FROM servicos WHERE data = '" + data_format + "' AND turno = " + str(servico_para_ser_removido.turno)

            cursor.execute(rm_query)                       
            conn.commit()
            if cursor.rowcount:
                print('Servico removido com sucesso: ')
                print(servico_para_ser_removido)
                print('\'' * 40)
            else:
                print('Não foi realizada a remoção do servico (' + servico_para_ser_removido.data + ', ' + str(servico_para_ser_removido.turno) +  'º turno). Causa não identificada.')

        except:
            print('Erro ao tentar excluir do banco de dados o serviço : ')
            print(servico_para_ser_removido)
            print('Tipo do erro', sys.exc_info()[0], sep=':  ')
            print('Descrição do erro', sys.exc_info()[1], sep=': ')
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
    
    def servico_update(self, data_atual, turno_atual, nome_de_guerra=None, data=None, turno=None, nome_estagio=None):
        servico_para_ser_atualizado = self.get_servico(data_atual, turno_atual)
        if servico_para_ser_atualizado == None:
            raise ValueError('Não há servico para ser atualizado, com a data e o turno informados (' + data_atual + ', ' + str(turno_atual) + 'º turno).')

        servico_atualizador = servico.Servico(
            nome_de_guerra if nome_de_guerra != None else servico_para_ser_atualizado.nome_de_guerra,
            data if data != None else datetime.strftime(servico_para_ser_atualizado.data, '%Y-%m-%d'),
            turno if turno != None else servico_para_ser_atualizado.turno,
            nome_estagio if nome_estagio != None else servico_para_ser_atualizado.nome_estagio            
        )
        if servico_para_ser_atualizado == servico_atualizador:
            raise myexceptions.LogicException('Não foi informado nenhum dado novo para atualizar o serviço.')
                
        complemento_query = ''
        for key, value in servico_atualizador.__repr__().items():
            if value == None:
                continue
            if key == 'data':
                complemento_query += key + " = '" + datetime.strftime(servico_atualizador.data, '%Y-%m-%d') + "', "
            else:
                complemento_query += key + " = '" + str(value) + "', "
        complemento_query = complemento_query[:-2]
        
        update_query = 'UPDATE servicos SET ' + complemento_query + " WHERE " +\
            "data = '" + datetime.strftime(servico_para_ser_atualizado.data, '%Y-%m-%d') + "' AND " +\
            "turno = " + str(servico_para_ser_atualizado.turno)

        try:
            connection_conn = connection.Connection()
            conn = connection_conn.get_connection()
            cursor = conn.cursor()

            cursor.execute(update_query)
            conn.commit()
            if cursor.rowcount == 1:
                serv_antes_dict = servico_para_ser_atualizado.__repr__()
                serv_depois_dict = servico_atualizador.__repr__()

                serv_antes_dict['data'] = datetime.strftime(serv_antes_dict['data'], '%d/%m/%Y')
                serv_depois_dict['data'] = datetime.strftime(serv_depois_dict['data'], '%d/%m/%Y')
                
                print('Serviço atualizado com sucesso: ')
                for attr, value in serv_antes_dict.items():
                    if serv_antes_dict[attr] == serv_depois_dict[attr]:
                        print(attr, value, sep=': ')
                    else:
                        print(attr, value, sep=': ', end='')
                        print(' > ATUALIZADO PARA # ' + str(serv_depois_dict[attr]) + ' #')
                print('Novo serviço', servico_atualizador, sep=' >> ')
                print('\'' * 40)            
        except:
            print('Erro ao tentar obter atualizar o serviço no banco de dados: ')
            print(servico_atualizador)
            print('Tipo do erro: ', sys.exc_info()[0])
            print('Descrição: ', sys.exc_info()[1])
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
            qtdServicosPorDiaDict[datetime.strptime(el[0], '%Y-%m-%d')] = {'somaTurnos':el[1], 'contDatas': el[2]}
        return qtdServicosPorDiaDict
    
    def get_servicos_from_data(self, data):
        data = datetime.strptime(data, '%d/%m/%Y')
        dataFormat = datetime.strftime(data, '%Y-%m-%d')
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