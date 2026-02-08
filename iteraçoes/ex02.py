# Dada uma lista de números inteiros e um inteiro positivo k, 
# percorra a lista e, para cada subsequência contígua de tamanho k,
# determine qual é o maior valor dentro dessa subsequência.

lista = [5,6,3,2,5,9,4,1,6,2,5,1]

k = 3
lista_maiores = []

for i in range(len(lista) - 2): 
    lista_maiores.append(max(lista[i:i+k:1]))
       
print(lista) # [5, 6, 3, 2, 5, 9, 4, 1, 6, 2, 5, 1]
print()
print(lista_maiores) # [6, 6, 5, 9, 9, 9, 6, 6, 6, 5]
    


