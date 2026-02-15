
"""
Parte 2 – Manipulação de Usuários (Comprehensions)

Objetivo:
Criar funções para manipular a lista de usuários utilizando
list comprehension, set comprehension e dict comprehension.

Funções:

1) usuarios_ativos(usuarios)
   - Retornar apenas usuários onde "ativo" seja True.
   - Usar list comprehension.

2) nomes_unicos(usuarios)
   - Retornar um set com todos os nomes únicos.
   - Usar set comprehension.

3) maiores_de_idade(usuarios)
   - Retornar os usuários com idade >= 18.
   - Usar list comprehension.

4) medias(usuarios)
   - Retornar um dicionário no formato:
        {nome: média_das_pontuações}
   - Usar dict comprehension.
   - Tratar corretamente usuários com lista de pontuações vazia.

Restrições:
- Não usar for tradicional com append.
- Não criar lista vazia antes.
- Priorizar expressões diretas.
"""

usuarios = [
    {"nome": "Ana", "idade": 22, "ativo": True, "pontuacoes": [10, 8, 9]},
    {"nome": "Carlos", "idade": 17, "ativo": False, "pontuacoes": []},
    {"nome": "Maria", "idade": 30, "ativo": True, "pontuacoes": [7, 9, 10]},
    # {"nome": "Maria", "idade": 30, "ativo": True, "pontuacoes": [5, 8, 6]},
]

# Retornar apenas usuários ativos
def usuarios_ativos(usuarios):
    active_users = [user for user in usuarios if user['ativo'] == True]
    return active_users

usuarios_ativos(usuarios) # retonra ficha de maria e ana


# Retornar nomes únicos
def nomes_unicos(usuarios):
    nomes = {user['nome'] for user in usuarios}
    return nomes

nomes_unicos(usuarios) #{'Carlos', 'Maria', 'Ana'}

from operator import itemgetter
b = set(map(itemgetter('nome'), usuarios))
b = {user['nome'] for user in usuarios}

# Retornar usuários maiores de idade
def maiores_de_idade(usuarios):
    maiores_idade = [users for users in usuarios if users['idade'] > 17]
    return maiores_idade

maiores_de_idade(usuarios)


# Calcular média de pontuação de cada usuário
def medias(usuarios):
    medias = {item['nome']:round(sum(item['pontuacoes'])/len(item['pontuacoes']), 2) for item in usuarios if item['pontuacoes']}
    return medias 

print(medias(usuarios)) #{'Ana': 9.0, 'Carlos': 5.5, 'Maria': 8.67}
#obs: caso nome se repetir o valor da media ira se atualizar
