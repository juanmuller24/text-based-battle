import random
import os
from character import Hero, Enemy
from weapon import (steel_sword, magic_staff, war_hammer, crossbow, dagger, 
                    short_bow, iron_sword)
from spells import fireball, heal, lightning_bolt, frost_lance, divine_blessing

class GameState:
    def __init__(self):
        self.turn_count = 0
        self.game_over = False
        self.victory = False
        
    def increment_turn(self):
        self.turn_count += 1

class Shop:
    def __init__(self):
        self.weapons = [steel_sword, magic_staff, war_hammer, crossbow, dagger]
        self.spells = [fireball, heal, lightning_bolt, frost_lance, divine_blessing]
        self.potion_price = 15
    
    def show_shop(self, hero: Hero):
        print("\n=== WEAPON & MAGIC SHOP ===")
        print(f"Your Gold: {hero.gold}")
        
        print("\nWeapons for sale:")
        for i, weapon in enumerate(self.weapons):
            print(f"{i+1}. {weapon.name} - {weapon.damage} damage - {weapon.value} gold")
            print(f"   {weapon.description}")
        
        print("\nSpells for sale:")
        start_idx = len(self.weapons)
        for i, spell in enumerate(self.spells):
            spell_idx = start_idx + i + 1
            price = spell.mana_cost * 10  # Price based on mana cost
            knows_spell = spell in hero.spells
            status = " (Already Known)" if knows_spell else ""
            print(f"{spell_idx}. {spell.name} - {price} gold{status}")
            print(f"   {spell.description} (Cost: {spell.mana_cost} mana)")
        
        potion_idx = len(self.weapons) + len(self.spells) + 1
        print(f"\n{potion_idx}. Healing Potion - {self.potion_price} gold")
        print(f"{potion_idx + 1}. Exit shop")
    
    def buy_item(self, hero: Hero, choice: int) -> bool:
        if choice <= len(self.weapons):
            weapon = self.weapons[choice - 1]
            if hero.gold >= weapon.value:
                hero.gold -= weapon.value
                hero.inventory.append(weapon)
                
                # Track for quests
                if hasattr(hero, 'items_purchased'):
                    hero.items_purchased += 1
                
                print(f"Purchased {weapon.name}!")
                return True
            else:
                print("Not enough gold!")
                return False
        
        elif choice <= len(self.weapons) + len(self.spells):
            spell_idx = choice - len(self.weapons) - 1
            spell = self.spells[spell_idx]
            price = spell.mana_cost * 10
            
            if spell in hero.spells:
                print(f"You already know {spell.name}!")
                return False
            
            if hero.gold >= price:
                hero.gold -= price
                hero.learn_spell(spell)
                
                # Track for quests
                if hasattr(hero, 'items_purchased'):
                    hero.items_purchased += 1
                
                print(f"Learned {spell.name}!")
                return True
            else:
                print("Not enough gold!")
                return False
        
        elif choice == len(self.weapons) + len(self.spells) + 1:
            if hero.gold >= self.potion_price:
                hero.gold -= self.potion_price
                hero.potions += 1
                
                # Track for quests
                if hasattr(hero, 'items_purchased'):
                    hero.items_purchased += 1
                
                print("Purchased healing potion!")
                return True
            else:
                print("Not enough gold!")
                return False
        return False

class EnemyGenerator:
    enemy_names = ["Goblin", "Orc", "Skeleton", "Bandit", "Wolf", "Spider", "Troll", "Dark Knight"]
    
    @staticmethod
    def generate_enemy(level: int) -> Enemy:
        name = random.choice(EnemyGenerator.enemy_names)
        base_health = random.randint(60, 100)
        health = base_health + (level * 10)
        
        # Select weapon based on level
        weapons = [short_bow, iron_sword, steel_sword, war_hammer, crossbow]
        weapon = random.choice(weapons[:min(len(weapons), level + 2)])
        
        # Determine enemy type
        enemy_type = "normal"
        if random.random() < 0.1:  # 10% chance for elite
            enemy_type = "elite"
            name = f"Elite {name}"
        elif random.random() < 0.05:  # 5% chance for boss
            enemy_type = "boss"
            name = f"Boss {name}"
        
        return Enemy(name, health, weapon, level, enemy_type)

def clear_screen():
    """Clear the console screen"""
    os.system("cls" if os.name == "nt" else "clear")

