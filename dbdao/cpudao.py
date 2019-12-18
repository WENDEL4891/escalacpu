from entities import cpu
from db import connection
import sqlite3
import myexceptions
import copy

class CpuDAO:
    def cpu_add(self, pg, nome_completo, nome_de_guerra, funcao, curso, ano_base):        
        try:
            cpu_instance = cpu.Cpu(pg, nome_completo, nome_de_guerra, funcao, curso, ano_base)
            
            connection_conn = connection.Connection()
            conn = connection_conn.get_connection()
            cursor = conn.cursor()
            
            addQuery = "INSERT INTO CPUs (pg, nome_completo, nome_de_guerra, funcao, curso, ano_base) VALUES (?, ?, ?, ?, ?, ?)"
            params = (cpu_instance.pg, cpu_instance.nome_completo, cpu_instance.nome_de_guerra, cpu_instance.funcao, cpu_instance.curso, cpu_instance.ano_base)
            
            cursor.execute(addQuery, params)
            conn.commit()
            if cursor.rowcount == 1:
                print('Novo CPU cadastrado com sucesso: ')
                for key, value in cpu_instance.__repr__().items():
                    print(key, value, sep=' > ')
                print('\'' * 40 )
            else:
                raise myexceptions.BdOperationError('O cadastro não foi realizado. Causa não identificada.')

        except sqlite3.OperationalError as err:
            print('Erro de Banco de Dados : ')
            print(err)
            raise
        except sqlite3.IntegrityError as err:
            print('Já existe um registro com o nome de guerra: ' + cpu_instance.nome_de_guerra)
            raise
        finally:
            if 'conn' in locals():
                conn.close()

    def cpu_remove(self, nome_de_guerra):
        cpu_para_ser_removido = self.get_cpu(nome_de_guerra)
        if cpu_para_ser_removido == None:
            raise ValueError('Não há cpu com o nome de guerra informado (' + nome_de_guerra + '), para remoção.')
        try:
            connection_conn = connection.Connection()
            conn = connection_conn.get_connection()
            cursor = conn.cursor()

            rm_query = "DELETE FROM CPUs WHERE nome_de_guerra = '" + cpu_para_ser_removido.nome_de_guerra + "'"

            cursor.execute(rm_query)                       
            conn.commit()
            if cursor.rowcount:
                print('CPU removido com sucesso: ')
                print(cpu_para_ser_removido)
                print('\'' * 40)
            else:
                print('Não foi realizada a remoção do cpu (' + cpu_para_ser_removido.nome_de_guerra + '). Causa não identificada.')

        except sqlite3.OperationalError as err:
            print('Erro ao tentar excluir do banco de dados o cpu : ')
            print(cpu_para_ser_removido)
            print('Tipo do erro: ', sys.exc_info()[0], sep=' > ')
            print('Descrição do erro: ', sys.exc_info()[1], sep=' > ')
            raise
        finally:
            if 'conn' in locals():
                conn.close()
    
    def cpu_update(self, nome_de_guerra_atual, pg='', nome_completo='', nome_de_guerra='', funcao='', curso='', ano_base=''):
        cpu_para_ser_atualizado = self.get_cpu(nome_de_guerra_atual)
        if cpu_para_ser_atualizado == None:
            raise ValueError('Não há CPU com o nome de guerra informado, para ser atualizado.')

        if pg == nome_completo == nome_de_guerra == funcao == curso == ano_base == '':
            raise NameError('Deve ser informado ao menos 1 campo para ser atualizado dentre os seguintes: '\
                + ', '.join(list(cpu_para_ser_atualizado.__repr__())) + '.')
        
        novo_cpu_dict = {
            'nome_de_guerra': nome_de_guerra if nome_de_guerra != '' else cpu_para_ser_atualizado.nome_de_guerra,
            'nome_completo': nome_completo if nome_completo != '' else cpu_para_ser_atualizado.nome_completo,
            'pg': pg if pg != '' else cpu_para_ser_atualizado.pg,
            'funcao': funcao if funcao != '' else cpu_para_ser_atualizado.funcao,
            'curso': curso if curso != '' else cpu_para_ser_atualizado.curso,
            'ano_base': ano_base if ano_base != '' else cpu_para_ser_atualizado.ano_base
        }

        novo_cpu_obj = cpu.Cpu(
            pg=novo_cpu_dict['pg'],
            nome_completo=novo_cpu_dict['nome_completo'],
            nome_de_guerra=novo_cpu_dict['nome_de_guerra'],
            funcao=novo_cpu_dict['funcao'],
            curso=novo_cpu_dict['curso'],
            ano_base=novo_cpu_dict['ano_base']
        )
                       
        if cpu_para_ser_atualizado == novo_cpu_obj:
            raise myexceptions.LogicException('Não foi informado nenhum dado novo para atualização.')
                        
        dados_para_atualizar_para_query = ''        
        
        for key, value in novo_cpu_obj.__repr__().items():
            dados_para_atualizar_para_query += key + " = '" + str(value) + "', "
        
        dados_para_atualizar_para_query = dados_para_atualizar_para_query[0:-2]        

        update_cpu_query = "UPDATE CPUs SET " + dados_para_atualizar_para_query + " WHERE nome_de_guerra = '" + nome_de_guerra_atual.upper() +"'"
                
        try:            
            connection_conn = connection.Connection()
            conn = connection_conn.get_connection()
            cursor = conn.cursor()

            cursor.execute(update_cpu_query)
            conn.commit()
            antes_dict = cpu_para_ser_atualizado.__repr__()
            depois_dict = novo_cpu_obj.__repr__()
            if cursor.rowcount == 1:
                print('CPU atualizado com sucesso:')
                for key, value in antes_dict.items():
                    if antes_dict[key] != depois_dict[key]:
                        print(key, value, sep=' > ', end='')
                        print(' # atualizado para ' + str(depois_dict[key]), sep=': ')
                    else:
                        print(key, value, sep=' > ')
                print('\'' * 40)
            else:
                print('Problema na atualização. Causa ignorada')
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
            conn = connection_conn.get_connection()
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
            conn = connection_conn.get_connection()
            cursor = conn.cursor()

            select_cpus_query = "SELECT * FROM CPUs"

            cursor.execute(select_cpus_query)
            results = cursor.fetchall()                        
            cpus = list()

            for result in results:                
                cpu_instance = cpu.Cpu(result[1], result[2], result[3], result[4], result[5], result[6])
                cpus.append(cpu_instance)
            return cpus            
        except sqlite3.OperationalError as err:
            print('Erro de Banco de Dados: ')
            print(err)        
        finally:
            if 'conn' in locals():
                conn.close()         