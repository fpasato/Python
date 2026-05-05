

class Ponto:
    def __init__(self, x, y, z='string'):
        self.x = x
        self.y = y
        self.z = z
    
    
    def __str__(self):
        return f'({self.x}, {self.y})'
    
    def __repr__(self):
        # class_name = self.__class__.__name__
        class_name = type(self).__name__
        return f'{class_name}(x={self.x!r}, y={self.y!r}, z={self.z!r})'
    
p1 = Ponto(1, 2)
p2 = Ponto(3, 4)

print(p1)
print(f'{p2!r}')
