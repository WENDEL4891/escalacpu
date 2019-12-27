import connection
import sys


create_tables_queries = (
    '''
    CREATE TABLE IF NOT EXISTS "CPUs" (
        "id"	INTEGER PRIMARY KEY AUTOINCREMENT,
        "pg"	TEXT NOT NULL,
        "nome_completo"	TEXT NOT NULL,
        "nome_de_guerra"	TEXT NOT NULL UNIQUE,
        "funcao"	TEXT NOT NULL,
        "curso"	TEXT,
        "ano_base"	INTEGER
    )    
    ''',
    '''
    CREATE TABLE IF NOT EXISTS "feriados" (
        "data"	TEXT,
        "tipo"	INTEGER NOT NULL,
        PRIMARY KEY("data")
    )   
    ''',
    '''
    CREATE TABLE IF NOT EXISTS "impedimentos" (
        "id"	INTEGER PRIMARY KEY AUTOINCREMENT,
        "nome_de_guerra"	TEXT,
        "tipo"	TEXT,
        "data_inicio"	TEXT,
        "data_fim"	TEXT,
        "observacao"	TEXT
    )
    ''',
    '''
    CREATE TABLE IF NOT EXISTS "ordenacao_por_militar" (
        "nome_de_guerra"	TEXT NOT NULL,
        "seg_12"	INTEGER,
        "seg_3"	INTEGER,
        "ter_qui_sex_12"	INTEGER,
        "qua_12"	INTEGER,
        "ter_3"	INTEGER,
        "qua_3"	INTEGER,
        "qui_3"	INTEGER,
        "sex_3"	INTEGER,
        "fds_12"	INTEGER,
        "sab_3"	INTEGER,
        "dom_3"	INTEGER,
        PRIMARY KEY("nome_de_guerra")
    )
    ''',
    '''
    CREATE TABLE IF NOT EXISTS "servicos" (
        "nome_de_guerra"	INTEGER NOT NULL,
        "data"	TEXT NOT NULL,
        "turno"	INTEGER NOT NULL,
        "nome_estagio"	TEXT,
        PRIMARY KEY("data","turno")
    )
    '''    
)

try:    
    _connection = connection.Connection()
    conn = _connection.get_connection()
    cursor = conn.cursor()

    for query in create_tables_queries:
        cursor.execute(query)
except:
    erros = sys.exc_info()
    for i in range(len(erros) - 1):
        print(erros[i])
        raise
else:
    print('Queries executadas com sucesso: ')
    for query in create_tables_queries:
        print(query)
        print('-' * 40)
finally:
    if 'conn' in locals():
        conn.close()

