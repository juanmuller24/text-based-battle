import json
import os
from character import Hero
from weapon import iron_sword, short_bow, steel_sword, magic_staff, war_hammer, crossbow, dagger, fists

SAVE_FILE = "savegame.json"

class SaveSystem:
    @staticmethod
    def save_game(hero: Hero, game_state, filename: str = SAVE_FILE):
        """Save the current game state to a file"""
        try:
            save_data = {
                "hero": {
                    "name": hero.name,
                    "health": hero.health,
                    "health_max": hero.health_max,
                    "level": hero.level,
                    "experience": hero.experience,
                    "experience_to_next_level": hero.experience_to_next_level,
                    "gold": hero.gold,
                    "potions": hero.potions,
                    "weapon": hero.weapon.name,
                    "inventory": [weapon.name for weapon in hero.inventory]
                },
                "game_state": {
                    "turn_count": game_state.turn_count
                }
            }
            
            with open(filename, 'w') as f:
                json.dump(save_data, f, indent=2)
            
            print(f"Game saved successfully to {filename}!")
            return True
        except Exception as e:
            print(f"Error saving game: {e}")
            return False
    
    @staticmethod
    def load_game(filename: str = SAVE_FILE):
        """Load a saved game from a file"""
        try:
            if not os.path.exists(filename):
                print(f"Save file {filename} not found.")
                return None, None
            
            with open(filename, 'r') as f:
                save_data = json.load(f)
            
            # Recreate hero
            hero_data = save_data["hero"]
            hero = Hero(hero_data["name"], hero_data["health_max"], hero_data["level"])
            hero.health = hero_data["health"]
            hero.experience = hero_data["experience"]
            hero.experience_to_next_level = hero_data["experience_to_next_level"]
            hero.gold = hero_data["gold"]
            hero.potions = hero_data["potions"]
            
            # Restore weapon
            hero.weapon = SaveSystem._get_weapon_by_name(hero_data["weapon"])
            
            # Restore inventory
            hero.inventory = [SaveSystem._get_weapon_by_name(name) for name in hero_data["inventory"]]
            
            # Recreate game state
            from game_utils import GameState
            game_state = GameState()
            game_state.turn_count = save_data["game_state"]["turn_count"]
            
            print(f"Game loaded successfully from {filename}!")
            return hero, game_state
            
        except Exception as e:
            print(f"Error loading game: {e}")
            return None, None
    
    @staticmethod
    def _get_weapon_by_name(name: str):
        """Get weapon object by name"""
        weapon_dict = {
            "Iron Sword": iron_sword,
            "Short Bow": short_bow,
            "Steel Sword": steel_sword,
            "Magic Staff": magic_staff,
            "War Hammer": war_hammer,
            "Crossbow": crossbow,
            "Dagger": dagger,
            "Fists": fists
        }
        return weapon_dict.get(name, fists)
    
    @staticmethod
    def has_save_file(filename: str = SAVE_FILE) -> bool:
        """Check if a save file exists"""
        return os.path.exists(filename)
