

class A:
    def metodo(self):
        print('A')
        
        
class B(A):
    def metodo(self):
        super(B, self).metodo()
        print('B')
        
        
class C(B):
    def metodo(self):
        print('C')
        
         
a = A()
b = B()
c = C()

a.metodo()
b.metodo()
c.metodo()

