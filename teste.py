import services
import dbdao
import entities
from dbdao import cpudao, impedimentodao


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
#cpu_dao.cpu_add('2 tEN', 'NOVO CPU6 DA SILVA', 'NOVO CPu', 'op', 'CFO', 2013)
#cpu_dao.cpu_remove('NOVO CPU7')
cpu_dao.cpu_update('cpu5', pg='1 tEN', funcao='adm', nome_completo='NOVO CPU5 SILVA')
#cpu_dao.cpu_remove('NOVO CPU5')
#cpu_dao.cpu_remove('NOVO CPU7')
#cpu_dao.cpu_remove('NOVO CPU9')
#cpu_dao.cpu_remove('NOVO CPU3')

#escalar = services.Escalar()
#escalar.escalarSeg_Sex()

#impedimento_dao = impedimentodao.ImpedimentoDAO()
#impedimento_dao.impedimento_add('madureira', 'ferias', '04/02/2020', '20/02/2020')
#impedimento_dao.impedimento_remove('cunha', '21/01/2020')
#impedimento_dao.impedimento_update('madureira', '11/01/2020', observacao='nova observacao', data_fim='22/01/2020')
#for i in impedimentoDao.getImpedimentos('29/01/2020', '27/01/2020'):
#    print(i)
#impedimento = impedimentoDao.getImpedimento('jefferson', '05/01/2020')
#print(impedimento.__rep__())
#cpu = Cpu('2 ten', 'maia silva', 'MAIa', 'op', 'cfo', 2020)
#print(cpu.__rep__())

#impedimento = Impedimento('maia', 'ferias', '10/10/2020', '20/10/2020')
#print(impedimento.data_inicio)
#print(impedimento.data_fim)