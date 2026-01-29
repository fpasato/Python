lista = [3, -1, 0, 7, -2] 
# lista_palavras = ['bola', 'mesa', 'escada', 'copo', 'folha'] 

# def soma_impares(array):
#     contador = 0
#     return (contador + 1 for n in array if n % 2 != 0)
# print(soma_impares(lista))
# #3

# def soma_positivos(array):
#     return sum(n for n in array if n > 0)
# print(soma_positivos(lista))
# #10

def maior(array):
    return (n for n in array if n > n)
print(maior(lista))
#7


# def conta_letras(array):
#     return sum(1 for p in array if len(p) > 4 )
# print(conta_letras(lista_palavras))
# #


def conta_zero(array):
    contador = 0
    for n in array:
        if n == 0:
            contador +=1
    return contador
    

