    def find_duplication(codigo, log=None):
        duplicada = []
        d = defaultdict(list)
        for i,item in enumerate(codigo):
            d[item].append(i)

        for k,v in d.items():
            if len(v)>1:
                duplicada.extend(v)

        dupla = [v for k,v in d.items() if len(v)>1]
        if log:
            print('Genetic::find_duplication\t Existe duplicação')
            print(duplicada)
        return duplicada, dupla