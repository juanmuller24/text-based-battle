class Weapon:
    def __init__(self, name: str, weapon_type: str, damage: int, value: int) -> None:
        self.name = name
        self.weapon_type = weapon_type
        self.damage = damage
        self.value = value


iron_sword = Weapon("Iron Sword", "sharp", 5, 10)
short_bow = Weapon("Short Bow", "ranged", 4, 8)
fists = Weapon("Fists", "blunt", 2, 0)