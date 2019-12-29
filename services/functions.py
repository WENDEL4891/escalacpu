from datetime import datetime

def invertFormatDateStr(strDate):
    if not isinstance(strDate, str):
        raise TypeError('A data deve ser informada no formato "hifens": AAAA-mm-dd; ou "barras": dd/mm/AAAA. ')

    formatBarras = True
    formatHifens = True

    try:
        datetime.strptime(strDate, '%d/%m/%Y')
    except ValueError:
        formatBarras = False

    try:
        datetime.strptime(strDate, '%Y-%m-%d')
    except ValueError:
        formatHifens = False

    if formatBarras:
        dia = strDate[:2]
        mes = strDate[3:5]
        ano = strDate[6:]
        return ano + '-' + mes + '-' + dia
    
    if formatHifens:
        ano = strDate[:4]
        mes = strDate[5:7]
        dia = strDate[8:10]
        return dia + '/' + mes + '/' + ano
    
    raise ValueError("A data informada não está em formato de 'barras', nem de 'hifens'. ")


def date_str_to_datetime(data_str):
        try:
            data = datetime.strptime(data_str, '%d/%m/%Y').date()
        except:
            pass
        else:
            return data
        try:
            data = datetime.strptime(data_str, '%Y-%m-%d').date()
        except:
            raise ValueError('A data deve estar em um dos formatos:\ndd/mm/AAAA\nAAAA-mm-dd')
        return data

def get_value_from_key_in_dict(_dict, value_parameter):
    for key, value in _dict.items():
        if value == value_parameter:
            return key

#def classifica_servico_por_modalidade(data, turno):
#    if turno not in (1, 2, 3, '1', '2', '3'):
#        raise ValueError('O parâmetro turno só aceita os argumentos 1, 2 ou 3.')
#    turno = int(turno)
#    dias_da_semana = ['segunda', 'terca', 'quarta', 'quinta', 'sexta', 'sabado', 'domingo']
#    try:
#        dia_da_semana = dias_da_semana[data.weekday()]
#    except:
#        try:
#            data_in_datetime = date_str_to_datetime(data)
#            dia_da_semana = dias_da_semana[data_in_datetime.weekday()]
#        except:
#            raise ValueError('O parâmetro data recebe uma data válida, em datetime ou em string, em algum dos formatos: dd/mm/AAAA; AAAA-mm-dd.')
#    
#    
#    if dia_da_semana == 'segunda' and turno in (1, 2):
#        return 'seg_12'
#    if dia_da_semana == 'segunda' and turno == 3:
#        return 'seg_3'
#    if dia_da_semana in ('terca', 'quinta', 'sexta') and turno in (1, 2):
#        return 'ter_qui_sex_12'
#    if dia_da_semana == 'quarta' and turno in (1, 2):
#        return 'qua_12'
#    if dia_da_semana == 'terca' and turno == 3:
#        return 'ter_3'
#    if dia_da_semana == 'quarta' and turno == 3:
#        return 'qua_3'
#    if dia_da_semana == 'quinta' and turno == 3:
#        return 'qui_3'
#    if dia_da_semana == 'sexta' and turno == 3:
#        return 'sex_3'
#    if dia_da_semana in ('sabado', 'domingo') and turno in (1, 2):
#        return 'fds_12'
#    if dia_da_semana == 'sabado' and turno == 3:
#        return 'sab_3'
#    if dia_da_semana == 'domingo' and turno == 3:
#        return 'dom_3'
