import json

class Pessoa:
    def __init__(self, nome, idade):
        self.nome = nome
        self.idade = idade
        
caminho_arquivo = "pessoas.json"

p1 = Pessoa('Fer', 22)
p2 = Pessoa('maria', 25)
p3 = Pessoa('João', 28)

bd = [vars(p1), vars(p2), vars(p3)]

with open(caminho_arquivo, 'w', encoding='utf-8') as f:
    json.dump(bd, f, ensure_ascii= False, indent= 2)
    