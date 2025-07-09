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
        self.mana = 50 + (level * 10)  # Base mana + level bonus
        self.mana_max = self.mana
        self.spells = []
        self.buffs = []  # Active buffs/debuffs
        self.skills = {
            "strength": 10 + level,
            "agility": 10 + level,
            "intelligence": 10 + level,
            "luck": 10 + level
        }
        
    def attack(self, target) -> None:
        if not self.is_alive or not target.is_alive:
            return
            
        damage, is_crit = self.weapon.calculate_damage()
        
        # Add level-based damage bonus and strength bonus
        damage += self.level // 2
        damage += self.skills["strength"] // 5
        
        # Apply class-specific combat bonuses
        if hasattr(self, 'character_class'):
            from character_classes import apply_class_combat_bonuses
            damage = apply_class_combat_bonuses(self, damage)
        
        # Apply buffs
        for buff in self.buffs:
            if buff.get("effect") == "damage_boost":
                damage = int(damage * 1.3)
                break
        
        target.take_damage(damage)
        
        crit_text = " (CRITICAL HIT!)" if is_crit else ""
        print(f"{self.name} dealt {damage} damage to {target.name} with {self.weapon.name}{crit_text}")
        
        if not target.is_alive:
            print(f"{target.name} has been defeated!")
            self.gain_experience(target.level * 25)
            self.gold += target.level * 5
    
    def cast_spell(self, spell, target=None):
        """Cast a spell if the character knows it"""
        if spell not in self.spells:
            print(f"{self.name} doesn't know the spell {spell.name}!")
            return False
        
        # Apply class-specific mana efficiency
        mana_cost = spell.mana_cost
        if hasattr(self, 'character_class'):
            from character_classes import get_class_mana_bonus
            mana_cost = int(mana_cost * get_class_mana_bonus(self.character_class))
        
        if self.mana < mana_cost:
            print(f"{self.name} doesn't have enough mana to cast {spell.name}!")
            return False
        
        # Temporarily adjust spell mana cost for casting
        original_cost = spell.mana_cost
        spell.mana_cost = mana_cost
        result = spell.cast(self, target)
        spell.mana_cost = original_cost  # Restore original cost
        
        return result
    
    def learn_spell(self, spell):
        """Learn a new spell"""
        if spell not in self.spells:
            self.spells.append(spell)
            print(f"{self.name} learned {spell.name}!")
        else:
            print(f"{self.name} already knows {spell.name}!")
    
    def regenerate_mana(self, amount: int = 0):
        """Regenerate mana over time or by amount"""
        if amount == 0:
            amount = self.mana_max // 10  # 10% of max mana
        
        self.mana = min(self.mana + amount, self.mana_max)
    
    def update_buffs(self):
        """Update buff durations and remove expired ones"""
        self.buffs = [buff for buff in self.buffs if buff.get("duration", 0) > 0]
        for buff in self.buffs:
            buff["duration"] -= 1
    
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
        
        # Increase max health and mana
        health_increase = random.randint(5, 15)
        mana_increase = random.randint(3, 10)
        self.health_max += health_increase
        self.health += health_increase  # Also heal on level up
        self.mana_max += mana_increase
        self.mana += mana_increase  # Also restore mana on level up
        
        # Increase skills
        for skill in self.skills:
            self.skills[skill] += random.randint(1, 3)
        
        # Apply class-specific level bonuses
        if hasattr(self, 'character_class'):
            from character_classes import get_class_level_bonuses
            class_bonuses = get_class_level_bonuses(self.character_class, self.level)
            for skill, bonus in class_bonuses.items():
                self.skills[skill] += bonus
                if class_bonuses:
                    print(f"Class bonus: +{bonus} {skill.capitalize()}!")
        
        print(f"🎉 {self.name} reached level {self.level}!")
        print(f"Max HP increased by {health_increase}! Max Mana increased by {mana_increase}!")
        print("All skills improved!")
        
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
        self.skill_points = 0
        
        # Achievement tracking
        self.battles_won = 0
        self.battles_fought = 0
        self.elite_kills = 0
        self.boss_kills = 0
        self.spells_cast = 0
        
        # Learn basic spells (will be overridden by class)
        # from spells import minor_heal
        # self.learn_spell(minor_heal)

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
        if hasattr(self, 'character_class'):
            print(f"Class: {self.character_class.name}")
        print(f"Level: {self.level}")
        print(f"Health: {self.health}/{self.health_max}")
        print(f"Mana: {self.mana}/{self.mana_max}")
        print(f"Weapon: {self.weapon}")
        print(f"Experience: {self.experience}/{self.experience_to_next_level}")
        print(f"Gold: {self.gold}")
        print(f"Potions: {self.potions}")
        print(f"Skill Points: {self.skill_points}")
        print("\nSkills:")
        for skill, value in self.skills.items():
            print(f"  {skill.capitalize()}: {value}")
        
        if self.spells:
            print("\nSpells:")
            for spell in self.spells:
                print(f"  {spell.name} (Cost: {spell.mana_cost} mana) - {spell.description}")
        
        if hasattr(self, 'character_class') and self.character_class.special_abilities:
            print("\nSpecial Abilities:")
            for ability in self.character_class.special_abilities:
                print(f"  • {ability}")
    
    def allocate_skill_point(self, skill: str) -> bool:
        """Allocate a skill point to a specific skill"""
        if self.skill_points > 0 and skill in self.skills:
            self.skills[skill] += 1
            self.skill_points -= 1
            print(f"Increased {skill} to {self.skills[skill]}!")
            return True
        elif self.skill_points == 0:
            print("No skill points available!")
        else:
            print("Invalid skill!")
        return False
        
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
