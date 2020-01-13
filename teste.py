from services import escalarsemana
from entities import filapormodalidade, servico
from dbdao import cpudao, impedimentodao, servicodao, feriadodao, ordenacaopormilitardao
import datetime



""" queue = services.queuemaneger.QueueManager()
queue.zerarEPovoarFilas()

print('sem_12', queue.getNext("sem_12"))
print('sem_3', queue.getNext("sem_3")) """

#servico_dao = servicodao.ServicoDAO()
#servico_dao.servico_add('03/02/2020', 1, 'DIMITRi')
#servico_dao.servico_add('04/03/2021', 2, 'FERNANDA')
#servico_dao.servico_add('04/03/2021', 3, 'CUNHA')
#servico_dao.servico_add('05/01/2021', 1, 'MARCELO')
#servico_dao.servico_add('JONAS', '05/01/2021', 2)
#servico_dao.servico_add('GONDIM', '05/01/2021', 3)
#servico_dao.servico_add('JEFFERSON', '06/01/2021', 1)
#servico_dao.servico_add('MAIA', '06/01/2021', 2)
#servico_dao.servico_add('ERNANE', '06/01/2021', 3)
#servico_dao.servico_add('CUNHA', '07/01/2021', 1)
#servico_dao.servico_add('lucas', '07/01/2021', 2)
#servico_dao.servico_add('DIMITRI', '07/01/2021', 3)
#servico_dao.servico_add('RENAN', '08/01/2021', 1)
#servico_dao.servico_add('FERNANDA', '08/01/2021', 2)
#servico_dao.servico_add('CUNHA', '08/01/2021', 3)
#servico_dao.servico_add('MARCELO', '09/01/2021', 1)
#servico_dao.servico_add('JONAS', '09/01/2021', 2)
#servico_dao.servico_add('GONDIM', '09/01/2021', 3)
#servico_dao.servico_add('JEFFERSON', '10/01/2021', 1)
#servico_dao.servico_add('MAIA', '10/01/2021', 2)
#servico_dao.servico_add('ERNANE', '10/01/2021', 3)
#servico_dao.servico_add('RENA', '19/01/2020', 1, 'Ruan')
#servico_dao.servico_add('HELDER', '16/01/2020', 3, 'gomes')
#servico_dao.servico_add('MADUREIRA', '15/01/2020', 1)
#servico_dao.servico_add('EVERTON CAMPOS', '15/01/2020', 2)
#servico_dao.servico_update('04/03/2021', 1, nome_estagio='ASP ruan JÚNIOR',_cpu='EVERTON CAMPOS')
#servico_dao.servico_remove('19/01/2020', 1)
#for serv in servico_dao.get_servicos():
#    print(serv)
#_servico = servico_dao.get_servico('04/01/2021', 1)
#print(_servico.get_modalidade())
#_servico = servico_dao.get_servico('04/01/2021', 2)
#print(_servico.get_modalidade())
#_servico = servico_dao.get_servico('04/01/2021', 3)
#print(_servico.get_modalidade())
#_servico = servico_dao.get_servico('05/01/2021', 1)
#print(_servico.get_modalidade())
#_servico = servico_dao.get_servico('05/01/2021', 2)
#print(_servico.get_modalidade())
#_servico = servico_dao.get_servico('05/01/2021', 3)
#print(_servico.get_modalidade())
#_servico = servico_dao.get_servico('06/01/2021', 1)
#print(_servico.get_modalidade())
#_servico = servico_dao.get_servico('06/01/2021', 2)
#print(_servico.get_modalidade())
#_servico = servico_dao.get_servico('06/01/2021', 3)
#print(_servico.get_modalidade())
#_servico = servico_dao.get_servico('07/01/2021', 1)
#print(_servico.get_modalidade())
#_servico = servico_dao.get_servico('07/01/2021', 2)
#print(_servico.get_modalidade())
#_servico = servico_dao.get_servico('07/01/2021', 3)
#print(_servico.get_modalidade())
#_servico = servico_dao.get_servico('08/01/2021', 1)
#print(_servico.get_modalidade())
#_servico = servico_dao.get_servico('08/01/2021', 2)
#print(_servico.get_modalidade())
#_servico = servico_dao.get_servico('08/01/2021', 3)
#print(_servico.get_modalidade())
#_servico = servico_dao.get_servico('09/01/2021', 1)
#print(_servico.get_modalidade())
#_servico = servico_dao.get_servico('09/01/2021', 2)
#print(_servico.get_modalidade())
#_servico = servico_dao.get_servico('09/01/2021', 3)
#print(_servico.get_modalidade())
#_servico = servico_dao.get_servico('10/01/2021', 1)
#print(_servico.get_modalidade())
#_servico = servico_dao.get_servico('10/01/2021', 2)
#print(_servico.get_modalidade())
#_servico = servico_dao.get_servico('10/01/2021', 3)
#print(_servico.get_modalidade())
#print(_servico.get_weekday())

#cpu_dao = cpudao.CpuDAO()
#cpus = cpu_dao.get_cpus()
#cabecalio = '{:^8} | {:^40} | {:^20} | {:^7} | {:^7} | {:^12}'.format('PG', 'NOME COMPLETO', 'NOME DE GUERRA', 'FUNCAO', 'CURSO', 'ANO BASE')

