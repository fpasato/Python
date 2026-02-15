"""
Parte 3 – Manipulação com map, filter e lambda

Objetivo:
Refazer as operações da Parte 2 utilizando programação funcional
com map(), filter() e lambda, sem usar comprehensions.

Funções a implementar:

1) Usuários ativos
   - Usar filter() para retornar apenas usuários com "ativo" == True.
   - Converter o resultado para list.

2) Nomes únicos
   - Usar map() para extrair os nomes.
   - Converter o resultado para set.

3) Maiores de idade
   - Usar filter() para retornar usuários com idade >= 18.
   - Converter o resultado para list.

4) Médias
   - Usar map() para transformar cada usuário em uma tupla:
        (nome, média_das_pontuações)
   - Converter o resultado final para dict.
   - Tratar usuários com lista de pontuações vazia.

Regras:
- Não usar list/set/dict comprehension.
- Não usar loop tradicional (for/while).
- Entender que map e filter retornam iteradores (lazy),
  sendo necessário converter para list ou dict para visualizar.
- Usar lambda corretamente para transformação ou filtragem.
"""

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



# print(a) #[{'nome': 'Ana', 'idade': 22, 'ativo': True, 'pontuacoes': [10, 8, 9]}, {'nome': 'Maria', 'idade': 30, 'ativo': True, 'pontuacoes': [7, 9, 10]}]

# print(b)  #{'Carlos', 'Maria', 'Ana'}
# print(c) #[{'nome': 'Ana', 'idade': 22, 'ativo': True, 'pontuacoes': [10, 8, 9]}, {'nome': 'Maria', 'idade': 30, 'ativo': True, 'pontuacoes': [7, 9, 10]}]
# print(d)# {'Ana': 9.0, 'Carlos': None, 'Maria': 8.67}