# Exercício: Mini Sistema de Análise de Usuários
# Você vai criar um pequeno sistema que analisa 
# um conjunto de usuários e gera relatórios.

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
print(u) # {'nome': 'Ana', 'idade': 22, 'ativo': True, 'pontuacoes': [10, 8, 9], 'cidade': 'SP', 'premium': True}



usuarios = [
    {"nome": "Ana", "idade": 22, "ativo": True, "pontuacoes": [10, 8, 9]},
    {"nome": "Carlos", "idade": 17, "ativo": False, "pontuacoes": []},
    {"nome": "Maria", "idade": 30, "ativo": True, "pontuacoes": [7, 9, 10]},
    # {"nome": "Maria", "idade": 30, "ativo": True, "pontuacoes": [5, 8, 6]},
]



# 1️⃣ Retornar apenas usuários ativos
def usuarios_ativos(usuarios):
    active_users = [user for user in usuarios if user['ativo'] == True]
    return active_users
    
usuarios_ativos(usuarios) # retonra ficha de maria e ana




# 2️⃣ Retornar nomes únicos
def nomes_unicos(usuarios):
    nomes = {user['nome'] for user in usuarios}
    return nomes

nomes_unicos(usuarios) #{'Carlos', 'Maria', 'Ana'}


# 3️⃣ Retornar usuários maiores de idade
def maiores_de_idade(usuarios):
    maiores_idade = [users for users in usuarios if users['idade'] > 17]
    return maiores_idade

maiores_de_idade(usuarios)



# 4️⃣ Calcular média de pontuação de cada usuário
def medias(usuarios):
    medias = {item['nome']:round(sum(item['pontuacoes'])/len(item['pontuacoes']), 2) for item in usuarios if item['pontuacoes']}
    return medias 

print(medias(usuarios)) #{'Ana': 9.0, 'Carlos': 5.5, 'Maria': 8.67}
#obs: caso nome se repetir o valor da media ira se atualizar