#print(cabecalio)
#print('-' * len(cabecalio))
#for cpu in cpus:
#    ano_base = cpu.ano_base if cpu.ano_base != None else '----'
#    cpu_format = '{c.pg:^8} | {c.nome_completo:<40} | {c.nome_de_guerra:<20} | {c.funcao:<7} | {c.curso:<7} | {0:^12}'.format(ano_base, c=cpu)
#    print(cpu_format)
#cpu_dao.cpu_add('1 TEN', 'MAIA DA SILVA', 'MAIA', 'op', 'CFO', 2013)
#cpu_dao.cpu_add('1 TEN', 'LUCAS DA SILVA', 'LUCAS', 'TM', 'CFO', 2013)
#cpu_dao.cpu_add('2 TEN', 'GONDIM DA SILVA', 'GONDIM', 'ADM', 'CHO', 2013)
#cpu_dao.cpu_add('2 TEN', 'ERNANE DA SILVA', 'ERNANE', 'op', 'ChO', 2013)
#cpu_dao.cpu_add('2 TEN', 'DIMITRI DA SILVA', 'DIMITRI', 'op', 'CFO', 2013)
#cpu_dao.cpu_add('2 TEN', 'CUNHA DA SILVA', 'CUNHA', 'op', 'CFO', 2013)
#cpu_dao.cpu_add('2 TEN', 'HELDER DA SILVA', 'HELDER', 'op', 'CFO', 2013)
#cpu_dao.cpu_add('2 TEN', 'JONAS DA SILVA', 'JONAS', 'ADM', 'ChO', 2013)
#cpu_dao.cpu_add('2 TEN', 'FERNANDA DA SILVA', 'FERNANDA', 'op', 'CFO', 2013)
#cpu_dao.cpu_add('2 TEN', 'RENAN DA SILVA', 'RENAN', 'op', 'CFO', 2013)
#cpu_dao.cpu_add('2 TEN', 'EVERTON DA SILVA', 'EVERTON', 'TM', 'CFO', 2013)
#cpu_dao.cpu_add('2 TEN', 'JEFFERSON DA SILVA', 'JEFFERSON', 'op', 'CFO', 2013)
#cpu_dao.cpu_add('2 TEN', 'MARCELO DA SILVA', 'MARCELO', 'ADM', 'CHO', 2013)

#cpu_dao.cpu_remove('novo cpu')
#cpu_dao.cpu_update('cpu5', pg='1 tEN', funcao='adm', nome_completo='NOVO CPU5 SILVA', ano_base='2005')
#cpu_dao.cpu_remove('NOVO CPU5')
#cpu_dao.cpu_remove('NOVO CPU7')
#cpu_dao.cpu_remove('NOVO CPU9')
#cpu_dao.cpu_remove('NOVO CPU3')
#_escalar = escalar.Escalar()

#data = datetime.datetime.strptime('01/02/2020', '%d/%m/%Y').date()
#while data < datetime.datetime.strptime('03/02/2020', '%d/%m/%Y').date():
#    for i in range(3):
#        servicodao.ServicoDAO().servico_add(data, i + 1, 'Madureira')
#    data += datetime.timedelta(days=1)



#_servico = servico.Servico('10/10/2020', 2, 'MADUREIRA', 'ASP GOULARD')


#impedimento_dao = impedimentodao.ImpedimentoDAO()
#impedimento_dao.impedimento_add('madureira', 'ferias', '27/02/2020', '29/02/2020', 'comentário madureira')
#impedimento_dao.impedimento_add('cunha', 'ferias', '04/02/2020', '04/08/2020', 'comentário cunha')
#impedimento_dao.impedimento_add('jefferson', 'ferias', '28/02/2020', '05/03/2020', 'comentário jefferson')
#impedimento_dao.impedimento_add('fernanda', 'ferias', '11/07/2020', '13/08/2020', 'comentário fernanda')
#impedimento_dao.impedimento_add('renan', 'ferias', '04/07/2020', '20/08/2020', 'comentário renan')
#impedimento_dao.impedimento_add('maia', 'LICENCAS/DISPENSAS REGULAMENTARES', '01/02/2020', '01/02/2020', 'comentário helder')

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
#feriado_dao.feriado_add('04/02/2020', 'Pré-Carnaval')
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
#ordenacao_por_militar_dao = ordenacaopormilitardao.OrdenacaoPorMilitarDAO()
#ordenacao_por_militar_dao.ordenacao_por_militar_add('cunha',1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 112)
#print(ordenacao_por_militar_dao.get_ordenacao_por_militar('rodrigo'))
#ordenacao = ordenacao_por_militar_dao.get_ordenacao_por_modalidade('qua_12')
#ordenacao_por_militar = ordenacao_por_militar_dao.get_ordenacao_por_militar('MAIA')
#ordenacoes = ordenacao_por_militar_dao.get_ordenacao_por_militar_all()
#for ordenacao in ordenacoes:
#    print(ordenacao)

#fila_seg_12 = filapormodalidade.FilaPorModalidade('seg_12')
#fila_seg_12.membro_add('MAIA')
#fila_seg_12.membro_add('jefferson')
#fila_seg_12.membro_add('RENAN')
#fila_seg_12.membro_add('MAIA')
#fila_seg_12.membro_add('DIMITRi')
#fila_seg_12.membro_add('RENAN')
#fila_seg_12.membro_add('fernanda')
#fila_seg_12.membro_add('RENAN')
#fila_seg_12.membro_add('MAIA')
#fila_seg_12.membro_add('helder')


#print(fila_seg_12)
#print(fila_seg_12.get_next_membro(1))
#print(fila_seg_12)
#print(fila_seg_12.get_next_membro(2))
#print(fila_seg_12)


#l = [
#    servico.Servico('10/10/2020', 2, 'RENAN'),
#    servico.Servico('10/10/2020', 1, 'MADUREIRA')
#]
#
#servico_c = servico.Servico('10/10/2020', 2, 'DIMITRI')
#print(servico_c)
#print(servico_c == l[0])
#print(servico_c in l)


escalarsemana.EscalarSemana().escalar_seg_a_dom(escalar_tm=True)