from entities import feriado, ordenacaopormilitar
from db import connection
import myexceptions
import copy
import sys
import services
from datetime import datetime

class OrdenacaoPorMilitarDAO:
    def ordenacao_por_militar_add(self, nome_de_guerra, seg_12, seg_3, ter_qui_sex_12, qua_12, ter_3, qua_3, qui_3, sex_3, fds_12, sab_3, dom_3):
        try:
            ordenacao_por_militar = ordenacaopormilitar.OrdenacaoPorMilitar(
                nome_de_guerra,
                seg_12,
                seg_3,
                ter_qui_sex_12,
                qua_12,
                ter_3,
                qua_3,
                qui_3,
                sex_3,
                fds_12,
                sab_3,
                dom_3
            )
        except:
            print('Erro ao tentar instanciar um objeto OrdenacaoPorMilitar, no método OrdenacaoPorMilitarDAO.ordenacao_por_militar_add(): ')
            erros = sys.exc_info()
            for i in range(len(erros) - 1):
                print(erros[i])
            raise        

        try:            
            connection_conn = connection.Connection()
            conn = connection_conn.get_connection()
            cursor = conn.cursor()
            
            add_query = "INSERT INTO ordenacao_por_militar VALUES ({})".format('?,' * 11 + '?')
            
            params = (
                ordenacao_por_militar.nome_de_guerra,
                ordenacao_por_militar.seg_12,
                ordenacao_por_militar.seg_3,
                ordenacao_por_militar.ter_qui_sex_12,
                ordenacao_por_militar.qua_12,
                ordenacao_por_militar.ter_3,
                ordenacao_por_militar.qua_3,
                ordenacao_por_militar.qui_3,
                ordenacao_por_militar.sex_3,
                ordenacao_por_militar.fds_12,
                ordenacao_por_militar.sab_3,
                ordenacao_por_militar.dom_3
            )
            
            cursor.execute(add_query, params)
            conn.commit()
            if cursor.rowcount == 1:
                print('Novo registro cadastrado com sucesso na tabela ordenacao_por_militar: ')
                print(ordenacao_por_militar)
                print('\'' * 40 )
            else:
                raise myexceptions.BdOperationError('O cadastro não foi realizado. Causa não identificada.')
        except:
            print('Erro ao tentar incluir um feriado no banco de dados : ')
            erros = sys.exc_info()
            for i in range(len(erros) - 1):
                print(erros[i])
            raise        
        finally:
            if 'conn' in locals():
                conn.close()
    
    def get_ordenacao_por_modalidade(self, modalidade, impedidos=[]):
        if not isinstance(modalidade, str):
            raise TypeError('O parâmetro modalidade deve receber uma string como argumneto.')
        modalidades_validas = ('seg_12', 'seg_3', 'ter_qui_sex_12', 'qua_12', 'ter_3', 'qua_3', 'qui_3', 'sex_3', 'fds_12', 'sab_3', 'dom_3')
        if modalidade not in modalidades_validas:
            raise ValueError('O parâmetro modalidades deve receber uma dentre as modalidades seguintes: [{}].'.format(', '.join(modalidades_validas)))

        try:
            connection_conn = connection.Connection()
            conn = connection_conn.get_connection()
            cursor = conn.cursor()

            query_get_next = "SELECT nome_de_guerra, {} FROM ordenacao_por_militar".format(modalidade.lower())
            cursor.execute(query_get_next)
            results = cursor.fetchall()
            if results:
                ordenacao_por_modalidade_dict = dict()
                for result in results:
                    ordenacao_por_modalidade_dict[result[0]] = result[1]
                return ordenacao_por_modalidade_dict
            else:
                print('Não há ordenacao cadastrada, na modalidade {}.'.format(modalidade.lower()))
        except:
            print('Erro ao tentar obter a ordenação na modalidade {}.'.format(modalidade.lower()))
            erros = sys.exc_info()
            for i in range(len(erros) - 1):
                print(erros[1])
        finally:
            if 'conn' in locals():
                conn.close()


    def feriado_remove(self, data):
        data_em_datetime = services.functions.date_str_to_datetime(data)
        feriado_para_ser_removido = self.get_feriado(data)
        if feriado_para_ser_removido == None:
            raise ValueError('Não há feriado na data informada: ({}), para remoção.'.format(data))
        try:
            connection_conn = connection.Connection()
            conn = connection_conn.get_connection()
            cursor = conn.cursor()

            rm_query = "DELETE FROM feriados WHERE data = '{}'".format(datetime.strftime(data_em_datetime, '%Y-%m-%d'))

            cursor.execute(rm_query)                       
            conn.commit()
            if cursor.rowcount:
                print('Feriado removido com sucesso: ')
                print(feriado_para_ser_removido)
                print('\'' * 40)
            else:
                print('Não foi realizada a remoção do feriado descrito adiante. Causa não identificada.')
                print(feriado_para_ser_removido)

        except sqlite3.OperationalError as err:
            print('Erro ao tentar excluir do banco de dados o cpu : ')
            print(feriado_para_ser_removido)
            print('Tipo do erro: ', sys.exc_info()[0], sep=' > ')
            print('Descrição do erro: ', sys.exc_info()[1], sep=' > ')
            raise
        finally:
            if 'conn' in locals():
                conn.close()
    
    def feriado_update(self, data_atual, data=None, tipo=None):
        data_atual_datetime= services.functions.date_str_to_datetime(data_atual)
        feriado_para_ser_atualizado = self.get_feriado(data_atual)
        if feriado_para_ser_atualizado == None:
            raise ValueError('Não há feriado cadastrado na data informada ({}), para atualização.'.format(data_atual))

        if data == tipo == None:
            raise NameError('Deve ser informado ao menos 1 campo para ser atualizado, dentre data e tipo.')
                
        feriado_atualizador = feriado.Feriado(
            data if data != None else '{:%d/%m/%Y}'.format(feriado_para_ser_atualizado.data),
            tipo if tipo != None else feriado_para_ser_atualizado.tipo

        )
                       
        if feriado_para_ser_atualizado == feriado_atualizador:
            raise myexceptions.LogicException('Não foi informado nenhum dado novo para atualização.')
                        
        
        complemento_query_tupla = (            
            "data = '{:%Y-%m-%d}'".format(feriado_atualizador.data),
            "tipo = '{}'".format(feriado_atualizador.tipo)                    
        )

        complemento_query_string = ', '.join(complemento_query_tupla)

        update_feriado_query = "UPDATE feriados SET {} WHERE data = '{:%Y-%m-%d}'".format(complemento_query_string, data_atual_datetime)        
                
        try:            
            connection_conn = connection.Connection()
            conn = connection_conn.get_connection()
            cursor = conn.cursor()

            cursor.execute(update_feriado_query)
            conn.commit()
            antes_dict = feriado_para_ser_atualizado.__repr__()
            depois_dict = feriado_atualizador.__repr__()
            if cursor.rowcount == 1:
                print('Feriado atualizado com sucesso:')
                for key, value in antes_dict.items():
                    if antes_dict[key] != depois_dict[key]:
                        print('{:7}: {:-<25}'.format(key, value), end='')
                        print(' >> ATUALIZADO PARA >> {} <<'.format(str(depois_dict[key])))
                    else:
                        print('{:7}: {}'.format(key, value))
                print('\'' * 40)
            else:
                print('Problema na atualização. Causa ignorada')
        except:
            print("Erro ao tentar atualizar o registro no banco de dados: ")
            erros = sys.exc_info()
            for i in range(len(erros) - 1):
                print(erros[i])
            raise            
        finally:
            if 'conn' in locals():
                conn.close()
    
    def get_ordenacao_por_militar(self, nome_de_guerra):
        if not isinstance(nome_de_guerra, str):
            raise TypeError('O parâmetro nome_de_guerra deve receber um argumento do tipo string.')
        try:
            connection_conn = connection.Connection()
            conn = connection_conn.get_connection()
            cursor = conn.cursor()

            selectCpuQuery = "SELECT * FROM ordenacao_por_militar WHERE nome_de_guerra = '{}'".format(nome_de_guerra.upper())

            cursor.execute(selectCpuQuery)
            result = cursor.fetchall()
            if len(result):
                ordenacao_por_militar = ordenacaopormilitar.OrdenacaoPorMilitar(
                    result[0][0],
                    result[0][1],
                    result[0][2],
                    result[0][3],
                    result[0][4],
                    result[0][5],
                    result[0][6],
                    result[0][7],
                    result[0][8],
                    result[0][9],
                    result[0][10],
                    result[0][11]                    
                )
                return ordenacao_por_militar
            else:
                return None
        except:
            print('Erro ao tentar obter um registro na tabela ordenacao_por_militar, no banco de dados: ')
            erros = sys.exc_info()
            for i in range(len(erros) - 1):
                print(erros[i])
            raise
        finally:            
            if 'conn' in locals():
                conn.close()        

    def get_ordenacao_por_militar_all(self):
        
        select_query = "SELECT * FROM ordenacao_por_militar"
        
        try:
            connection_instance = connection.Connection()
            conn = connection_instance.get_connection()
            cursor = conn.cursor()            

            cursor.execute(select_query)
            results = cursor.fetchall()            
            if len(results):                
                ordenacoes = list()
                for result in results:
                    ordenacao_por_militar = ordenacaopormilitar.OrdenacaoPorMilitar(
                        result[0],result[1],result[2],result[3],result[4],result[5],result[6],result[7],result[8],result[9],result[10],result[11]
                    )
                    ordenacoes.append(ordenacao_por_militar)
                return ordenacoes
            else:
                return list()
        except:
            print('Erro ao tentar obter registros na tabela feriados, no banco de dados: ')
            erros = sys.exc_info()
            for i in range(len(erros) - 1):
                print(erros[i])
            raise
        finally:
            if 'conn' in locals():
                conn.close()