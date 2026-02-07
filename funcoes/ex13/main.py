
nomes = []

for i in range(5):
    nome = input('Digite um nome: ')
    nomes.append(nome)

print(f'Lista Original: {nomes}')
print(f'Lista Ordenada: {sorted(nomes)}')


# Lista Original: ['Ana', 'Carlos', 'Bruno', 'Diana', 'Eduardo']
# Lista Ordenada: ['Ana', 'Bruno', 'Carlos', 'Diana', 'Eduardo']
