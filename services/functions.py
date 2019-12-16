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