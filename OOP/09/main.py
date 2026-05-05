

class Produto:
    def __init__(self, nome, preco):
      self.nome = nome
      self.preco = preco
      
      if not self.preco > 0:
          raise ValueError('O PREÇO DO PRODUTO NÃO PODE SER 0')
     
      
class ItemPedido:
    def __init__(self, produto, quantidade):
      self.produto = produto
      self.quantidade = quantidade
      
      if not self.quantidade > 0:
          raise ValueError('A QUANTIDADE NÃO PODE SER 0')
      
    def calcular_total_item(self):
        return self.produto.preco * self.quantidade
      
      
class Pedido:
    def __init__(self, status='Aberto'):
      self._itens = []
      self._status = status
      
    def adicionar_item(self, nome , preco, quantidade):
        
        if self._status == 'Finalizado':
            print('Este pedido já foi finalizado.')
            return
            
        produto = Produto(nome, preco)
        pedido = ItemPedido(produto, quantidade)
        self._itens.append(pedido)
        
    def remover_item(self, nome_produto):
        for item in self._itens:
            if item.produto.nome == nome_produto:
                self._itens.remove(item)
                break
        
    def calcular_total(self):
        return sum(produto.calcular_total_item() for produto in self._itens)
     
    def finalizar_pedido(self):
        self._status = 'Finalizado'         
    
    def mostrar_resumo(self):
        print('\nItens:\n')
        valor_total = self.calcular_total()
        for produto in self._itens:
            print(f'- {produto.produto.nome} x{produto.quantidade} = {produto.calcular_total_item()}')
        print()
        print(f'Total: {valor_total}')
        

pedido = Pedido()
pedido.adicionar_item("Teclado", 100, 2)
pedido.adicionar_item("Mouse", 50, 1)

pedido.remover_item('Teclado')
pedido.mostrar_resumo()

pedido.finalizar_pedido()

pedido.adicionar_item("Mouse", 50, 1)

# SAIDA:
# Itens:

# - Mouse x1 = 50

# Total: 50
# Este pedido já foi finalizado.