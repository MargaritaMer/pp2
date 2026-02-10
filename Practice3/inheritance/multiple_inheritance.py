# multiple_inheritance.py

class Flyer:
    def move(self):
        print("Flying in the sky")

class Swimmer:
    def move(self):
        print("Swimming in the water")

# Child class with multiple inheritance
class Duck(Flyer, Swimmer):
    def move(self):
        print("Duck can do both:")
        super().move()   # follows Method Resolution Order (MRO)

# Main
if __name__ == "__main__":
    d = Duck()
    d.move()

    print(Duck.__mro__)  # shows method resolution order
