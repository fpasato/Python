def conta_pares(args):
    pares = 0
    for n in args:
        if n % 2 == 0:
            pares +=1
    return pares




print(conta_pares([1, 2, 3, 4, 6]))  # 3