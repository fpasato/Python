from main import caminho_arquivo, Pessoa
import json

with open(caminho_arquivo, 'r', encoding='utf-8') as f:
    pessoas = json.load(f)
    
    for pessoa in pessoas:
         
    
