import sys, getopt
from db import Connection
from dbDAO import ServicoDAO, FeriadoDAO
import config
from services import Escalar

def main(argv):

    escalar = Escalar()
    print(escalar.getDiasETurnosParaEscalar())
    
    escalar = Escalar()
    escalar.escalarSeg_Sex()

    try:
        opts, remains = getopt.gnu_getopt(argv,"ha:b:c:d",["saldos","cpus"])
    except getopt.GetoptError:
        print('Opções válidas:\n-h\t\tpara ver as opções válidas\n-a\t\tpara a\n-b\t\tpara b\n-c\t\tpara c\n-d\t\tpara d')
        print('--saldos\tpara saldos de serviços\n--cpus\t\tpara Tenentes cadastrados')
        sys.exit(2)
    for opt, arg in opts:        
        if opt == '-h':
            print('Opções válidas:\n-h\t\tpara ver as opções válidas\n-a\t\tpara a\n-b\t\tpara b\n-c\t\tpara c\n-d\t\tpara d')
            print('--saldos\tpara saldos de serviços\n--cpus\t\tpara Tenentes cadastrados')
            sys.exit()
        if opt == '-a':
            print('Executar opção ' + opt)
        if opt == '-b':
            print('Executar opção ' + opt)
        if opt == '-c':
            print('Executar opção ' + opt)
        if opt == '-d':
            print('Executar opção ' + opt)
        if opt == '--saldos':
            print('Exibir saldos de serviços.')
        if opt == '--cpus':
            print('Exibir Tenentes Cadastrados')

    print('-------------\nArgumentos não utilizados: ' + str(remains))


if __name__ == "__main__":
   main(sys.argv[1:])