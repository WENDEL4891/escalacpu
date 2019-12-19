import services
import entities
from dbdao import cpudao, impedimentodao, servicodao


""" queue = services.queuemaneger.QueueManager()
queue.zerarEPovoarFilas()

print('sem_12', queue.getNext("sem_12"))
print('sem_3', queue.getNext("sem_3")) """

#servico_dao = servicodao.ServicoDAO()
#servico_dao.servico_update('29/12/2019', 1, turno=2, nome_estagio='ASP JEAN', data='28/12/2019')
#servico_dao.servico_remove('19/01/2020', 1)
#servico_dao.servico_add('RENAN', '19/01/2020', 1, 'Ruan')
#servico_dao.servico_add('DIMITRI', '19/01/2020', 2)
#servico_dao.servico_add('HELDER', '16/01/2020', 3, 'gomes')
#servico_dao.servico_add('MADUREIRA', '15/01/2020', 1)
#servico_dao.servico_add('EVERTON CAMPOS', '15/01/2020', 2)
#for serv in servico_dao.get_servicos():
#    print(serv)

#cpu_dao = cpudao.CpuDAO()
#cpu_dao.cpu_add('2 tEN', 'NOVO CPU5 DA SILVA', 'CPu5', 'op', 'CFO', 2013)
#cpu_dao.cpu_remove('novo cpu')
#cpu_dao.cpu_update('cpu5', pg='1 tEN', funcao='adm', nome_completo='NOVO CPU5 SILVA', ano_base='2005')
#cpu_dao.cpu_remove('NOVO CPU5')
#cpu_dao.cpu_remove('NOVO CPU7')
#cpu_dao.cpu_remove('NOVO CPU9')
#cpu_dao.cpu_remove('NOVO CPU3')
#escalar = services.Escalar()
#escalar.escalarSeg_Sex()

#impedimento_dao = impedimentodao.ImpedimentoDAO()
#impedimento_dao.impedimento_add('madureira', 'ferias', '04/02/2020', '20/08/2020', 'comentário madureira')
#impedimento_dao.impedimento_add('cunha', 'ferias', '04/02/2020', '04/08/2020', 'comentário cunha')
#impedimento_dao.impedimento_add('jefferson', 'ferias', '11/07/2020', '13/08/2020', 'comentário jefferson')
#impedimento_dao.impedimento_add('fernanda', 'ferias', '11/07/2020', '13/08/2020', 'comentário fernanda')
#impedimento_dao.impedimento_add('renan', 'ferias', '04/07/2020', '20/08/2020', 'comentário renan')
#impedimento_dao.impedimento_add('helder', 'ferias', '21/07/2020', '25/08/2020', 'comentário madureira')

#impedimento_dao.impedimento_remove('cunha', '21/01/2020')
#impedimento_dao.impedimento_update('madureira', '11/01/2020', observacao='nova observacao', data_fim='22/01/2020')
#impedimentos = impedimento_dao.get_impedimentos_from_date()
#for imp in impedimentos:
#  for i in impedimento_dao.get_impedimentos_from_date('11/07/2020', '    print(i)
#impedimento = impedimentoDao.getImpedimento('jefferson', '05/01/2020')
#print(impedimento.__rep__())
#cpu = Cpu('2 ten', 'maia silva', 'MAIa', 'op', 'cfo', 2020)
#print(cpu.__rep__())

#impedimento = Impedimento('maia', 'ferias', '10/10/2020', '20/10/2020')
#print(impedimento.data_inicio)
#print(impedimento.data_fim)