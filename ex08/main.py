# Peça para o usuário digitar a idade de uma pessoa e informe:

# Criança → menor que 12

# Adolescente → de 12 a 17

# Adulto → de 18 a 59

# Idoso → 60 ou mais


idade = int(input('Digite uma idade: '))

if idade <= 12:
    print(F"Criança")
elif idade <=17:
    print(F"Adolescente")
elif idade <=59:
    print(F"Adulto")
else:
    print(F"Idoso")
