import datetime
from db import connection
from entities import servico
import config
import sys
from services import functions
import myexceptions


class ServicoDAO:
    def __init__(self):
        self.primeira_data_de_servico = functions.date_str_to_datetime(config.primeira_data)

    def servico_add(self, data=None, turno=None, _cpu=None, nome_estagio=None, _servico=None):        
        if _servico == None:
            serv_inst = servico.Servico(data, turno, _cpu, nome_estagio)
        else:
            serv_inst = _servico
        if serv_inst.cpu.nome_de_guerra == 'DEFAULT':
            raise myexceptions.OperationalException('O serviço com nome de guerra DEFAULT não pode ser inserido no banco de dados.')

        try:
            conn_inst = connection.Connection()
            conn = conn_inst.get_connection()
            cursor = conn.cursor()

            insertServico = 'INSERT INTO servicos VALUES (?, ?, ?, ?)'
            params = (serv_inst.data, serv_inst.turno, serv_inst.cpu.nome_de_guerra, serv_inst.nome_estagio)
            cursor.execute(insertServico, params)
            conn.commit()
            if cursor.rowcount == 1:
                print('Serviço inserido no banco de dados com sucesso: ')
                print(serv_inst)
                print('\'' * 40)
                return 0
            else:
                print('O serviço não foi inserido no banco de dados. Causa não identificada.')
                return 1
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
        if isinstance(data, datetime.date):
            data_datetime = data
        else:
            data_datetime = functions.date_str_to_datetime(data)
        data_format = datetime.datetime.strftime(data_datetime, '%Y-%m-%d')
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

            data_format = datetime.datetime.strftime(servico_para_ser_removido.data, '%Y-%m-%d')

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

    def get_servicos(self, data_inicio=None, data_fim=None):
        if isinstance(data_inicio, datetime.date) and isinstance(data_fim, datetime.date):
            data_inicio_str_format = datetime.datetime.strftime(data_inicio, '%Y-%m-%d')
            data_fim_str_format = datetime.datetime.strftime(data_fim, '%Y-%m-%d')
            complemento_query = "WHERE data BETWEEN '{}' AND '{}'".format(data_inicio_str_format, data_fim_str_format)

        elif isinstance(data_inicio, str) and isinstance(data_fim, str):
            data_inicio_datetime = functions.date_str_to_datetime(data_inicio_str)
            data_fim_datetime = functions.date_str_to_datetime(data_fim_str)
            data_inicio_str_format = datetime.datetime.strftime(data_inicio_datetime, '%Y-%m-%d')
            data_fim_str_format = datetime.datetime.strftime(data_fim_datetime, '%Y-%m-%d')
            complemento_query = "WHERE data BETWEEN '{}' AND '{}'".format(data_inicio_str_format, data_fim_str_format)

        elif data_inicio == None and data_fim == None:
            complemento_query = ''

        elif data_inicio == None or data_fim == None:
            raise ValueError('Os parâmetros data_inicio e data_fim devem ambos serem deixados em branco ou receberem argumentos do mesmo tipo, str ou datetime.date.')
        
        else:
            raise ValueError('Os parâmetros data_inicio e data_fim devem ambos serem deixados em branco ou receberem argumentos do mesmo tipo, str ou datetime.date.')
    
        try:
            conn_inst = connection.Connection()
            conn = conn_inst.get_connection()
            cursor = conn.cursor()

            get_servicos_query = 'SELECT * FROM servicos {} ORDER BY data'.format(complemento_query, )

            cursor.execute(get_servicos_query)
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
    
    def servico_update(self, data_atual, turno_atual, data=None, turno=None, _cpu=None, nome_estagio=None):
        servico_para_ser_atualizado = self.get_servico(data_atual, turno_atual)
        if servico_para_ser_atualizado == None:
            raise ValueError('Não há servico para ser atualizado, com a data e o turno informados (' + data_atual + ', ' + str(turno_atual) + 'º turno).')

        servico_atualizador = servico.Servico(
            data if data != None else datetime.datetime.strftime(servico_para_ser_atualizado.data, '%Y-%m-%d'),
            turno if turno != None else servico_para_ser_atualizado.turno,
            _cpu if _cpu != None else servico_para_ser_atualizado.cpu,
            nome_estagio if nome_estagio != None else servico_para_ser_atualizado.nome_estagio            
        )
        
        if servico_atualizador.cpu.nome_de_guerra == 'DEFAULT':
            raise myexceptions.OperationalException('O serviço com nome de guerra DEFAULT não pode ser inserido no banco de dados.')

        if servico_para_ser_atualizado == servico_atualizador:
            raise myexceptions.LogicException('Não foi informado nenhum dado novo para atualizar o serviço.')
                
        complemento_query = ''
        for key, value in servico_atualizador.__repr__().items():
            if value == None:
                continue
            if key == 'data':
                complemento_query += key + " = '" + datetime.datetime.strftime(servico_atualizador.data, '%Y-%m-%d') + "', "
            if key == 'cpu':
                complemento_query += 'nome_de_guerra' + " = '" + value.nome_de_guerra + "', "
            else:
                complemento_query += key + " = '" + str(value) + "', "
        complemento_query = complemento_query[:-2]
        
        update_query = 'UPDATE servicos SET ' + complemento_query + " WHERE " +\
            "data = '" + datetime.datetime.strftime(servico_para_ser_atualizado.data, '%Y-%m-%d') + "' AND " +\
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
                serv_antes_dict['cpu'] = '{} {}'.format(serv_antes_dict['cpu'].pg, serv_antes_dict['cpu'].nome_de_guerra)
                serv_depois_dict['cpu'] = '{} {}'.format(serv_depois_dict['cpu'].pg, serv_depois_dict['cpu'].nome_de_guerra)

                serv_antes_dict['data'] = datetime.datetime.strftime(serv_antes_dict['data'], '%d/%m/%Y')
                serv_depois_dict['data'] = datetime.datetime.strftime(serv_depois_dict['data'], '%d/%m/%Y')
                
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
        try:                
            conn_inst = connection.Connection()
            conn = conn_inst.get_connection()
            cursor = conn.cursor()

            get_contagem_query = "SELECT data, SUM(turno), COUNT(data) FROM servicos GROUP BY data;"

            cursor.execute(get_contagem_query)
            qtd_de_servicos_por_dia_list = cursor.fetchall()            
        except:
            erros = sys.exc_info()
            for i in range(len(erros) - 1):
                print(erros[i])
                raise
        finally:
            if 'conn' in locals():
                conn.close()

        qtd_de_servicos_por_dia_dict = dict()
        for el in qtd_de_servicos_por_dia_list:            
            data = functions.date_str_to_datetime(el[0])
            qtd_de_servicos_por_dia_dict[data] = {'soma_turnos':el[1], 'cont_datas': el[2]}        
        return qtd_de_servicos_por_dia_dict
    
    def get_servicos_from_data(self, data_in_datetime):
        data_in_datetime = datetime.datetime.strptime(data_in_datetime, '%d/%m/%Y')
        dataFormat = datetime.datetime.strftime(data_in_datetime, '%Y-%m-%d')
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
        data = self.primeira_data_de_servico
        qtd_de_servicos_por_dia_dict = self.get_qtd_de_servicos_por_dia()
        datasList = list(qtd_de_servicos_por_dia_dict)
                
        while(True):                        
            if data in datasList:
                if qtd_de_servicos_por_dia_dict[data]['soma_turnos'] == 6:
                    data += datetime.timedelta(days=1)                    
                else:                    
                    return data
            else:
                return data
    
    def get_dias_e_turnos_para_escalar(self):        
        primeira_data_incompleta = self.get_data_com_qtde_de_servicos_incompleta()        
        dia_da_semana_num = primeira_data_incompleta.weekday() # 0 para segunda até 6 para domingo        
        seg_no_periodo = primeira_data_incompleta - datetime.timedelta(days=dia_da_semana_num)
        dom_no_periodo = seg_no_periodo + datetime.timedelta(days=6)
        #todas_as_datas_do_periodo_in_list = list()#

        def todas_as_datas_da_semana_generator():
            for num in range(7):
                yield seg_no_periodo + datetime.timedelta(days=num)
        todas_as_datas_da_semana_list = list(todas_as_datas_da_semana_generator())
        
        #for num in range(7):            
        #    todas_as_datas_do_periodo_in_list.append(seg_no_periodo + datetime.timedelta(days=num))
        
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
        
        for data in todas_as_datas_da_semana_list:
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