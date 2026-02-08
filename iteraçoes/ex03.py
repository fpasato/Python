# Dada uma lista de números inteiros e um inteiro positivo k, 
# percorra a lista e, para cada subsequência contígua de tamanho k,
# determine qual é o maior valor dentro dessa subsequência.

lista = [5,6,3,2,5,9,4,1,6,2,5,1]

k = 3
lista_pares = []

for i in range(len(lista) - 2): 
    soma = 0
    for n in lista[i:i+k]:
        if n % 2 == 0:
            soma +=1
    lista_pares.append(soma)  
       
print(lista) # [5, 6, 3, 2, 5, 9, 4, 1, 6, 2, 5, 1]
print()
print(lista_pares) # [1, 2, 1, 1, 1, 1, 2, 2, 2, 1]
    




