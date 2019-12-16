from enum import Enum

class FuncaoEnum(Enum):
    ADM = 'ADM'
    OP = 'OP'
    TM = 'TM'


class PgEnum(Enum):
    TEN2 = '2 TEN'
    TEN1 = '1 TEN'
    SUB_TEN = 'SUB TEN'
    SGT1 = '1 SGT'
    SGT2 = '2 SGT'


class TipoImpedimentoEnum(Enum):
    FERIAS = 'FERIAS'
    LICENCAS_DISPENSAS = 'LICENCAS/DISPENSAS REGULAMENTARES'
    DISPENSA_DE_SERVICO = 'DISPENSA DE SERVICO'
    TRANSITO = 'TRANSITO'

class CursoEnum(Enum):
    CFO = 'CFO'
    CHO = 'CHO'