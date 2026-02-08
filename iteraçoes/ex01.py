# Pensa numa janelinha que pega k números seguidos da lista.
# Essa janela:

# soma esses k números

# anda 1 posição pra frente

# soma de novo

# repete até não dar mais

# Ela desliza pela lista, por isso o nome.

# 📦 Exemplo bem concreto

# Lista:

# [2, 4, 1, 3, 5]


# k = 3 (tamanho da janela)

# Passo a passo:

# 1️⃣ Primeira janela → pega os 3 primeiros:

# [2, 4, 1]
# soma = 7


# 2️⃣ Desliza 1 posição pra direita:

# [4, 1, 3]
# soma = 8


# 3️⃣ Desliza de novo:

# [1, 3, 5]
# soma = 9


# Acabou, porque não dá mais pra pegar 3 números seguidos.

# ✅ Resultado esperado

# Você deve mostrar:

# 7
# 8
# 9


# (ou guardar isso numa lista)


lista = [5,6,3,2,5,9,4,1,6,2,5,1]

k = 3
lista_soma = []

for i in range(len(lista) - 2): # o loop vai de 0 a len(lista) - 2
    soma = 0 
    for n in lista[i:i+k:1]: # para cada numero no range de i a i+k
        soma += n
    lista_soma.append(soma)
       
print(lista) # [5, 6, 3, 2, 5, 9, 4, 1, 6, 2, 5, 1]
print()
print(lista_soma) # [14, 11, 10, 16, 18, 14, 11, 9, 13, 8]
    


