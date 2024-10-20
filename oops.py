class Animal():
  def __init__(self):
    self.name = "Lan"

class Cat(Animal):
  def __init__(self, name):
    super().__init__(name)
    print(self)

cat = Animal("Kitty")
print(cat.name)