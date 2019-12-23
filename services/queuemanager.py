import db
import copy
import random
import sys

class QueueManager:
    def getNext(self, ref_queue):
        try:
            connection = db.connection.Connection()
            conn = connection.getConnection()
            cursor = conn.cursor()
            
            get_lista_ordem = 'SELECT {} FROM filas_servicos'.format(ref_queue)        
                    
            cursor.execute(get_lista_ordem)
            results = cursor.fetchall()
        except:
            print('Erro ao buscar dados na tabela filas_servicos, no banco de dados.')
            erros = sys.exc_info()
            for i in range(len(erros) - 1):
                print(erros[i])

        if results:
            listaOrdem = [elemento[0] for elemento in results]
        else:
            print("A query SQL no banco de dados não retornou nenhum dado da fila {}, na tabela filas_servicos.".format(ref_queue))
        
        min_ordem = min(listaOrdem)
        max_ordem = max(listaOrdem)


        
        
        update_ordem = "UPDATE filas_servicos SET {} = {}".format()
        getNome = 'SELECT nome FROM filas_servicos WHERE ' + refQueue + ' = ' + str(minOrdem)
        cursor.execute(getNome)
        nome = cursor.fetchone()[0]        

        vaiProFimDaFila = 'INSERT INTO filas_servicos (nome, '+ refQueue +') VALUES (?, ?) '
        cursor.execute(vaiProFimDaFila, (nome, maxOrdem + 1))        
        
        updateOrdem = 'UPDATE filas_servicos SET '+ refQueue +' = 0 WHERE '+ refQueue +' = ' + str(minOrdem)
        cursor.execute(updateOrdem)
        conn.commit()

        conn.close()
        return nome

    def zerarEPovoarFilas(self):
        connection = db.connection.Connection()
        conn = connection.getConnection()
        cursor = conn.cursor()

        cursor.execute("DELETE FROM filas_servicos")

        cursor.execute("SELECT pg, nomeDeGuerra, funcao FROM CPUs")
        results = cursor.fetchall()

        listaCPUs = [result[0] + ' ' + result[1] for result in results if result[2] != 'CT']

                
        qtdCPUs = len(listaCPUs)
        
        listaOrdens = [elemento for elemento in range(1, qtdCPUs + 1)]
        
        listaSem12 = copy.copy(listaOrdens)
        random.shuffle(listaSem12)

        listaSem3 = copy.copy(listaOrdens)
        random.shuffle(listaSem3)

        listaFds12 = copy.copy(listaOrdens)
        random.shuffle(listaFds12)

        listaSab3 = copy.copy(listaOrdens)
        random.shuffle(listaSab3)

        listaDom3 = copy.copy(listaOrdens)
        random.shuffle(listaDom3)

        listaSex3 = copy.copy(listaOrdens)
        random.shuffle(listaSex3)
        
        queryInsert = "INSERT INTO filas_servicos (nome, sem_12, sem_3, fds_12, sab_3, dom_3, sex_3) VALUES (?, ?, ?, ?, ?, ?, ?)"
        for num in range(0, qtdCPUs):            
            conn.execute(queryInsert,
                (
                    listaCPUs[num],
                    listaSem12[num],
                    listaSem3[num],
                    listaFds12[num],
                    listaSab3[num],
                    listaDom3[num],
                    listaSex3[num]                    
                )                
            )
        conn.commit()
        conn.close()