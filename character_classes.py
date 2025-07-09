"""
Character Classes System for Text-Based Battle Game

This module defines different character classes that players can choose from,
each with unique starting stats, equipment, spells, and progression bonuses.
"""

from typing import Dict, List, Optional
from weapon import iron_sword, short_bow, dagger, magic_staff
from spells import minor_heal, fireball, heal


class CharacterClass:
    """Base class for character classes"""
    
    def __init__(self, name: str, description: str, starting_weapon, starting_spells: Optional[List] = None,
                 stat_bonuses: Optional[Dict[str, int]] = None, special_abilities: Optional[List[str]] = None):
        self.name = name
        self.description = description
        self.starting_weapon = starting_weapon
        self.starting_spells = starting_spells if starting_spells is not None else []
        self.stat_bonuses = stat_bonuses if stat_bonuses is not None else {}
        self.special_abilities = special_abilities if special_abilities is not None else []
    
    def apply_to_hero(self, hero):
        """Apply class bonuses and equipment to a hero"""
        # Apply stat bonuses
        for stat, bonus in self.stat_bonuses.items():
            if stat in hero.skills:
                hero.skills[stat] += bonus
        
        # Equip starting weapon
        hero.equip(self.starting_weapon)
        
        # Learn starting spells
        for spell in self.starting_spells:
            hero.learn_spell(spell)
        
        # Adjust mana based on intelligence
        hero.mana_max = 50 + (hero.skills["intelligence"] * 2)
        hero.mana = hero.mana_max
        
        # Store class reference
        hero.character_class = self
        
        print(f"\n🎭 {hero.name} has become a {self.name}!")
        print(f"✨ {self.description}")
        
        if self.stat_bonuses:
            print("📊 Class bonuses applied:")
            for stat, bonus in self.stat_bonuses.items():
                if bonus > 0:
                    print(f"  +{bonus} {stat.capitalize()}")
        
        if self.starting_spells:
            print("📚 Starting spells learned:")
            for spell in self.starting_spells:
                print(f"  - {spell.name}")


# Define character classes
warrior_class = CharacterClass(
    name="Warrior",
    description="A mighty melee fighter with exceptional strength and endurance.",
    starting_weapon=iron_sword,
    starting_spells=[minor_heal],
    stat_bonuses={
        "strength": 5,
        "agility": 2,
        "intelligence": -2,
        "luck": 1
    },
    special_abilities=["Weapon Mastery", "Battle Rage"]
)

mage_class = CharacterClass(
    name="Mage",
    description="A master of arcane arts with powerful spells and high intelligence.",
    starting_weapon=magic_staff,
    starting_spells=[minor_heal, fireball, heal],
    stat_bonuses={
        "strength": -2,
        "agility": 1,
        "intelligence": 6,
        "luck": 1
    },
    special_abilities=["Spell Power", "Mana Efficiency"]
)

archer_class = CharacterClass(
    name="Archer",
    description="A swift ranged combatant with keen eyes and deadly precision.",
    starting_weapon=short_bow,
    starting_spells=[minor_heal],
    stat_bonuses={
        "strength": 1,
        "agility": 5,
        "intelligence": 1,
        "luck": 4
    },
    special_abilities=["Precise Shot", "Eagle Eye"]
)

rogue_class = CharacterClass(
    name="Rogue",
    description="A cunning trickster who relies on speed, luck, and stealth.",
    starting_weapon=dagger,
    starting_spells=[minor_heal],
    stat_bonuses={
        "strength": 1,
        "agility": 4,
        "intelligence": 2,
        "luck": 5
    },
    special_abilities=["Sneak Attack", "Lucky Strike"]
)

# List of all available classes
AVAILABLE_CLASSES = [warrior_class, mage_class, archer_class, rogue_class]


def display_class_selection():
    """Display available character classes for selection"""
    print("\n=== CHARACTER CLASS SELECTION ===")
    print("Choose your character class:")
    print()
    
    for i, char_class in enumerate(AVAILABLE_CLASSES):
        print(f"{i+1}. {char_class.name}")
        print(f"   {char_class.description}")
        print(f"   Starting Weapon: {char_class.starting_weapon.name}")
        
        if char_class.stat_bonuses:
            bonuses = []
            for stat, bonus in char_class.stat_bonuses.items():
                if bonus != 0:
                    sign = "+" if bonus > 0 else ""
                    bonuses.append(f"{sign}{bonus} {stat.capitalize()}")
            print(f"   Stat Bonuses: {', '.join(bonuses)}")
        
        if char_class.starting_spells:
            spells = [spell.name for spell in char_class.starting_spells]
            print(f"   Starting Spells: {', '.join(spells)}")
        
        print()
    
    return AVAILABLE_CLASSES


def select_character_class():
    """Allow player to select a character class"""
    available_classes = display_class_selection()
    
    while True:
        try:
            choice = int(input(f"Choose class (1-{len(available_classes)}): "))
            if 1 <= choice <= len(available_classes):
                return available_classes[choice - 1]
            else:
                print(f"Invalid choice. Please enter 1-{len(available_classes)}.")
        except ValueError:
            print("Invalid input. Please enter a number.")


def get_class_level_bonuses(character_class: CharacterClass, new_level: int) -> Dict[str, int]:
    """Get class-specific bonuses for leveling up"""
    bonuses = {}
    
    # Every 3 levels, characters get class-specific bonuses
    if new_level % 3 == 0:
        if character_class.name == "Warrior":
            bonuses["strength"] = 2
            bonuses["agility"] = 1
        elif character_class.name == "Mage":
            bonuses["intelligence"] = 2
            bonuses["luck"] = 1
        elif character_class.name == "Archer":
            bonuses["agility"] = 2
            bonuses["luck"] = 1
        elif character_class.name == "Rogue":
            bonuses["luck"] = 2
            bonuses["agility"] = 1
    
    return bonuses


def apply_class_combat_bonuses(hero, damage: int) -> int:
    """Apply class-specific combat bonuses"""
    if not hasattr(hero, 'character_class'):
        return damage
    
    char_class = hero.character_class
    
    # Warrior: Extra damage with melee weapons
    if char_class.name == "Warrior" and hero.weapon.weapon_type in ["sharp", "blunt"]:
        damage = int(damage * 1.15)
    
    # Mage: Extra damage with magic weapons and spells
    elif char_class.name == "Mage" and hero.weapon.weapon_type == "magic":
        damage = int(damage * 1.10)
    
    # Archer: Extra damage with ranged weapons
    elif char_class.name == "Archer" and hero.weapon.weapon_type == "ranged":
        damage = int(damage * 1.20)
    
    # Rogue: Chance for extra damage based on luck
    elif char_class.name == "Rogue":
        import random
        luck_bonus = hero.skills.get("luck", 10)
        if random.random() < (luck_bonus * 0.01):  # Luck% chance for bonus damage
            damage = int(damage * 1.5)
            print("💀 Sneak Attack! Critical damage!")
    
    return damage


def get_class_mana_bonus(character_class: CharacterClass) -> float:
    """Get class-specific mana efficiency bonus"""
    if character_class.name == "Mage":
        return 0.8  # Mages use 20% less mana
    elif character_class.name == "Warrior":
        return 1.2  # Warriors use 20% more mana
    else:
        return 1.0  # Standard mana usage
