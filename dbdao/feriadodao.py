from entities import Feriado
from db import Connection
import sqlite3
from datetime import datetime

class FeriadoDAO:
    def feriadoAdd(self, data, tipo):        
        try:
            feriado = Feriado(data, tipo)
            
            connection = Connection()
            conn = connection.get_connection()
            cursor = conn.cursor()
            
            addQuery = "INSERT INTO feriados VALUES (?, ?)"
            
            cursor.execute(addQuery, (feriado.data, feriado.tipo))
            conn.commit()
            conn.close()
        except sqlite3.OperationalError as err:
            print('Deu o seguinte erro: ')
            print(err)
    
    def getFeriadosEmPeriodo(self, dataInicial, dataFinal):        
        dataInicialFormatada = datetime.strftime(dataInicial, '%Y-%m-%d')
        dataFinalFormatada = datetime.strftime(dataFinal, '%Y-%m-%d')
        
        connection = Connection()
        conn = connection.get_connection()
        cursor = conn.cursor()

        getFeriadoQuery = "SELECT * FROM feriados WHERE data >= '" + dataInicialFormatada +"' AND data <= '" + dataFinalFormatada + "'"
        cursor.execute(getFeriadoQuery)
        results = cursor.fetchall()        
        conn.close()
        
        feriadosDict = dict()
        for result in results:
            feriadosDict[result[0]] = result[1]
        return feriadosDict
