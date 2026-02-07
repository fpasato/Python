# Exercício 14 – Separar positivos e negativos
# Enunciado

# Dada uma lista de números, crie:
# uma lista apenas com números positivos
# uma lista apenas com números negativos
# Ignore o valor 0.

# Regras
# Use for
# Use listas
# Não use list comprehension (por enquanto)
numeros = [-5, 3, -2, 0, 7, -1]

positivos = []
negativos = []

for numero in numeros:
    if numero > 0:
        positivos.append(numero)
    elif numero < 0:
        negativos.append(numero)

print(f'Positivos: {positivos}')
print(f'Negativos: {negativos}')