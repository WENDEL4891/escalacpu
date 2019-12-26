class FilaPorModalidade:
    def __init__(self, modalidade):
        self.modalidade = modalidade
        self.fila = dict()
    
    def membro_add(self, ordem, nome_de_guerra):
        self.fila[ordem] = nome_de_guerra
    
    def __str__(self):
        self.fila = dict(sorted(self.fila.items()))
        aux = 'Fila = {} '.format(self.modalidade) + '{\n'
        for ordem, militar in self.fila.items():
            aux += '\t{}: {}\n'.format(ordem, militar)
        aux += '}'
        return aux

fila_seg_12 = FilaPorModalidade('seg_12')
fila_seg_12.membro_add(5, 'MAIA')
fila_seg_12.membro_add(4, 'jefferson')
fila_seg_12.membro_add(2, 'RENAN')
fila_seg_12.membro_add(6, 'DIMITRI')

print(fila_seg_12)