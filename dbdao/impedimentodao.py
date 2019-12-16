from entities import Impedimento
from db import Connection
from .cpudao import CpuDAO
import sqlite3
from datetime import datetime
import services
import myprogramerrors


class ImpedimentoDAO:
    def impedimentoAdd(self, nomeDeGuerra, tipo, dataInicio, dataFim='', observacao=''):        
        impedimento = Impedimento(nomeDeGuerra, tipo, dataInicio, dataFim, observacao)
        try:
            connection = Connection()
            conn = connection.getConnection()
            cursor = conn.cursor()
            
            dtaInFormat = datetime.strftime(impedimento.dataInicio, '%Y-%m-%d')
            dtaFimFormat = datetime.strftime(impedimento.dataFim, '%Y-%m-%d')

            primCond = "nomeDeGuerra = '" + impedimento.nomeDeGuerra + "'"
            segCond = "'" + dtaInFormat + "' BETWEEN DATE(dataInicio) AND DATE(dataFim)"            
            terCond = "DATE(dataInicio) BETWEEN '" + dtaInFormat + "' AND '" + dtaFimFormat + "'"
            quarCond = "DATE(dataFim) BETWEEN '" + dtaInFormat + "' AND '" + dtaFimFormat + "'"
            condicoes = "(" + primCond + ") AND ( (" + segCond + ") OR (" + terCond + ") OR (" + quarCond + ") )"

            selectQuery = "SELECT nomeDeGuerra, tipo, dataInicio, dataFim FROM impedimentos WHERE " + condicoes
            
            cursor.execute(selectQuery)
            
            impedimentosConflitantes = cursor.fetchall()
            
            if len(impedimentosConflitantes):
                complemento = ''
                for impedimentoConflitante in impedimentosConflitantes:                    
                    inicio = services.functions.invertFormatDateStr(impedimentoConflitante[2])
                    fim = services.functions.invertFormatDateStr(impedimentoConflitante[3])

                    complemento += '\nNome de guerra: ' + impedimentoConflitante[0] + '\nTipo: ' + impedimentoConflitante[1] + '\nInicio: ' + inicio + '\nFim: ' + fim + '\n' + '-' * 20
                
                msgErro = 'Impedimento conflitante com o(s) seguinte(s): ' + complemento                
                
                raise ValueError(msgErro)

            addQuery = "INSERT INTO impedimentos (nomeDeGuerra, tipo, dataInicio, dataFim, observacao) VALUES (?, ?, ?, ?, ?)"
            
            cursor.execute(addQuery, (impedimento.nomeDeGuerra, impedimento.tipo, impedimento.dataInicio.date(), impedimento.dataFim.date(), impedimento.observacao))
            conn.commit()
            print('Impedimento cadastrado com sucesso: ')
            for key, value in impedimento.__rep__().items():
                print(key, value, sep=' > ')

        except sqlite3.OperationalError as err:
            print('Erro de Banco de Dados : ')
            print(err)
        finally:
            if 'conn' in locals():
                conn.close()

    def impedimentoRemove(self, nomeDeGuerra, dataInicio):
        impedimento_para_ser_removido = self.getImpedimento(nomeDeGuerra, dataInicio)
        

        try:
            connection = Connection()
            conn = connection.getConnection()
            cursor = conn.cursor()
           
            nomeDeGuerraFormat = impedimento_para_ser_removido.nome_de_guerra
            
            print(impedimento_para_ser_removido.__repr__())
            print(impedimento_para_ser_removido.nome_de_guerra)
            print(impedimento_para_ser_removido.data_inicio)
            print(type(impedimento_para_ser_removido.data_inicio))
            print(impedimento_para_ser_removido.tipo)

            dataInicioFormat = datetime.strftime(impedimento_para_ser_removido.data_inicio, '%Y-%m-%d')

            rmQuery = "DELETE FROM impedimentos WHERE nomeDeGuerra = '" + nomeDeGuerraFormat + "' AND DATE(dataInicio) = '" + dataInicioFormat + "'"

            cursor.execute(rmQuery)
            conn.commit()

            if cursor.rowcount == 1:
                print('Impedimento excluído com sucesso: ')
                print(impedimento_para_ser_removido.__repr__())            

        except sqlite3.OperationalError as err:
            print('Erro de Banco de Dados: ')
            print(err)
        finally:
            if 'conn' in locals():
                conn.close()
    
    def impedimentoUpdate(self, nomeDeGuerraAtual, dataInicioAtual, **dadosParaAtualizarParams):
        impedimentoParaAtualizar = self.getImpedimento(nomeDeGuerraAtual, dataInicioAtual)
        if impedimentoParaAtualizar == None:
            raise ValueError('Não há impedimento com o nome de guerra e data de início informados.')
                        
        if (not type(nomeDeGuerraAtual) == type(dataInicioAtual) == str):
            raise TypeError('O nome de guerra e a data de início devem ser strings.')
        else:
            nomeDeGuerraAtual = nomeDeGuerraAtual.upper()

        try:
            datetime.strptime(dataInicioAtual, '%d/%m/%Y')
        except ValueError:
            raise ValueError('As datas devem ser informadas no formato dd/mm/AAAA.')
        
        
        parametrosValidos = ['nomeDeGuerra', 'tipo', 'dataInicio', 'dataFim', 'observacao']
        if len(dadosParaAtualizarParams) == 0:
            raise NameError('Deve ser informado ao menos 1 campo para ser atualizado dentre os seguintes: \n\t'\
                + ', '.join(parametrosValidos) + '.')
        
        for key, value in dadosParaAtualizarParams.items():
            if type(value) == str:
                dadosParaAtualizarParams[key] = value.upper()            
            else:
                raise TypeError('Todos os parâmetros devem ser do tipo string.')
        
        parametrosInformados = list(dadosParaAtualizarParams)
                
        
        
        if 'dataInicio' in parametrosInformados and 'dataFim' in parametrosInformados:
            try:
                di = datetime.strptime(dadosParaAtualizarParams['dataInicio'], '%d/%m/%Y')
                df = datetime.strptime(dadosParaAtualizarParams['dataFim'], '%d/%m/%Y')
            except ValueError:
                raise ValueError('As datas devem ser informadas no formato dd/mm/AAAA.')
            if di > df:
                raise ValueError('A data de início não pode ser posterior a data fim.')
            dadosParaAtualizarParams['dataInicio'] = datetime.strftime(di, '%Y-%m-%d')
            dadosParaAtualizarParams['dataFim'] = datetime.strftime(df, '%Y-%m-%d')
        if 'dataInicio' in parametrosInformados and 'dataFim' not in parametrosInformados:        
            try:
                di = datetime.strptime(dadosParaAtualizarParams['dataInicio'], '%d/%m/%Y')                
            except ValueError:
                raise ValueError('As datas devem ser informadas no formato dd/mm/AAAA.')
            if di.date() > impedimentoParaAtualizar.dataFim:
                raise ValueError('A data de início não pode ser posterior a data fim.')
            dadosParaAtualizarParams['dataInicio'] = datetime.strftime(di, '%Y-%m-%d')
        if 'dataFim' in parametrosInformados and 'dataInicio' not in parametrosInformados:
            try:                
                df = datetime.strptime(dadosParaAtualizarParams['dataFim'], '%d/%m/%Y')
            except ValueError:
                raise ValueError('As datas devem ser informadas no formato dd/mm/AAAA.')            
            if df.date() < impedimentoParaAtualizar.dataInicio:
                raise ValueError('A data fim deve ser posterior a data de início.')
            dadosParaAtualizarParams['dataFim'] = datetime.strftime(df, '%Y-%m-%d')        
            
        
        parametrosInvalidos = list()
        for key in dadosParaAtualizarParams:
            if key not in parametrosValidos:
                parametrosInvalidos.append(key)
        
        if len(parametrosInvalidos):
            raise ValueError('Somente devem ser passados parâmetros dentre os seguintes: ' + ', '.join(parametrosValidos) + '.')
        
        dadosAtuaisList = self.getImpedimento(nomeDeGuerraAtual, dataInicioAtual)
                
        """ if len(dadosAtuaisList) == 0:
            raise NameError('Não há impedimento com os parâmetros informados.') """

        dadosParaAtualizarParaQuery = ''        
        
        for key, value in dadosParaAtualizarParams.items():                
            dadosParaAtualizarParaQuery += key + " = '" + value + "', "
        dadosParaAtualizarParaQuery = dadosParaAtualizarParaQuery[0:-2]        
        
        dataInicioAtualFormat = services.functions.invertFormatDateStr(dataInicioAtual)

        updateQuery = "UPDATE impedimentos SET " + dadosParaAtualizarParaQuery + " WHERE nomeDeGuerra = '" + nomeDeGuerraAtual +"' AND DATE(dataInicio) = '" + dataInicioAtualFormat + "'"        
                
        try:            
            connection = Connection()
            conn = connection.getConnection()
            cursor = conn.cursor()
            cursor.execute(updateQuery)
            conn.commit()
            
            import copy        
            if cursor.rowcount == 1:                                
                antes = impedimentoParaAtualizar.__rep__()            
                depois = copy.copy(antes)
                for key, value in depois.items():
                    if key in list(dadosParaAtualizarParams):
                        if key in ['dataInicio', 'dataFim']:
                            depois[key] = services.functions.invertFormatDateStr(dadosParaAtualizarParams[key])
                        else:
                            depois[key] = dadosParaAtualizarParams[key]

                print('Impedimento atualizado com sucesso:')
                print('Antes: ', antes)
                print('Depois: ', depois)
                print('-' * 30)
                print('Parâmetros atualizados:')                
                for key, value in dadosParaAtualizarParams.items():
                    if key == 'dataInicio':
                        print(key, datetime.strftime(di, '%d/%m/%Y'), sep=' > ')
                    elif key == 'dataFim':
                        print(key, datetime.strftime(df, '%d/%m/%Y'), sep=' > ')
                    else:
                        print(key, value, sep=' > ')
            else:
                print('Não há impedimento com o nome e data de início informados.')
        except sqlite3.OperationalError as err:
            print("Erro de Banco de Dados: ")
            print(err)
        finally:
            if 'conn' in locals():
                conn.close()
               
    
    def getImpedimento(self, nomeDeGuerra, dataInicio):        
        if not isinstance(nomeDeGuerra, str) and isinstance(dataInicio, str):
            raise TypeError('O nome de guerra e a data de início devem ser strings.')        
        nomeDeGuerraFormat = nomeDeGuerra.upper()

        dataInicioDatetime = services.functions.date_str_to_datetime(dataInicio)
        dataInicioFormat = datetime.strftime(dataInicioDatetime, '%Y-%m-%d')               
        
        selectQuery = "SELECT nomeDeGuerra, tipo, dataInicio, dataFim, observacao FROM impedimentos WHERE nomeDeGuerra  = '" + nomeDeGuerraFormat + "' AND  dataInicio = '" + dataInicioFormat + "'"        
        
        try:           
            connection = Connection()
            conn = connection.getConnection()            
            cursor = conn.cursor()
            
            cursor.execute(selectQuery)
            result = cursor.fetchall()            
            
            if len(result) > 1:
                raise myprogramerrors.IntegrityError('Há mais de um registro com o mesmo nome de guerra e data de início.')
            elif len(result) == 1:
                impedimento = Impedimento(result[0][0], result[0][1], result[0][2], result[0][3], result[0][4])
                return impedimento
            else:
                return None
        except sqlite3.OperationalError as err:            
            print('Erro de Banco de Dados: ')
            print(err)
            raise
        finally:            
            if 'conn' in locals():
                conn.close()

    def getImpedimentos(self, dataInicio='', dataFim=''):
        if not type(dataInicio) == type(dataFim) == str:
            raise ValueError('Os parâmetros são opcionais. Mas se informados, devem ser strings.')
        
        if len(dataInicio) != len(dataFim):
            raise ValueError('Informe uma data de início e uma de fim do período. Ou não informe nenhuma data.')
        
        complementoQuery = ''
        if len(dataInicio):
            try:
                if datetime.strptime(dataInicio, '%d/%m/%Y') > datetime.strptime(dataFim, '%d/%m/%Y'):
                    raise ValueError('A data fim deve ser superior a data de início.')
            except ValueError:
                raise ValueError('Informe as datas no formato dd/mm/AAAA. Ou não informe nenhuma data.')
            
            dia = dataInicio[:2]
            mes = dataInicio[3:5]
            ano = dataInicio[6:]
            dtaInFormat = ano + '-' + mes + '-' + dia        

            dia = dataFim[:2]
            mes = dataFim[3:5]
            ano = dataFim[6:]
            dtaFimFormat = ano + '-' + mes + '-' + dia        
        
        primCond = "'" + dtaInFormat + "' BETWEEN DATE(dataInicio) AND DATE(dataFim)"        
        segCond = "DATE(dataInicio) BETWEEN '" + dtaInFormat + "' AND '" + dtaFimFormat + "'"
        terCond = "DATE(dataFim) BETWEEN '" + dtaInFormat + "' AND '" + dtaFimFormat + "'"
        condicoes = "(" + primCond + ") OR (" + segCond + ") OR (" + terCond + ")"

        selectQuery = "SELECT nomeDeGuerra, tipo, dataInicio, dataFim FROM impedimentos WHERE " + condicoes          
        
        try:
            connection = Connection()
            conn = connection.getConnection()
            cursor = conn.cursor()            

            cursor.execute(selectQuery)
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