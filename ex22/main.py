lista = [6, 2, 5, 9, 7, 4]

def soma_pares(array):
    contador = 0
    for n in array:
        contador += 1 if n % 2 == 0 else 0
    return contador

print(soma_pares(lista))
