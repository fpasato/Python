# Estrutura do CPF
# 11 dígitos: N1 N2 N3 . N4 N5 N6 . N7 N8 N9 - D1 D2
# N1 a N9: Nove primeiros dígitos.
# D1 (10º dígito): Primeiro dígito verificador.
# D2 (11º dígito): Segundo dígito verificador. 

def verifica_cpf(cpf):
    # verifica d1

    soma, indice_digito = 0, 0
    for n in range(10, 1, -1):
        print('n : ', n)
        print('indice digito: ', indice_digito)
        print('digito cpf: ',  cpf[indice_digito])
        print('soma: ', soma) 
        soma += int(cpf[indice_digito]) * n
        indice_digito +=1
    d1 = 0 if soma % 11 < 2 else 11 - (soma % 11)
    print(d1)
    print(soma)

    # verifica d2
    soma, indice_digito = 0, 0
    for n in range(11, 2, -1):
        print('n : ', n)
        print('indice digito: ', indice_digito)
        print('digito cpf: ',  cpf[indice_digito])
        print('soma: ', soma) 
        soma += int(cpf[indice_digito]) * n
        indice_digito +=1
    soma += d1 * 2
    
    d2 = 0 if soma % 11 < 2 else 11- (soma % 11)
    print(d2)
    print(soma)


    # 40027319016
    # 01234567890  ← índices

    print(cpf)
    print(f"O CPF {cpf[0:3]}.{cpf[3:6]}.{cpf[6:9]}-{d1}{d2}")


    if d1 == int(cpf[-2]) and d2 == int(cpf[-1]):
        print(f"O CPF {cpf[0:3]}.{cpf[3:6]}.{cpf[6:9]}-{d1}{d2} é VÁLIDO")
    else:
        print(f"O CPF {cpf[0:3]}.{cpf[3:6]}.{cpf[6:9]}-{d1}{d2} é INVÁLIDO")
        

cpf = input('Digite o CPF sem pontos ou traços (ex.: 12345678900): ').strip()

verifica_cpf(cpf)



