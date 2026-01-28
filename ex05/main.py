# Peça para o usuário digitar três notas (podem ser decimais).
# Calcule a média aritmética e informe a situação do aluno:
# Aprovado → média ≥ 7
# Recuperação → média ≥ 5 e < 7
# Reprovado → média < 5

print('Calcula Média'.center(30, '='))
n1 = float(input('Digite a Nota 1: '))
print('-' *30)
n2 = float(input('Digite a Nota 2: '))
print('-' *30)
n3 = float(input('Digite a Nota 3: '))
print('-' *30)

media = (n1 + n2 + n3) / 3

print(f'média geral: {media:.2f}')

if media <5:
    print('Reprovado')
elif media < 7:
    print('Recuperação')
else: 
    print('Aprovado')