from character import Hero
from weapon import iron_sword
from game_utils import (GameState, Shop, EnemyGenerator, clear_screen, 
                       display_combat_menu, display_main_menu, display_inventory, 
                       wait_for_input)
from save_system import SaveSystem
import random

def main():
    # Initialize game
    print("=== WELCOME TO TEXT-BASED BATTLE GAME ===")
    
    # Check for existing save file
    if SaveSystem.has_save_file():
        choice = input("Found existing save file. Load game? (y/n): ").strip().lower()
        if choice == 'y':
            hero, game_state = SaveSystem.load_game()
            if hero and game_state:
                shop = Shop()
                print(f"Welcome back, {hero.name}!")
                wait_for_input()
            else:
                hero, game_state, shop = create_new_game()
        else:
            hero, game_state, shop = create_new_game()
    else:
        hero, game_state, shop = create_new_game()
    
    # Main game loop
    while not game_state.game_over:
        clear_screen()
        print(f"=== ADVENTURE - Day {game_state.turn_count + 1} ===")
        hero.show_stats()
        
        choice = display_main_menu()
        
        if choice == 1:  # Continue Adventure
            battle_loop(hero, game_state)
        elif choice == 2:  # Visit Shop
            shop_loop(hero, shop)
        elif choice == 3:  # View Inventory
            display_inventory(hero)
            wait_for_input()
        elif choice == 4:  # Character Stats
            hero.show_stats()
            wait_for_input()
        elif choice == 5:  # Save Game
            SaveSystem.save_game(hero, game_state)
            wait_for_input()
        elif choice == 6:  # Quit Game
            save_choice = input("Save game before quitting? (y/n): ").strip().lower()
            if save_choice == 'y':
                SaveSystem.save_game(hero, game_state)
            print("Thanks for playing!")
            game_state.game_over = True
    
    print("\n=== GAME OVER ===")
    print(f"Final Stats for {hero.name}:")
    hero.show_stats()
    print(f"Days survived: {game_state.turn_count}")

def create_new_game():
    """Create a new game with fresh hero and game state"""
    hero_name = input("Enter your hero's name: ").strip()
    if not hero_name:
        hero_name = "Hero"
    
    hero = Hero(hero_name, 100, 1)
    hero.equip(iron_sword)
    
    game_state = GameState()
    shop = Shop()
    
    print(f"\nWelcome, {hero.name}! Your adventure begins...")
    wait_for_input()
    
    return hero, game_state, shop

def battle_loop(hero: Hero, game_state: GameState):
    """Main battle loop"""
    # Generate enemy based on hero's level
    enemy_level = max(1, hero.level + random.randint(-1, 2))
    enemy = EnemyGenerator.generate_enemy(enemy_level)
    
    print(f"\n💀 A {enemy.name} (Level {enemy.level}) appears!")
    print(f"Enemy Health: {enemy.health}")
    print(f"Enemy Weapon: {enemy.weapon.name}")
    wait_for_input()
    
    # Battle loop
    while hero.is_alive and enemy.is_alive:
        clear_screen()
        print(f"=== BATTLE: {hero.name} vs {enemy.name} ===")
        
        # Display health bars
        hero.health_bar.draw()
        enemy.health_bar.draw()
        
        # Hero's turn
        if hero.is_alive:
            action = display_combat_menu()
            
            if action == 1:  # Attack
                hero.attack(enemy)
            elif action == 2:  # Use Potion
                hero.use_potion()
            elif action == 3:  # View Stats
                hero.show_stats()
                wait_for_input()
                continue
            elif action == 4:  # Run Away
                if random.random() < 0.7:  # 70% chance to escape
                    print(f"{hero.name} successfully ran away!")
                    wait_for_input()
                    return
                else:
                    print(f"{hero.name} couldn't escape!")
        
        # Enemy's turn
        if enemy.is_alive:
            print()
            enemy.ai_action(hero)
        
        wait_for_input()
    
    # Battle result
    if hero.is_alive:
        print(f"\n🎉 Victory! {hero.name} defeated {enemy.name}!")
        print(f"Gained {enemy.gold} gold!")
        hero.gold += enemy.gold
        game_state.increment_turn()
    else:
        print(f"\n💀 {hero.name} has been defeated...")
        game_state.game_over = True
    
    wait_for_input()

def shop_loop(hero: Hero, shop: Shop):
    """Shop interaction loop"""
    while True:
        clear_screen()
        shop.show_shop(hero)
        
        try:
            choice = int(input("Choose item to buy (or exit): "))
            if choice == len(shop.weapons) + 2:  # Exit shop
                break
            elif 1 <= choice <= len(shop.weapons) + 1:
                shop.buy_item(hero, choice)
                wait_for_input()
            else:
                print("Invalid choice.")
                wait_for_input()
        except ValueError:
            print("Invalid input. Please enter a number.")
            wait_for_input()

if __name__ == "__main__":
    main()