def display_combat_menu() -> int:
    """Display combat menu and return choice"""
    print("\n=== COMBAT MENU ===")
    print("1. Attack")
    print("2. Cast Spell")
    print("3. Use Potion")
    print("4. View Stats")
    print("5. Run Away")
    
    while True:
        try:
            choice = int(input("Choose action (1-5): "))
            if 1 <= choice <= 5:
                return choice
            else:
                print("Invalid choice. Please enter 1-5.")
        except ValueError:
            print("Invalid input. Please enter a number.")

def display_spell_menu(hero: Hero) -> int:
    """Display spell menu and return choice"""
    if not hero.spells:
        print("You don't know any spells!")
        return 0
    
    print(f"\n=== SPELL MENU === (Mana: {hero.mana}/{hero.mana_max})")
    for i, spell in enumerate(hero.spells):
        can_cast = "✅" if hero.mana >= spell.mana_cost else "❌"
        print(f"{i+1}. {spell.name} - {spell.mana_cost} mana {can_cast}")
        print(f"   {spell.description}")
    
    print(f"{len(hero.spells)+1}. Cancel")
    
    while True:
        try:
            choice = int(input("Choose spell: "))
            if 1 <= choice <= len(hero.spells) + 1:
                return choice
            else:
                print(f"Invalid choice. Please enter 1-{len(hero.spells)+1}.")
        except ValueError:
            print("Invalid input. Please enter a number.")

def display_main_menu() -> int:
    """Display main menu and return choice"""
    print("\n=== MAIN MENU ===")
    print("1. Continue Adventure")
    print("2. Explore Dungeons")
    print("3. Visit Shop")
    print("4. Visit NPCs")
    print("5. View Inventory")
    print("6. Character Stats")
    print("7. Skill Points")
    print("8. Quest Log")
    print("9. Achievements")
    print("10. Save Game")
    print("11. Quit Game")
    
    while True:
        try:
            choice = int(input("Choose option (1-11): "))
            if 1 <= choice <= 11:
                return choice
            else:
                print("Invalid choice. Please enter 1-11.")
        except ValueError:
            print("Invalid input. Please enter a number.")

def display_inventory(hero: Hero):
    """Display hero's inventory"""
    print(f"\n=== {hero.name}'s INVENTORY ===")
    print(f"Current Weapon: {hero.weapon.name}")
    print(f"Gold: {hero.gold}")
    print(f"Potions: {hero.potions}")
    
    if hero.inventory:
        print("\nWeapons in inventory:")
        for i, weapon in enumerate(hero.inventory):
            print(f"{i+1}. {weapon.name} - {weapon.damage} damage")
        
        print(f"\n{len(hero.inventory)+1}. Exit inventory")
        
        while True:
            try:
                choice = int(input("Equip weapon (enter number): "))
                if 1 <= choice <= len(hero.inventory):
                    old_weapon = hero.weapon
                    hero.weapon = hero.inventory[choice - 1]
                    hero.inventory[choice - 1] = old_weapon
                    print(f"Equipped {hero.weapon.name}!")
                    break
                elif choice == len(hero.inventory) + 1:
                    break
                else:
                    print("Invalid choice.")
            except ValueError:
                print("Invalid input. Please enter a number.")
    else:
        print("Inventory is empty.")

def display_skill_menu(hero: Hero):
    """Display skill allocation menu"""
    if hero.skill_points == 0:
        print("No skill points available!")
        wait_for_input()
        return
    
    while hero.skill_points > 0:
        print(f"\n=== SKILL ALLOCATION === (Points available: {hero.skill_points})")
        print("Current Skills:")
        skills = list(hero.skills.keys())
        for i, (skill, value) in enumerate(hero.skills.items()):
            print(f"{i+1}. {skill.capitalize()}: {value}")
        
        print(f"{len(skills)+1}. Exit")
        
        try:
            choice = int(input("Allocate point to skill: "))
            if 1 <= choice <= len(skills):
                skill_name = skills[choice - 1]
                hero.allocate_skill_point(skill_name)
            elif choice == len(skills) + 1:
                break
            else:
                print("Invalid choice.")
        except ValueError:
            print("Invalid input. Please enter a number.")
    
    wait_for_input()

def wait_for_input():
    """Wait for user input to continue"""
    input("\nPress Enter to continue...")
