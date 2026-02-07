def soma_lista(args):
    soma = 0
    for n in args:
        soma += n
    return soma



soma_lista([1, 2, 3])      # 6
soma_lista([5, 10, -2])    # 13