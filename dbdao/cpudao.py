from entities import cpu
from db import connection
import sqlite3
import myprogramerrors

class CpuDAO:
    def cpu_add(self, pg, nome_completo, nome_de_guerra, funcao, curso, ano_base):        
        try:
            cpu_instance = cpu.Cpu(pg, nome_completo, nome_de_guerra, funcao, curso, ano_base)
            
            connection_conn = connection.Connection()
            conn = connection_conn.getConnection()
            cursor = conn.cursor()
            
            addQuery = "INSERT INTO CPUs (pg, nome_completo, nome_de_guerra, funcao, curso, ano_base) VALUES (?, ?, ?, ?, ?, ?)"
            
            cursor.execute(addQuery, (cpu_instance.pg, cpu_instance.nome_completo, cpu_instance.nome_de_guerra, cpu_instance.funcao, cpu_instance.curso, cpu_instance.ano_base))
            conn.commit()
            if cursor.rowcount == 1:
                print('Novo CPU cadastrado com sucesso: ')
                for key, value in cpu_instance.__repr__().items():
                    print(key, value, sep=' > ')
            else:
                raise myprogramerrors.BdOperationError('O cadastro não foi realizado. Causa não identificada.')

        except sqlite3.OperationalError as err:
            print('Erro de Banco de Dados : ')
            print(err)
        except sqlite3.IntegrityError as err:
            print('Já existe um registro com o nome de guerra: ' + cpu_instance.nome_de_guerra)
        finally:
            if 'conn' in locals():
                conn.close()


    def cpu_remove(self, nome_de_guerra):
        cpu_para_ser_removido = self.get_cpu(nome_de_guerra)
        if cpu_para_ser_removido == None:
            raise ValueError('Não há cpu com o nome de guerra informado (' + nome_de_guerra + '), para remoção.')
        try:
            connection_conn = connection.Connection()
            conn = connection_conn.getConnection()
            cursor = conn.cursor()

            rmQuery = "DELETE FROM CPUs WHERE nome_de_guerra = '" + cpu_para_ser_removido.nome_de_guerra + "'"

            cursor.execute(rmQuery)                       
            if cursor.rowcount:
                print('CPU removido com sucesso: ')
                for key, value in cpu_para_ser_removido.__repr__().items():
                    print(key, value, sep= ' > ')
            else:
                print('Não foi realizada a remoção do cpu (' + cpu_para_ser_removido.nome_de_guerra + '). Causa não identificada.')

        except sqlite3.OperationalError as err:
            print('Erro de Banco de Dados: ')
            print(err)        
        finally:
            conn.commit()
            conn.close()
    
    def cpu_update(self, nome_de_guerra_atual, **dados_para_atualizar_params):
        cpu_para_ser_atualizado = self.get_cpu(nome_de_guerra_atual)
        if cpu_para_ser_atualizado == None:
            raise ValueError('Não há CPU com o nome de guerra informado, para ser atualizado.')
        
        parametros_validos = ['pg', 'nome_completo', 'nome_de_guerra', 'funcao', 'curso', 'ano_base']
        if len(dados_para_atualizar_params) == 0:
            raise NameError('Deve ser informado ao menos 1 campo para ser atualizado dentre os seguintes: '\
                + ', '.join(parametros_validos) + '.')
        
        for key, value in dados_para_atualizar_params.items():
            if isinstance(value, str):
                dados_para_atualizar_params[key] = value.upper()
        
        argumentos_invalidos = list()
        for key in dados_para_atualizar_params:
            if key not in parametros_validos:
                argumentos_invalidos.append(key)
        
        if len(argumentos_invalidos):
            raise ValueError('Somente devem ser passados argumentos dentre os seguintes: ' + ', '.join(parametros_validos) + '.')
        
        dados_para_atualizar_para_query = ''
        
        if len(dados_para_atualizar_params) > 1:
            for key, value in dados_para_atualizar_params.items():
                if isinstance(value, str):                    
                    dados_para_atualizar_para_query += key + " = '" + value + "', "
                else:                    
                    dados_para_atualizar_para_query += key + " = " + str(value) + ", "
            dados_para_atualizar_para_query = dados_para_atualizar_para_query[0:-2]
        else:
            for key, value in dados_para_atualizar_params.items():
                if isinstance(value, str):                    
                    dados_para_atualizar_para_query += key + " = '" + value + "' "
                else:                    
                    dados_para_atualizar_para_query += key + " = " + str(value) + " "                

        update_cpu_query = "UPDATE CPUs SET " + dados_para_atualizar_para_query + " WHERE nome_de_guerra = '" + nome_de_guerra_atual +"'"
                
        try:            
            connection_conn = connection.Connection()
            conn = connection_conn.getConnection()
            cursor = conn.cursor()

            cursor.execute(update_cpu_query)
            conn.commit()
            print('*' * 30)
            print('CPU atualizado com sucesso:')
            print('Antes: ')
            for key, value in cpu_para_ser_atualizado.__repr__().items():
                print(key, value, sep=' > ')
            print('-' * 30)
            print('Dados atualizados: ')
            for key, value in dados_para_atualizar_params.items():
                print(key, value, sep=' > ')
            print('*' * 30)
        except sqlite3.OperationalError as err:
            print("Erro de Banco de Dados: ")
            print(err)
        finally:
            if 'conn' in locals():
                conn.close()
               
    
    def get_cpu(self, nome_de_guerra):
        if not isinstance(nome_de_guerra, str):
            raise ValueError('O parâmetro nome_de_guerra deve receber uma string.')            
        try:
            connection_conn = connection.Connection()
            conn = connection_conn.getConnection()
            cursor = conn.cursor()

            selectCpuQuery = "SELECT * FROM CPUs WHERE nome_de_guerra = '" + nome_de_guerra.upper() + "'"

            cursor.execute(selectCpuQuery)
            result = cursor.fetchall()            
            if len(result):
                cpu_instance = cpu.Cpu(result[0][1], result[0][2], result[0][3], result[0][4], result[0][5], result[0][6])
                return cpu_instance
            else:
                return None
        except sqlite3.OperationalError as err:
            print('Erro de Banco de Dados: ')
            print(err)
        finally:            
            if 'conn' in locals():
                conn.close()        

    def get_cpus(self):
        try:
            connection_conn = connection.Connection()
            conn = connection_conn.getConnection()
            cursor = conn.cursor()

            selectCpusQuery = "SELECT * FROM CPUs"

            cursor.execute(selectCpusQuery)
            result = cursor.fetchall()            
            conn.commit()

        except sqlite3.OperationalError as err:
            print('Erro de Banco de Dados: ')
            print(err)
        finally:
            conn.close()
            if 'result' in locals():
                return result
            return list()