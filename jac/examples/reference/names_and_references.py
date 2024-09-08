class Animal:
    def __init__(self, animal_type):
        self.animal_type = animal_type


class Dog(Animal):
    def __init__(self, breed):
        super().__init__("Dog")
        self.breed = breed
        self.sound = ""
        self._post_init()

    def _post_init(self):
        self.sound = "woof woof"


dog1 = Dog(breed="Labrador")
print(dog1.animal_type, dog1.breed, dog1.sound)
