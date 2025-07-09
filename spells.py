import random

class Spell:
    def __init__(self, name: str, damage: int, mana_cost: int, spell_type: str, description: str = ""):
        self.name = name
        self.damage = damage
        self.mana_cost = mana_cost
        self.spell_type = spell_type  # "damage", "heal", "buff", "debuff"
        self.description = description

    def cast(self, caster, target=None):
        """Cast the spell and return success status"""
        if caster.mana < self.mana_cost:
            print(f"{caster.name} doesn't have enough mana to cast {self.name}!")
            return False
        
        caster.mana -= self.mana_cost
        
        if self.spell_type == "damage" and target:
            damage = self.damage + random.randint(-2, 2)  # Slight variance
            target.take_damage(damage)
            print(f"{caster.name} casts {self.name} dealing {damage} magic damage to {target.name}!")
        
        elif self.spell_type == "heal":
            heal_amount = self.damage + random.randint(-5, 5)
            caster.heal(heal_amount)
            print(f"{caster.name} casts {self.name} and heals for {heal_amount} HP!")
        
        elif self.spell_type == "buff":
            # Apply temporary buff (simplified)
            print(f"{caster.name} casts {self.name} and feels empowered!")
            return {"type": "buff", "duration": 3, "effect": "damage_boost"}
        
        return True

# Spell instances
fireball = Spell("Fireball", 8, 15, "damage", "A blazing ball of fire")
heal = Spell("Heal", 25, 20, "heal", "Restores health with divine magic")
lightning_bolt = Spell("Lightning Bolt", 12, 25, "damage", "A devastating bolt of electricity")
minor_heal = Spell("Minor Heal", 15, 10, "heal", "A small healing spell")
frost_lance = Spell("Frost Lance", 10, 18, "damage", "A piercing shard of ice")
divine_blessing = Spell("Divine Blessing", 0, 30, "buff", "Temporarily increases combat effectiveness")
