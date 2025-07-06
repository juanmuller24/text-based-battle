import random
import os
from character import Hero, Enemy
from weapon import (steel_sword, magic_staff, war_hammer, crossbow, dagger, 
                    short_bow, iron_sword)

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
        self.potion_price = 15
    
    def show_shop(self, hero: Hero):
        print("\n=== WEAPON SHOP ===")
        print(f"Your Gold: {hero.gold}")
        print("\nWeapons for sale:")
        for i, weapon in enumerate(self.weapons):
            print(f"{i+1}. {weapon.name} - {weapon.damage} damage - {weapon.value} gold")
            print(f"   {weapon.description}")
        
        print(f"\n{len(self.weapons)+1}. Healing Potion - {self.potion_price} gold")
        print(f"{len(self.weapons)+2}. Exit shop")
    
    def buy_item(self, hero: Hero, choice: int) -> bool:
        if choice <= len(self.weapons):
            weapon = self.weapons[choice - 1]
            if hero.gold >= weapon.value:
                hero.gold -= weapon.value
                hero.inventory.append(weapon)
                print(f"Purchased {weapon.name}!")
                return True
            else:
                print("Not enough gold!")
                return False
        elif choice == len(self.weapons) + 1:
            if hero.gold >= self.potion_price:
                hero.gold -= self.potion_price
                hero.potions += 1
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
    print("2. Use Potion")
    print("3. View Stats")
    print("4. Run Away")
    
    while True:
        try:
            choice = int(input("Choose action (1-4): "))
            if 1 <= choice <= 4:
                return choice
            else:
                print("Invalid choice. Please enter 1-4.")
        except ValueError:
            print("Invalid input. Please enter a number.")

def display_main_menu() -> int:
    """Display main menu and return choice"""
    print("\n=== MAIN MENU ===")
    print("1. Continue Adventure")
    print("2. Visit Shop")
    print("3. View Inventory")
    print("4. Character Stats")
    print("5. Save Game")
    print("6. Quit Game")
    
    while True:
        try:
            choice = int(input("Choose option (1-6): "))
            if 1 <= choice <= 6:
                return choice
            else:
                print("Invalid choice. Please enter 1-6.")
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

def wait_for_input():
    """Wait for user input to continue"""
    input("\nPress Enter to continue...")
