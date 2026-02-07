contador = 0
while True:
    n = float(input('Digite qualquer valor para somar: (Digite 0 Para Encerrar) '))
    if n == 0:
        break
    contador +=n

print(f'A Soma Total foi: {contador}')