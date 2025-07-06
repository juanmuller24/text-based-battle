import random
from weapon import fists
from health_bar import HealthBar

class Character:
    def __init__(self, name: str, health: int, level: int = 1) -> None:
        self.name = name
        self.health = health
        self.health_max = health
        self.level = level
        self.weapon = fists
        self.experience = 0
        self.experience_to_next_level = 100
        self.gold = 0
        self.is_alive = True
        self.health_bar = None  # Will be set by subclasses
        
    def attack(self, target) -> None:
        if not self.is_alive or not target.is_alive:
            return
            
        damage, is_crit = self.weapon.calculate_damage()
        
        # Add level-based damage bonus
        damage += self.level // 2
        
        target.take_damage(damage)
        
        crit_text = " (CRITICAL HIT!)" if is_crit else ""
        print(f"{self.name} dealt {damage} damage to {target.name} with {self.weapon.name}{crit_text}")
        
        if not target.is_alive:
            print(f"{target.name} has been defeated!")
            self.gain_experience(target.level * 25)
            self.gold += target.level * 5
    
    def take_damage(self, damage: int) -> None:
        """Take damage and update health status"""
        self.health -= damage
        if self.health <= 0:
            self.health = 0
            self.is_alive = False
        if self.health_bar:
            self.health_bar.update()
    
    def heal(self, amount: int) -> None:
        """Heal the character"""
        if not self.is_alive:
            return
        self.health = min(self.health + amount, self.health_max)
        if self.health_bar:
            self.health_bar.update()
        print(f"{self.name} healed for {amount} HP!")
    
    def gain_experience(self, exp: int) -> None:
        """Gain experience and level up if enough"""
        self.experience += exp
        print(f"{self.name} gained {exp} experience!")
        
        while self.experience >= self.experience_to_next_level:
            self.level_up()
    
    def level_up(self) -> None:
        """Level up the character"""
        self.experience -= self.experience_to_next_level
        self.level += 1
        self.experience_to_next_level = int(self.experience_to_next_level * 1.5)
        
        # Increase max health
        health_increase = random.randint(5, 15)
        self.health_max += health_increase
        self.health += health_increase  # Also heal on level up
        
        print(f"🎉 {self.name} reached level {self.level}! Max HP increased by {health_increase}!")
        if self.health_bar:
            self.health_bar.update()

class Hero(Character):
    def __init__(self, name: str, health: int, level: int = 1) -> None:
        super().__init__(name, health, level)
        self.default_weapon = self.weapon
        self.health_bar = HealthBar(self, color="green")
        self.inventory = []
        self.potions = 3
        self.gold = 50

    def equip(self, weapon) -> None:
        """Equip a weapon"""
        old_weapon = self.weapon
        self.weapon = weapon
        print(f"{self.name} equipped {self.weapon.name}.")
        if old_weapon != self.default_weapon:
            self.inventory.append(old_weapon)
        
    def drop(self) -> None:
        """Drop current weapon and equip default"""
        if self.weapon != self.default_weapon:
            self.inventory.append(self.weapon)
        self.weapon = self.default_weapon
        print(f"{self.name} dropped the weapon and equipped {self.weapon.name}.")
    
    def use_potion(self) -> bool:
        """Use a healing potion"""
        if self.potions > 0 and self.health < self.health_max:
            self.potions -= 1
            heal_amount = random.randint(20, 40)
            self.heal(heal_amount)
            print(f"{self.name} used a potion! ({self.potions} potions remaining)")
            return True
        elif self.potions == 0:
            print(f"{self.name} has no potions left!")
        else:
            print(f"{self.name} is already at full health!")
        return False
    
    def show_stats(self) -> None:
        """Display character stats"""
        print(f"\n--- {self.name}'s Stats ---")
        print(f"Level: {self.level}")
        print(f"Health: {self.health}/{self.health_max}")
        print(f"Weapon: {self.weapon}")
        print(f"Experience: {self.experience}/{self.experience_to_next_level}")
        print(f"Gold: {self.gold}")
        print(f"Potions: {self.potions}")
        
class Enemy(Character):
    def __init__(self, name: str, health: int, weapon, level: int = 1, enemy_type: str = "normal") -> None:
        super().__init__(name, health, level)
        self.weapon = weapon
        self.health_bar = HealthBar(self, color="red")
        self.enemy_type = enemy_type
        self.gold = level * random.randint(3, 8)
        
        # Adjust stats based on enemy type
        if enemy_type == "elite":
            self.health_max = int(self.health_max * 1.5)
            self.health = self.health_max
            self.gold *= 2
        elif enemy_type == "boss":
            self.health_max = int(self.health_max * 2.5)
            self.health = self.health_max
            self.gold *= 3
    
    def ai_action(self, target) -> None:
        """Simple AI for enemy actions"""
        if not self.is_alive:
            return
            
        # Simple AI: attack most of the time, occasionally "defend" (skip turn)
        if random.random() < 0.1:  # 10% chance to skip turn
            print(f"{self.name} is preparing for the next attack...")
        else:
            self.attack(target)
