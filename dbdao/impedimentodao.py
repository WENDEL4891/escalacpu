from entities import impedimento
from db import connection
from dbdao import cpudao
import sqlite3
from datetime import datetime
from services import functions
import myexceptions
import copy


class ImpedimentoDAO:
    def impedimento_add(self, nome_de_guerra, tipo, data_inicio, data_fim='', observacao=''):        
        impedimento_instance = impedimento.Impedimento(nome_de_guerra, tipo, data_inicio, data_fim, observacao)
                
        try:
            connection_instance = connection.Connection()
            conn = connection_instance.get_connection()
            cursor = conn.cursor()
            
            dta_in_format = datetime.strftime(impedimento_instance.data_inicio, '%Y-%m-%d')
            dta_fim_format = datetime.strftime(impedimento_instance.data_fim, '%Y-%m-%d')

            primCond = "nome_de_guerra = '" + impedimento_instance.nome_de_guerra + "'"
            segCond = "'" + dta_in_format + "' BETWEEN DATE(data_inicio) AND DATE(data_fim)"            
            terCond = "DATE(data_inicio) BETWEEN '" + dta_in_format + "' AND '" + dta_fim_format + "'"
            quarCond = "DATE(data_fim) BETWEEN '" + dta_in_format + "' AND '" + dta_fim_format + "'"
            condicoes = "(" + primCond + ") AND ( (" + segCond + ") OR (" + terCond + ") OR (" + quarCond + ") )"

            select_query = "SELECT nome_de_guerra, tipo, data_inicio, data_fim FROM impedimentos WHERE " + condicoes
            
            cursor.execute(select_query)
            
            impedimentosConflitantes = cursor.fetchall()
            
            if len(impedimentosConflitantes):
                complemento = ''
                for impedimentoConflitante in impedimentosConflitantes:                    
                    inicio = functions.invertFormatDateStr(impedimentoConflitante[2])
                    fim = functions.invertFormatDateStr(impedimentoConflitante[3])

                    complemento += '\nNome de guerra: ' + impedimentoConflitante[0] + '\nTipo: ' + impedimentoConflitante[1] + '\nInicio: ' + inicio + '\nFim: ' + fim + '\n' + '-' * 20
                
                msgErro = 'Impedimento conflitante com o(s) seguinte(s): ' + complemento                
                
                raise ValueError(msgErro)

            addQuery = "INSERT INTO impedimentos (nome_de_guerra, tipo, data_inicio, data_fim, observacao) VALUES (?, ?, ?, ?, ?)"
            params = (impedimento_instance.nome_de_guerra, impedimento_instance.tipo, impedimento_instance.data_inicio, impedimento_instance.data_fim, 
            impedimento_instance.observacao)            
            
            cursor.execute(addQuery, params)
            conn.commit()
            print('Impedimento cadastrado com sucesso: ')
            for key, value in impedimento_instance.__repr__().items():
                print(key, value, sep=' > ')
            print('\'' * 40)

        except sqlite3.OperationalError as err:
            print('Erro de Banco de Dados : ')
            print(err)
        finally:
            if 'conn' in locals():
                conn.close()

    def impedimento_remove(self, nome_de_guerra, data_inicio):
        impedimento_para_ser_removido = self.get_impedimento(nome_de_guerra, data_inicio)
        if impedimento_para_ser_removido == None:
            raise ValueError('Não há impedimento com os dados informados (nome de guerra: ' + nome_de_guerra + ', data de início: ' + data_inicio + '), para remoção.')        

        try:
            connection_instance = connection.Connection()
            conn = connection_instance.get_connection()
            cursor = conn.cursor()
           
            nome_de_guerra_format = impedimento_para_ser_removido.nome_de_guerra
            data_inicio_format = datetime.strftime(impedimento_para_ser_removido.data_inicio, '%Y-%m-%d')

            rmQuery = "DELETE FROM impedimentos WHERE nome_de_guerra = '" + nome_de_guerra_format + "' AND DATE(data_inicio) = '" + data_inicio_format + "'"

            cursor.execute(rmQuery)
            conn.commit()

            if cursor.rowcount == 1:
                print('Impedimento excluído com sucesso: ')
                for key, value in impedimento_para_ser_removido.__repr__().items():
                    print(key, value, sep=' > ')

        except sqlite3.OperationalError as err:
            print('Erro de Banco de Dados: ')
            print(err)
        finally:
            if 'conn' in locals():
                conn.close()
    
    def impedimento_update(self, nome_de_guerra_atual, data_inicio_atual, **dados_para_atualizar_params):
        impedimento_para_atualizar = self.get_impedimento(nome_de_guerra_atual, data_inicio_atual)
        if impedimento_para_atualizar == None:
            raise ValueError('Não há impedimento com o nome de guerra e data de início informados.')
                        
        if not isinstance(nome_de_guerra_atual, str) and isinstance(data_inicio_atual, str):
            raise TypeError('O nome de guerra e a data de início devem ser strings.')
        else:
            nome_de_guerra_atual = nome_de_guerra_atual.upper()

        functions.date_str_to_datetime(data_inicio_atual)
        
        parametros_validos = ['nome_de_guerra', 'tipo', 'data_inicio', 'data_fim', 'observacao']
        if len(dados_para_atualizar_params) == 0:
            raise NameError('Deve ser informado ao menos 1 campo para ser atualizado dentre os seguintes: \n\t'\
                + ', '.join(parametros_validos) + '.')
        
        for key, value in dados_para_atualizar_params.items():
            if isinstance(value, str):
                dados_para_atualizar_params[key] = value.upper()            
            else:
                raise TypeError('Todos os parâmetros devem ser do tipo string.')
        
        parametros_informados = list(dados_para_atualizar_params)                
        
        
        if 'data_inicio' in parametros_informados and 'data_fim' in parametros_informados:
            try:
                di = datetime.strptime(dados_para_atualizar_params['data_inicio'], '%d/%m/%Y')
                df = datetime.strptime(dados_para_atualizar_params['data_fim'], '%d/%m/%Y')
            except ValueError:
                raise ValueError('As datas devem ser informadas no formato dd/mm/AAAA.')
            if di > df:
                raise ValueError('A data de início não pode ser posterior a data fim.')
            dados_para_atualizar_params['data_inicio'] = datetime.strftime(di, '%Y-%m-%d')
            dados_para_atualizar_params['data_fim'] = datetime.strftime(df, '%Y-%m-%d')
        if 'data_inicio' in parametros_informados and 'data_fim' not in parametros_informados:        
            try:
                di = datetime.strptime(dados_para_atualizar_params['data_inicio'], '%d/%m/%Y')                
            except ValueError:
                raise ValueError('As datas devem ser informadas no formato dd/mm/AAAA.')
            if di.date() > impedimento_para_atualizar.data_fim:
                raise ValueError('A data de início não pode ser posterior a data fim.')
            dados_para_atualizar_params['data_inicio'] = datetime.strftime(di, '%Y-%m-%d')
        if 'data_fim' in parametros_informados and 'data_inicio' not in parametros_informados:
            try:                
                df = datetime.strptime(dados_para_atualizar_params['data_fim'], '%d/%m/%Y')
            except ValueError:
                raise ValueError('As datas devem ser informadas no formato dd/mm/AAAA.')            
            if df.date() < impedimento_para_atualizar.data_inicio:
                raise ValueError('A data fim deve ser igual ou posterior a data de início.')
            dados_para_atualizar_params['data_fim'] = datetime.strftime(df, '%Y-%m-%d')
            
        
        parametros_invalidos = list()
        for key in dados_para_atualizar_params:
            if key not in parametros_validos:
                parametros_invalidos.append(key)
        
        if len(parametros_invalidos):
            raise ValueError('Somente devem ser passados parâmetros dentre os seguintes: ' + ', '.join(parametros_validos) + '.')        
        
        dadosParaAtualizarParaQuery = ''        
        
        for key, value in dados_para_atualizar_params.items():                
            dadosParaAtualizarParaQuery += key + " = '" + value + "', "
        dadosParaAtualizarParaQuery = dadosParaAtualizarParaQuery[0:-2]        
        
        data_inicio_atualFormat = functions.invertFormatDateStr(data_inicio_atual)

        updateQuery = "UPDATE impedimentos SET " + dadosParaAtualizarParaQuery + " WHERE nome_de_guerra = '" + nome_de_guerra_atual +"' AND DATE(data_inicio) = '" + data_inicio_atualFormat + "'"        
                
        try:            
            connection_instance = connection.Connection()
            conn = connection_instance.get_connection()
            cursor = conn.cursor()
            cursor.execute(updateQuery)
            conn.commit()
            
            if cursor.rowcount == 1:                                
                print('Impedimento atualizado com sucesso:')
                antes = impedimento_para_atualizar.__repr__()                
                for key, value in antes.items():
                    if key in parametros_informados:
                        print(key, value, sep=' > ', end='')
                        print(' | alterado para', dados_para_atualizar_params[key], sep=': ')
                    else:
                        print(key, value, sep=' > ')
                print('\'' * 40)
            else:
                print('A atualização não foi efetivada. Motivo ignorado.')
        except sqlite3.OperationalError as err:
            print("Erro de Banco de Dados: ")
            print(err)
        finally:
            if 'conn' in locals():
                conn.close()
               
    
    def get_impedimento(self, nome_de_guerra, data_inicio):        
        if not isinstance(nome_de_guerra, str) and isinstance(data_inicio, str):
            raise TypeError('O nome de guerra e a data de início devem ser strings.')        
        nome_de_guerra_format = nome_de_guerra.upper()

        data_inicio_datetime = functions.date_str_to_datetime(data_inicio)
        data_inicio_format = datetime.strftime(data_inicio_datetime, '%Y-%m-%d')               
        
        select_query = "SELECT nome_de_guerra, tipo, data_inicio, data_fim, observacao FROM \
            impedimentos WHERE nome_de_guerra  = '" + nome_de_guerra_format + "' AND  \
            data_inicio = '" + data_inicio_format + "'"        
        
        try:           
            connection_instance = connection.Connection()
            conn = connection_instance.get_connection()            
            cursor = conn.cursor()
            
            cursor.execute(select_query)
            result = cursor.fetchall()                        
            
            if len(result) > 1:
                raise myprogramerrors.IntegrityError('Há mais de um registro com o mesmo nome de guerra e data de início.')
            elif len(result) == 1:
                impedimento_instance = impedimento.Impedimento(result[0][0], result[0][1], result[0][2], result[0][3], result[0][4])
                return impedimento_instance                
            else:
                return None
        except sqlite3.OperationalError as err:            
            print('Erro de Banco de Dados: ')
            print(err)
            raise
        finally:            
            if 'conn' in locals():
                conn.close()

    def get_impedimentos_from_date(self, data_inicio='', data_fim=''):
        if not isinstance(data_inicio, str) and isinstance(data_fim, str):
            raise ValueError('Os parâmetros são opcionais. Mas se informados, devem ser strings.')
        
        if len(data_inicio) != len(data_fim):
            raise ValueError('Informe uma data de início e uma de fim do período. Ou não informe nenhuma data.')
        
        if not data_inicio == '':            
            data_inicio_datetime = functions.date_str_to_datetime(data_inicio)
            data_fim_datetime = functions.date_str_to_datetime(data_fim)
            if data_inicio_datetime > data_fim_datetime:
                raise ValueError('A data fim deve ser superior a data de início.')
                                    
            dta_in_format = datetime.strftime(data_inicio_datetime, '%Y-%m-%d')
            dta_fim_format = datetime.strftime(data_fim_datetime, '%Y-%m-%d')
        
            primCond = "'" + dta_in_format + "' BETWEEN DATE(data_inicio) AND DATE(data_fim)"        
            segCond = "DATE(data_inicio) BETWEEN '" + dta_in_format + "' AND '" + dta_fim_format + "'"
            terCond = "DATE(data_fim) BETWEEN '" + dta_in_format + "' AND '" + dta_fim_format + "'"
            condicoes = " WHERE (" + primCond + ") OR (" + segCond + ") OR (" + terCond + ")"
        else:
            condicoes = ''

        select_query = "SELECT nome_de_guerra, tipo, data_inicio, data_fim, observacao FROM impedimentos" + condicoes                  
        
        try:
            connection_instance = connection.Connection()
            conn = connection_instance.get_connection()
            cursor = conn.cursor()            

            cursor.execute(select_query)
            results = cursor.fetchall()            
            if len(results):
                impedimentos = list()
                for result in results:                    
                    impedimento_instance = impedimento.Impedimento(
                        result[0],
                        result[1],
                        result[2],
                        result[3],
                        result[4]
                    )
                    impedimentos.append(impedimento_instance)
                return impedimentos
            else:
                return list()
        except sqlite3.OperationalError as err:
            print('Erro de Banco de Dados: ')
            print(err)
        finally:
            if 'conn' in locals():
                conn.close()
            