from character import Hero
from game_utils import (GameState, Shop, EnemyGenerator, clear_screen, 
                       display_combat_menu, display_main_menu, display_inventory, 
                       display_spell_menu, display_skill_menu, wait_for_input)
from save_system import SaveSystem
from achievements import AchievementSystem, initialize_achievement_tracking
from dungeons import DungeonSystem
from character_classes import select_character_class, apply_class_combat_bonuses
from quest_system import QuestSystem, initialize_quest_tracking
import random

def main():
    # Initialize game systems
    print("=== WELCOME TO TEXT-BASED BATTLE GAME ===")
    
    # Check for existing save file
    if SaveSystem.has_save_file():
        choice = input("Found existing save file. Load game? (y/n): ").strip().lower()
        if choice == 'y':
            hero, game_state = SaveSystem.load_game()
            if hero and game_state:
                shop = Shop()
                achievement_system = AchievementSystem()
                dungeon_system = DungeonSystem()
                quest_system = QuestSystem()
                initialize_achievement_tracking(hero)
                initialize_quest_tracking(hero)
                print(f"Welcome back, {hero.name}!")
                wait_for_input()
            else:
                hero, game_state, shop, achievement_system, dungeon_system, quest_system = create_new_game()
        else:
            hero, game_state, shop, achievement_system, dungeon_system, quest_system = create_new_game()
    else:
        hero, game_state, shop, achievement_system, dungeon_system, quest_system = create_new_game()
    
    # Main game loop
    while not game_state.game_over:
        clear_screen()
        print(f"=== ADVENTURE - Day {game_state.turn_count + 1} ===")
        hero.show_stats()
        
        # Check for achievements
        achievement_system.check_achievements(hero)
        
        # Update quest progress
        quest_system.update_all_quests(hero)
        
        choice = display_main_menu()
        
        if choice == 1:  # Continue Adventure
            battle_loop(hero, game_state, achievement_system, quest_system)
        elif choice == 2:  # Explore Dungeons
            dungeon_loop(hero, game_state, dungeon_system, achievement_system, quest_system)
        elif choice == 3:  # Visit Shop
            shop_loop(hero, shop)
        elif choice == 4:  # Visit NPCs
            npc_loop(hero, quest_system)
        elif choice == 5:  # View Inventory
            display_inventory(hero)
            wait_for_input()
        elif choice == 6:  # Character Stats
            hero.show_stats()
            wait_for_input()
        elif choice == 7:  # Skill Points
            display_skill_menu(hero)
        elif choice == 8:  # Quest Log
            quest_system.show_quest_log(hero)
            wait_for_input()
        elif choice == 9:  # Achievements
            achievement_system.show_achievements(hero)
            wait_for_input()
        elif choice == 10:  # Save Game
            SaveSystem.save_game(hero, game_state)
            wait_for_input()
        elif choice == 11:  # Quit Game
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
    
    # Character class selection
    print(f"\nWelcome, {hero_name}! Now choose your path...")
    character_class = select_character_class()
    
    hero = Hero(hero_name, 100, 1)
    
    # Apply character class
    character_class.apply_to_hero(hero)
    
    # Initialize tracking
    initialize_achievement_tracking(hero)
    initialize_quest_tracking(hero)
    
    game_state = GameState()
    shop = Shop()
    achievement_system = AchievementSystem()
    dungeon_system = DungeonSystem()
    quest_system = QuestSystem()
    
    print(f"\nYour adventure begins, {hero.name} the {character_class.name}!")
    wait_for_input()
    
    return hero, game_state, shop, achievement_system, dungeon_system, quest_system

