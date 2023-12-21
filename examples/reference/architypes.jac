# Superhero Archetype
"""Enum for superhero powers"""
enum Superpower {
        FLYING = "Flying",
        SUPER_STRENGTH = "Super Strength",
        TELEPORTATION = "Teleportation"
    }

obj Superhero {

    has name: str, power: Superpower;

    """Method to introduce the superhero"""
    can introduce() -> str {
        return f"I am {self.name}, a superhero with the power of {self.power.value}!";
    }
}

# Subclass representing a Superhero with a cape, Superhero is inherited to define superhero's Cape
obj SuperheroWithCape:Superhero: {

    has:protect cape_color: str;

    """Method to describe the superhero with a cape"""
    can describe_with_cape() -> str {
        return f"{self.introduce()} I have a stylish {self.cape_color} cape!";
    }
}

with entry {
    # Creating an instance of the Superhero architype
    hero = Superhero("Captain Marvel",Superpower.FLYING);

    # Introducing the superhero
    print(hero.introduce());

    # Creating an instance of the SuperheroWithCape subclass
    hero_with_cape = SuperheroWithCape("Batman", Superpower.TELEPORTATION, "Black");

    # Describing the superhero with a cape
    hero_with_cape.describe_with_cape() |> print;
}
