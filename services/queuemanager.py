import db
import copy
import random

class QueueManager:
    def getNext(self, refQueue):
        connection = db.connection.Connection()
        conn = connection.getConnection()
        cursor = conn.cursor()
        
        getListaOrdem = 'SELECT ' + refQueue + ' FROM filaServicos'        
                
        cursor.execute(getListaOrdem)
        results = cursor.fetchall()

        listaOrdem = [elemento[0] for elemento in results if elemento[0] != 0 and elemento[0] != None]
        """ listaOrdem = list()

        for result in results:
            if result[0] != '0' and result[0] != None:
                listaOrdem.append(result[0]) """        
        
        minOrdem = min(listaOrdem)
        maxOrdem = max(listaOrdem)        
                     
        getNome = 'SELECT nome FROM filaServicos WHERE ' + refQueue + ' = ' + str(minOrdem)
        cursor.execute(getNome)
        nome = cursor.fetchone()[0]        

        vaiProFimDaFila = 'INSERT INTO filaServicos (nome, '+ refQueue +') VALUES (?, ?) '
        cursor.execute(vaiProFimDaFila, (nome, maxOrdem + 1))        
        
        updateOrdem = 'UPDATE filaServicos SET '+ refQueue +' = 0 WHERE '+ refQueue +' = ' + str(minOrdem)
        cursor.execute(updateOrdem)
        conn.commit()

        conn.close()
        return nome

    def zerarEPovoarFilas(self):
        connection = db.connection.Connection()
        conn = connection.getConnection()
        cursor = conn.cursor()

        cursor.execute("DELETE FROM filaServicos")

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
        
        queryInsert = "INSERT INTO filaServicos (nome, sem_12, sem_3, fds_12, sab_3, dom_3, sex_3) VALUES (?, ?, ?, ?, ?, ?, ?)"
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