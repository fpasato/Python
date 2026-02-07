def conta_vogal(arg):
    vogais = 0
    for letra in arg:
        if letra in 'aeiou':
            vogais+=1
    return vogais



print(conta_vogal('asdasdsad'))