import random

class Weapon:
    def __init__(self, name: str, weapon_type: str, damage: int, value: int, 
                 crit_chance: float = 0.1, description: str = "") -> None:
        self.name = name
        self.weapon_type = weapon_type
        self.damage = damage
        self.value = value
        self.crit_chance = crit_chance
        self.description = description

    def calculate_damage(self) -> tuple[int, bool]:
        """Calculate damage with critical hit chance"""
        is_crit = random.random() < self.crit_chance
        damage = self.damage * 2 if is_crit else self.damage
        return damage, is_crit

    def __str__(self) -> str:
        return f"{self.name} ({self.weapon_type}) - {self.damage} damage"


# Weapon instances
iron_sword = Weapon("Iron Sword", "sharp", 5, 10, 0.15, "A sturdy blade forged from iron")
short_bow = Weapon("Short Bow", "ranged", 4, 8, 0.2, "A lightweight bow for quick shots")
fists = Weapon("Fists", "blunt", 2, 0, 0.05, "Your bare hands")
steel_sword = Weapon("Steel Sword", "sharp", 8, 25, 0.12, "A superior blade made of steel")
magic_staff = Weapon("Magic Staff", "magic", 6, 15, 0.25, "A staff imbued with magical energy")
war_hammer = Weapon("War Hammer", "blunt", 7, 20, 0.08, "A heavy hammer that crushes enemies")
crossbow = Weapon("Crossbow", "ranged", 9, 30, 0.18, "A powerful mechanical bow")
dagger = Weapon("Dagger", "sharp", 3, 5, 0.3, "A quick and agile blade")