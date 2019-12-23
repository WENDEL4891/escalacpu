import services
import entities
from dbdao import cpudao, impedimentodao, servicodao, feriadodao, ordenacaopormilitardao


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
#cpus = cpu_dao.get_cpus()
#cabecalio = '{:^8} | {:^40} | {:^20} | {:^7} | {:^7} | {:^12}'.format('PG', 'NOME COMPLETO', 'NOME DE GUERRA', 'FUNCAO', 'CURSO', 'ANO BASE')

#print(cabecalio)
#print('-' * len(cabecalio))
#for cpu in cpus:
#    ano_base = cpu.ano_base if cpu.ano_base != None else '----'
#    cpu_format = '{c.pg:^8} | {c.nome_completo:<40} | {c.nome_de_guerra:<20} | {c.funcao:<7} | {c.curso:<7} | {0:^12}'.format(ano_base, c=cpu)
#    print(cpu_format)
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

#feriado_dao = feriadodao.FeriadoDAO()
#feriado_dao.feriado_add('31/10/2020', 'Dia dos velhos')
#feriado_dao.feriado_remove('25/10/2020')
#feriado_dao.feriado_remove('26/10/2020')
#feriado_dao.feriado_remove('29/10/2020')
#feriado_dao.feriado_remove('28/10/2020')
#feriado_dao.feriado_update('27/10/2020', tipo='NOVO TIPO3')
#feriado_dao.feriado_update('28/10/2020', tipo='8')
#feriados = feriado_dao.get_feriados()
#cabecalio = '{:^12} | {:^30}'.format('DATA', 'TIPO')

#print(cabecalio)
#print('-' * len(cabecalio))
#for feriado in feriados:
#    data = '{f.data:%d/%m/%Y}'.format(f=feriado)
#    feriado_format = '{:<12} | {f.tipo:<30}'.format(data, f=feriado)
#    print(feriado_format)
ordenacao_por_militar_dao = ordenacaopormilitardao.OrdenacaoPorMilitarDAO()
#ordenacao_por_militar_dao.ordenacao_por_militar_add('cunha',1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 112)
#print(ordenacao_por_militar_dao.get_ordenacao_por_militar('rodrigo'))
ordenacao = ordenacao_por_militar_dao.get_ordenacao_por_modalidade('qua_12')
print(ordenacao)