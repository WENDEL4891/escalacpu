import csv
from dbdao import servicodao
import sys

servico_dao = servicodao.ServicoDAO()
try:
    file_obj = open('servicos.csv', 'r', encoding='utf8')
except:
    erros = sys.exc_info()
    for i in range(len(erros) - 1):
        print(erros[i])
        raise
else:
    with file_obj:
        file_reader = csv.reader(file_obj, quotechar=",")
        for line in file_reader:            
            servico_dao.servico_add(line[0], line[1], line[2])