def battle_loop(hero: Hero, game_state: GameState, achievement_system: AchievementSystem, quest_system: QuestSystem):
    """Main battle loop"""
    # Generate enemy based on hero's level
    enemy_level = max(1, hero.level + random.randint(-1, 2))
    enemy = EnemyGenerator.generate_enemy(enemy_level)
    
    print(f"\n💀 A {enemy.name} (Level {enemy.level}) appears!")
    print(f"Enemy Health: {enemy.health}")
    print(f"Enemy Weapon: {enemy.weapon.name}")
    wait_for_input()
    
    # Track battle
    hero.battles_fought += 1
    
    # Battle loop
    while hero.is_alive and enemy.is_alive:
        clear_screen()
        print(f"=== BATTLE: {hero.name} vs {enemy.name} ===")
        
        # Update buffs
        hero.update_buffs()
        enemy.update_buffs()
        
        # Regenerate some mana
        hero.regenerate_mana()
        
        # Display health bars
        hero.health_bar.draw()
        enemy.health_bar.draw()
        
        # Hero's turn
        if hero.is_alive:
            action = display_combat_menu()
            
            if action == 1:  # Attack
                hero.attack(enemy)
            elif action == 2:  # Cast Spell
                spell_choice = display_spell_menu(hero)
                if spell_choice <= len(hero.spells):
                    spell = hero.spells[spell_choice - 1]
                    if hero.cast_spell(spell, enemy):
                        hero.spells_cast += 1
            elif action == 3:  # Use Potion
                hero.use_potion()
            elif action == 4:  # View Stats
                hero.show_stats()
                wait_for_input()
                continue
            elif action == 5:  # Run Away
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
        hero.battles_won += 1
        
        # Track enemy type kills
        if enemy.enemy_type == "elite":
            hero.elite_kills += 1
        elif enemy.enemy_type == "boss":
            hero.boss_kills += 1
        
        # Give skill points occasionally
        if random.random() < 0.3:  # 30% chance
            hero.skill_points += 1
            print("You gained a skill point!")
        
        game_state.increment_turn()
        
        # Check achievements
        achievement_system.check_achievements(hero)
    else:
        print(f"\n💀 {hero.name} has been defeated...")
        game_state.game_over = True
    
    wait_for_input()

def dungeon_loop(hero: Hero, game_state: GameState, dungeon_system: DungeonSystem, achievement_system: AchievementSystem, quest_system: QuestSystem):
    """Dungeon exploration loop"""
    available_dungeons = dungeon_system.show_dungeons(hero.level)
    
    if not available_dungeons:
        print("No dungeons available for your level!")
        wait_for_input()
        return
    
    try:
        choice = int(input("Choose dungeon (0 to cancel): "))
        if choice == 0:
            return
        if 1 <= choice <= len(available_dungeons):
            dungeon = available_dungeons[choice - 1]
            explore_dungeon(hero, game_state, dungeon, achievement_system)
        else:
            print("Invalid choice!")
            wait_for_input()
    except ValueError:
        print("Invalid input!")
        wait_for_input()

