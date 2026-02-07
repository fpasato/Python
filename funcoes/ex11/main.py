# Crie uma lista de números inteiros.
# Percorra essa lista e calcule a soma de todos os elementos.

# Regras
# Use for
# Não use a função sum()
# Imprima o resultado final

numeros = [8, 1, 2, 3, 4, 5, 6, 7, 8, 9]
contador = 0

for n in numeros:
    contador +=n

print(f'Soma total: {contador}')