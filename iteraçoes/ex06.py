# Dada uma lista de números inteiros, percorra a lista a partir do segundo elemento e compare cada número com o anterior.
# Para cada comparação:
# se o número aumentar em relação ao anterior → considere +1 ponto
# se diminuir → considere −1 ponto
# se permanecer igual → considere 0 ponto
# 👉 Ao longo do percurso, mantenha um saldo acumulado desses pontos.
# 👉 Ao final, determine qual foi o maior saldo acumulado atingido em qualquer momento.
# 🧩 Observações importantes
# Não existe janela
# Não existe 
# Cada elemento só olha para o anterior direto
# O primeiro número não entra na comparação

#                                            2   1    0      
lista = [5 , 6 , 3 , 2 , 5 , 9 , 4 , 1 , 6 , 2 , 5 ,  1 ]
#        0 , 1 , 2 , 3 , 4 , 5 , 6 , 7 , 8 , 9 , 10 , 11   
lista_maior = []
saldo= 0 

for i in range(len(lista) - 1): 
    proximo_i = i+1
    
    print(f'Valor comparados {lista[i]} {lista[i+1]}')
    
    if lista[i] < lista[proximo_i]:
        print(f'{lista[i]} < {lista[proximo_i]} aumentou')
        # se aumentou
        saldo +=1
        print(f'saldo : {saldo}')
        
    elif lista[i] > lista[proximo_i]: # se diminuiu
        print(f'{lista[i]} > {lista[proximo_i]} diminuiu')
        saldo -=1
        print(f'saldo : {saldo}')
        
    else:        # se manteve
        print(f'{lista[i]} == {lista[proximo_i]} igual ')
        saldo +=0
        print(f'saldo : {saldo}')
        
    
    lista_maior.append(saldo)
    print(f'lista final: {lista_maior}')     
print(lista) # [5, 6, 3, 2, 5, 9, 4, 1, 6, 2, 5, 1]
print()
print(lista_maior) # [1, 2, 1, 1, 1, 1, 2, 2, 2, 1]
print()
print(max(lista_maior)) # 1

    




