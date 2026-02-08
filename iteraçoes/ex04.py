# Dada uma lista de números inteiros e um inteiro positivo k, percorra a lista e,
# para cada subsequência contígua de tamanho k (a partir da segunda), 
# determine se a soma dessa subsequência é maior, menor ou igual à soma da subsequência imediatamente anterior.
# Para cada comparação, armazene:
# 1 se a soma aumentou
# -1 se a soma diminuiu
# 0 se a soma permaneceu igual  

#                                            2   1    0      
lista = [5 , 6 , 3 , 2 , 5 , 9 , 4 , 1 , 6 , 2 , 5 ,  1 ]
#        0 , 1 , 2 , 3 , 4 , 5 , 6 , 7 , 8 , 9 , 10 , 11   


k = 3
lista_maior = []

janela_atual = sum(lista[:3])


for i in range(len(lista)- k): 
    soma = sum(lista[i+1:i+4])
    print(soma)
    
    if soma > janela_atual: # se aumentou
        lista_maior.append(1)
    elif soma < janela_atual: # se diminuiu
        lista_maior.append(-1)
    else:        # se manteve
        lista_maior.append(0)
        
    janela_atual = soma
    
print(lista)
print(lista_maior)
        
        
        
    
        

       
# print(lista) # [5, 6, 3, 2, 5, 9, 4, 1, 6, 2, 5, 1]
# print()
# print(lista_maior) # [1, 2, 1, 1, 1, 1, 2, 2, 2, 1]
    




