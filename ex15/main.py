# lista = [1, 2, 3, 4, 5, 6, 7, 8]
# lista_invertida = []

# for i in lista:
#     lista_invertida.insert(0,i)

# print(lista)
# print(lista_invertida)



lista = [1, 2, 3, 4]
# saída esperada: [4, 3, 2, 1]
lista_invertida = lista[::-1]
print(lista)
print(lista_invertida)



palavra = input('Digite uma palavra: ')
palavra_invertida = palavra[::-1]
print(palavra)
print(palavra_invertida)


p = input('Digite uma palavra: ')
print(f'A palavra {p} é um palindromo' if p == p[::-1] else f"A palavra {p} Não é um palindromo")
