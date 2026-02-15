
"""
Parte 4 – Recursão

Objetivo:
Criar uma função recursiva que receba uma lista de usuários
e retorne a soma total de todas as pontuações de todos os usuários.

Regras:
- Não usar for ou while.
- Não usar comprehension.
- A função deve usar recursão para percorrer a lista de usuários.
- Caso base: quando a lista estiver vazia, retornar 0.
- Passo recursivo: somar as pontuações do primeiro usuário
  com o resultado da chamada recursiva para o restante da lista.

Desafio extra (opcional):
Implementar também a soma das pontuações de cada usuário
de forma recursiva, sem usar sum().
"""

usuarios = [
    {"nome": "Ana", "idade": 22, "ativo": True, "pontuacoes": [10, 8, 9]},
    {"nome": "Carlos", "idade": 17, "ativo": False, "pontuacoes": []},
    {"nome": "Maria", "idade": 30, "ativo": True, "pontuacoes": [7, 9, 10]},

]


def soma_pontuacoes(usuarios):
    if not usuarios:
        return 0
    soma_atual = sum(usuarios[0]['pontuacoes'])
    return soma_atual + soma_pontuacoes(usuarios[1:])
    
print(soma_pontuacoes(usuarios))