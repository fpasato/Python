n1 = input('Digite qualquer valor: ')

try:
    try:
        n1 = int(n1)
    except:
        n1 = float(n1)
except:
    pass
finally:
    print(f'o valor digitado é: {type(n1)}')
    