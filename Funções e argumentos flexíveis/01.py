"""
Parte 1 – Criação de Usuário

Objetivo:
Criar a função:

    criar_usuario(nome, idade, ativo=True, *pontuacoes, **extras)

Regras:
- Utilizar corretamente *args (pontuacoes) e **kwargs (extras).
- As pontuações devem ser armazenadas como lista.
- Montar e retornar um dicionário no formato:

    {
        "nome": ...,
        "idade": ...,
        "ativo": ...,
        "pontuacoes": [...],
        ...extras
    }

- A função deve apenas criar e retornar o usuário.
- Não deve gerenciar lista global.
- Deve funcionar mesmo se nenhuma pontuação for passada.
"""


def criar_usuario(nome, idade, ativo=True, *pontuacoes, **extras):

    pontuacoes= list(pontuacoes)
    
    ficha = {}
    ficha['nome'] = nome
    ficha['idade'] = idade
    ficha['ativo'] = ativo
    ficha['pontuacoes'] = pontuacoes
    
    # ficha.update(extras)
    for chave, valor in extras.items():
        ficha[f'{chave}'] = valor
    
    return ficha

u = criar_usuario("Ana", 22, True, 10, 8, 9, cidade="SP", premium=True) 
# print(u) # {'nome': 'Ana', 'idade': 22, 'ativo': True, 'pontuacoes': [10, 8, 9], 'cidade': 'SP', 'premium': True}


usuarios = [
    {"nome": "Ana", "idade": 22, "ativo": True, "pontuacoes": [10, 8, 9]},
    {"nome": "Carlos", "idade": 17, "ativo": False, "pontuacoes": []},
    {"nome": "Maria", "idade": 30, "ativo": True, "pontuacoes": [7, 9, 10]},
    # {"nome": "Maria", "idade": 30, "ativo": True, "pontuacoes": [5, 8, 6]},
]

a = list(filter(lambda user: user['ativo'], usuarios))
b = set(map(lambda user: user['nome'], usuarios))
c = list(filter(lambda user: user['idade'] >= 18 , usuarios))
d = dict(map(
    lambda user:(user['nome'], round(sum(user['pontuacoes']) / len(user['pontuacoes']),  2) if user['pontuacoes'] else None), 
    usuarios))


