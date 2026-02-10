# Parent class
class Animal:
    def make_sound(self):
        print("The animal makes a sound")

# Child class
class Dog(Animal):
    def make_sound(self):
        print("The dog barks")

class Cat(Animal):
    def make_sound(self):
        print("The cat miumiu")

# Main code
a = Animal()
d = Dog()
c = Cat()

a.make_sound()   # calls Animal's method
d.make_sound()   # calls Dog's overridden method
c.make_sound()
