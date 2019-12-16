import services
import dbdao
import entities
from dbdao import cpudao


""" queue = services.queuemaneger.QueueManager()
queue.zerarEPovoarFilas()

print('sem_12', queue.getNext("sem_12"))
print('sem_3', queue.getNext("sem_3")) """

""" servicoDao = dbdao.servicodao.ServicoDAO()
servicoDao.servicoAdd('TEN RENAN', '01/01/2020', 1)
servicoDao.servicoAdd('TEN DIMITRI', '28/12/2019', 2)
servicoDao.servicoAdd('TEN HELDER', '30/12/2019', 3)
servicoDao.servicoAdd('TEN MADUREIRA', '05/01/2020', 1)
servicoDao.servicoAdd('TEN EVERTON CAMPOS', '04/01/2020', 2) """

cpu_dao = cpudao.CpuDAO()
#cpu_dao.cpu_add('2 tEN', 'NOVO CPU6 DA SILVA', 'NOVO CPu9', 'op', 'CFO', 2013)
#cpu_dao.cpu_remove('NOVO CPU7')
cpu_dao.cpu_update('NOVO CPU9', pg='2 tEN', funcao='op', nome_completo='NOVO CPU9 DA SILVA')
#cpu_dao.cpu_remove('NOVO CPU')
#cpu_dao.cpu_remove('NOVO CPU3')

#escalar = services.Escalar()
#escalar.escalarSeg_Sex()

#impedimentoDao = dbdao.impedimentodao.ImpedimentoDAO()
#impedimentoDao.impedimentoAdd('CUNHA', 'LICENCAS/dispensas regulamentares', '19/01/2020', '22/01/2020', observacao='')
#impedimentoDao.impedimentoRemove('cunha', '15/01/2020')
#impedimentoDao.impedimentoUpdate('jefferson', '22/01/2020', dataFim='22/01/2020')
#for i in impedimentoDao.getImpedimentos('29/01/2020', '27/01/2020'):
#    print(i)
#impedimento = impedimentoDao.getImpedimento('jefferson', '05/01/2020')
#print(impedimento.__rep__())
#cpu = Cpu('2 ten', 'maia silva', 'MAIa', 'op', 'cfo', 2020)
#print(cpu.__rep__())

#impedimento = Impedimento('maia', 'ferias', '10/10/2020', '20/10/2020')
#print(impedimento.data_inicio)
#print(impedimento.data_fim)