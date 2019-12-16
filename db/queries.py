getNext = '''
    SELECT nome FROM ? WHERE ordem != 0 AND ordem = (MIN(ordem))
'''