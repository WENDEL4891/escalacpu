from entities import feriado
from db import connection
import myexceptions
import copy
import sys
import services
from datetime import datetime
from services import functions

class FeriadoDAO:
    def feriado_add(self, data, tipo):
        try:
            feriado_instance = feriado.Feriado(data, tipo)
        except:
            print('Erro ao tentar instanciar um Feriado, no método FeriadoDAO.feriado_add(): ')
            erros = sys.exc_info()
            for i in range(len(erros) - 1):
                print(erros[i])
            raise        

        try:            
            connection_conn = connection.Connection()
            conn = connection_conn.get_connection()
            cursor = conn.cursor()
            
            add_query = "INSERT INTO feriados VALUES (?, ?)"
            params = (feriado_instance.data, feriado_instance.tipo)
            
            cursor.execute(add_query, params)
            conn.commit()
            if cursor.rowcount == 1:
                print('Novo feriado cadastrado com sucesso: ')
                print(feriado_instance)
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
    
    def get_feriado(self, data):
        data_em_datetime = services.functions.date_str_to_datetime(data)
        try:
            connection_conn = connection.Connection()
            conn = connection_conn.get_connection()
            cursor = conn.cursor()

            selectCpuQuery = "SELECT * FROM feriados WHERE data = '" + datetime.strftime(data_em_datetime, '%Y-%m-%d') + "'"

            cursor.execute(selectCpuQuery)
            result = cursor.fetchall()
            if len(result):
                feriado_instance = feriado.Feriado(result[0][0], str(result[0][1]))
                return feriado_instance
            else:
                return None
        except:
            print('Erro ao tentar obter um registro na tabela feriados, no banco de dados: ')
            erros = sys.exc_info()
            for i in range(len(erros) - 1):
                print(erros[i])
            raise
        finally:            
            if 'conn' in locals():
                conn.close()        

    def get_feriados(self, data_inicio='', data_fim=''):        
        if not isinstance(data_inicio, str) and isinstance(data_fim, str):
            raise ValueError('Os parâmetros são opcionais. Mas se informados, devem ser strings.')
        
        if len(data_inicio) != len(data_fim):
            raise ValueError('Informe uma data de início e uma de fim do período. Ou não informe nenhuma data.')
        
        if not data_inicio == '':            
            data_inicio_datetime = functions.date_str_to_datetime(data_inicio)
            data_fim_datetime = functions.date_str_to_datetime(data_fim)
            if data_inicio_datetime > data_fim_datetime:
                raise ValueError('A data fim deve ser superior a data de início.')                   
            condicoes_select = "WHERE data BETWEEN '{:%Y-%m-%d}' AND '{:%Y-%m-%d}'".format(data_inicio_datetime, data_fim_datetime)
        else:
            condicoes_select = ''

        select_query = "SELECT * FROM feriados {}".format(condicoes_select)
        
        try:
            connection_instance = connection.Connection()
            conn = connection_instance.get_connection()
            cursor = conn.cursor()            

            cursor.execute(select_query)
            results = cursor.fetchall()            
            if len(results):                
                feriados = list()
                for result in results:                                        
                    feriado_instance = feriado.Feriado(
                        result[0],
                        str(result[1])
                    )
                    feriados.append(feriado_instance)
                return feriados
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