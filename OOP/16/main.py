
# ex:
# with open('file.txt', 'w') as file:
#     ...



class MyOpen:
    def __init__(self, caminho_arquivo ,modo):
        print('INIT')
        self.caminho_arquivo = caminho_arquivo
        self.modo = modo
        self._arquivo = None
    
    def __enter__(self):
        print('ABRINDO ARQUIVO')
        self._arquivo = open(self.caminho_arquivo, self.modo, encoding='utf8')
        return self._arquivo
    
    def __exit__(self, class_exception, exception_, traceback_exception_):
        print('FECHANDO ARQUIVO')
        self._arquivo.close()




with MyOpen('arquivo.txt', 'w') as arquivo:
    arquivo.write('Linha 1\n')
    arquivo.write('Linha 2\n')
    arquivo.write('Linha 3\n')
    print('WITH', arquivo)
