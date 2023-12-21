from enum import Enum


# Enum for superhero powers
class Superpower(Enum):
    FLYING = "Flying"
    SUPER_STRENGTH = "Super Strength"
    TELEPORTATION = "Teleportation"


# Superhero Class
class Superhero:
    def __init__(self, name: str, power: Superpower):
        self.name = name
        self.power = power

    def introduce(self) -> str:
        return f"I am {self.name}, a superhero with the power of {self.power.value}!"


# Subclass representing a Superhero with a cape
class SuperheroWithCape(Superhero):
    def __init__(self, name: str, power: Superpower, cape_color: str):
        super().__init__(name, power)
        self.cape_color = cape_color

    def describe_with_cape(self) -> str:
        return f"{self.introduce()} I have a stylish {self.cape_color} cape!"


# Creating an instance of the Superhero class
hero = Superhero("Captain Marvel", Superpower.FLYING)

# Introducing the superhero
print(hero.introduce())

# Creating an instance of the SuperheroWithCape subclass
hero_with_cape = SuperheroWithCape(
    name="Batman", power=Superpower.TELEPORTATION, cape_color="Black"
)

# Describing the superhero with a cape
print(hero_with_cape.describe_with_cape())
