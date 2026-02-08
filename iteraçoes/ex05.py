# Dada uma lista de números inteiros e um inteiro positivo k, percorra a lista usando janelas contíguas de tamanho k.
# Para cada nova janela (a partir da segunda):
# compare a soma da janela atual com a soma da janela anterior

# se a soma aumentar, considere isso como +1 ponto
# se a soma diminuir, considere −1 ponto
# se a soma permanecer igual, considere 0 ponto

# 👉 Ao final, determine qual foi o maior saldo acumulado de pontos em qualquer momento do percurso.

#                                            2   1    0      
lista = [5 , 6 , 3 , 2 , 5 , 9 , 4 , 1 , 6 , 2 , 5 ,  1 ]
#        0 , 1 , 2 , 3 , 4 , 5 , 6 , 7 , 8 , 9 , 10 , 11   
k = 3
lista_maior = []
saldo= 0 

janela_atual = sum(lista[:3])


for i in range(len(lista)- k): 
    soma = sum(lista[i+1:i+4])
    print(soma)
    
    if soma > janela_atual: # se aumentou
        saldo +=1
        lista_maior.append(saldo)
    elif soma < janela_atual: # se diminuiu
        saldo -=1
        lista_maior.append(saldo)
    else:        # se manteve
        saldo +=0
        lista_maior.append(saldo)
        
    janela_atual = soma

     
print(lista) # [5, 6, 3, 2, 5, 9, 4, 1, 6, 2, 5, 1]
print()
print(lista_maior) # [1, 2, 1, 1, 1, 1, 2, 2, 2, 1]
print()
print(max(lista_maior)) # 0

    




