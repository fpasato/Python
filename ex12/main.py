# Dada uma lista de números inteiros, percorra a lista e conte:

# quantos números são pares

# quantos números são ímpares

# No final, imprima os dois valores.

# Regras
# Use for
# Use o operador %
# Não use listas auxiliares

numeros = [1, 2, 3, 4, 5, 6]
pares = 0
impares = 0

for numero in numeros:
    if numero % 2 == 0:
        pares += 1
    else:
        impares +=1

print(numeros)
print(f'Pares: {pares}\nImpares: {impares}')