def explore_dungeon(hero: Hero, game_state: GameState, dungeon, achievement_system: AchievementSystem):
    """Explore a specific dungeon"""
    print(f"\n🏰 Entering {dungeon.name}...")
    dungeon.reset()
    
    while not dungeon.completed and hero.is_alive:
        room = dungeon.get_current_room()
        if not room:
            break
        
        clear_screen()
        print(f"=== {dungeon.name} ===")
        print(f"Room {dungeon.current_room + 1}/{len(dungeon.rooms)}")
        print(f"\n{room.name}")
        print(room.description)
        
        if room.room_type == "rest":
            print("\nYou found a safe place to rest!")
            heal_amount = hero.health_max // 4
            hero.heal(heal_amount)
            hero.regenerate_mana(hero.mana_max // 2)
            print("You feel refreshed!")
            
        elif room.room_type == "treasure" and room.treasure:
            print(f"\n💰 You found: {room.treasure['name']}!")
            if room.treasure['type'] == 'gold':
                hero.gold += room.treasure['amount']
                print(f"Gained {room.treasure['amount']} gold!")
            elif room.treasure['type'] == 'potion':
                hero.potions += room.treasure['amount']
                print(f"Found {room.treasure['amount']} potions!")
            elif room.treasure['type'] == 'experience':
                hero.gain_experience(room.treasure['amount'])
                print(f"Gained {room.treasure['amount']} experience!")
            
        elif room.enemy and room.enemy.is_alive:
            print(f"\n⚔️ A {room.enemy.name} blocks your path!")
            if not fight_dungeon_enemy(hero, room.enemy, achievement_system):
                return  # Hero died
        
        room.completed = True
        
        if dungeon.current_room < len(dungeon.rooms) - 1:
            input("\nPress Enter to continue to the next room...")
            dungeon.advance_room()
        else:
            dungeon.completed = True
            print(f"\n🎉 You have completed {dungeon.name}!")
            completion_reward = dungeon.max_level * 100
            hero.gold += completion_reward
            hero.gain_experience(completion_reward)
            print(f"Completion reward: {completion_reward} gold and experience!")
            
            # Give skill points for dungeon completion
            hero.skill_points += 2
            print("You gained 2 skill points!")
            
            # Track for quests
            if hasattr(hero, 'dungeons_completed'):
                hero.dungeons_completed += 1
            
            achievement_system.check_achievements(hero)
            break
    
    wait_for_input()

def fight_dungeon_enemy(hero: Hero, enemy, achievement_system: AchievementSystem) -> bool:
    """Fight an enemy in a dungeon room"""
    hero.battles_fought += 1
    
    while hero.is_alive and enemy.is_alive:
        clear_screen()
        print(f"=== DUNGEON BATTLE: {hero.name} vs {enemy.name} ===")
        
        # Update buffs and regenerate mana
        hero.update_buffs()
        enemy.update_buffs()
        hero.regenerate_mana()
        
        # Display health bars
        hero.health_bar.draw()
        enemy.health_bar.draw()
        
        # Hero's turn
        if hero.is_alive:
            action = display_combat_menu()
            
            if action == 1:  # Attack
                hero.attack(enemy)
            elif action == 2:  # Cast Spell
                spell_choice = display_spell_menu(hero)
                if spell_choice <= len(hero.spells):
                    spell = hero.spells[spell_choice - 1]
                    if hero.cast_spell(spell, enemy):
                        hero.spells_cast += 1
            elif action == 3:  # Use Potion
                hero.use_potion()
            elif action == 4:  # View Stats
                hero.show_stats()
                wait_for_input()
                continue
            elif action == 5:  # Run Away
                print("You can't run away from dungeon enemies!")
        
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
        hero.battles_won += 1
        
        # Track enemy type kills
        if enemy.enemy_type == "elite":
            hero.elite_kills += 1
        elif enemy.enemy_type == "boss":
            hero.boss_kills += 1
        
        achievement_system.check_achievements(hero)
        return True
    else:
        print(f"\n💀 {hero.name} has been defeated...")
        return False

def npc_loop(hero: Hero, quest_system: QuestSystem):
    """NPC interaction loop"""
    print("\n=== VILLAGE NPCs ===")
    print("1. Village Elder - Wise keeper of ancient knowledge")
    print("2. Training Master - Teaches combat techniques")
    print("3. Court Wizard - Master of magical arts")
    print("4. Dungeon Keeper - Expert on dangerous places")
    print("5. Return to main menu")
    
    while True:
        try:
            choice = int(input("Visit NPC (1-5): "))
            if choice == 1:
                quest_system.visit_npc("village_elder", hero)
                wait_for_input()
                break
            elif choice == 2:
                quest_system.visit_npc("training_master", hero)
                wait_for_input()
                break
            elif choice == 3:
                quest_system.visit_npc("court_wizard", hero)
                wait_for_input()
                break
            elif choice == 4:
                quest_system.visit_npc("dungeon_keeper", hero)
                wait_for_input()
                break
            elif choice == 5:
                break
            else:
                print("Invalid choice. Please enter 1-5.")
        except ValueError:
            print("Invalid input. Please enter a number.")

def shop_loop(hero: Hero, shop: Shop):
    """Shop interaction loop"""
    while True:
        clear_screen()
        shop.show_shop(hero)
        
        try:
            choice = int(input("Choose item to buy (or exit): "))
            exit_option = len(shop.weapons) + len(shop.spells) + 2  # Weapons + Spells + Potion + Exit
            if choice == exit_option:  # Exit shop
                break
            elif 1 <= choice <= exit_option - 1:
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