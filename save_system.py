import json
import os
from character import Hero
from weapon import iron_sword, short_bow, steel_sword, magic_staff, war_hammer, crossbow, dagger, fists
from spells import fireball, heal, lightning_bolt, minor_heal, frost_lance, divine_blessing

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
                    "mana": hero.mana,
                    "mana_max": hero.mana_max,
                    "level": hero.level,
                    "experience": hero.experience,
                    "experience_to_next_level": hero.experience_to_next_level,
                    "gold": hero.gold,
                    "potions": hero.potions,
                    "skill_points": hero.skill_points,
                    "weapon": hero.weapon.name,
                    "character_class": hero.character_class.name if hasattr(hero, 'character_class') else None,
                    "inventory": [weapon.name for weapon in hero.inventory],
                    "spells": [spell.name for spell in hero.spells],
                    "skills": hero.skills,
                    "battles_won": getattr(hero, 'battles_won', 0),
                    "battles_fought": getattr(hero, 'battles_fought', 0),
                    "elite_kills": getattr(hero, 'elite_kills', 0),
                    "boss_kills": getattr(hero, 'boss_kills', 0),
                    "spells_cast": getattr(hero, 'spells_cast', 0)
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
            hero.mana = hero_data.get("mana", 50)
            hero.mana_max = hero_data.get("mana_max", 50)
            hero.experience = hero_data["experience"]
            hero.experience_to_next_level = hero_data["experience_to_next_level"]
            hero.gold = hero_data["gold"]
            hero.potions = hero_data["potions"]
            hero.skill_points = hero_data.get("skill_points", 0)
            
            # Restore skills
            if "skills" in hero_data:
                hero.skills = hero_data["skills"]
            
            # Restore weapon
            hero.weapon = SaveSystem._get_weapon_by_name(hero_data["weapon"])
            
            # Restore inventory
            hero.inventory = [SaveSystem._get_weapon_by_name(name) for name in hero_data["inventory"]]
            
            # Restore spells
            if "spells" in hero_data:
                hero.spells = [SaveSystem._get_spell_by_name(name) for name in hero_data["spells"]]
            
            # Restore character class
            if "character_class" in hero_data and hero_data["character_class"]:
                from character_classes import AVAILABLE_CLASSES
                for char_class in AVAILABLE_CLASSES:
                    if char_class.name == hero_data["character_class"]:
                        hero.character_class = char_class
                        break
            
            # Restore achievement tracking
            hero.battles_won = hero_data.get("battles_won", 0)
            hero.battles_fought = hero_data.get("battles_fought", 0)
            hero.elite_kills = hero_data.get("elite_kills", 0)
            hero.boss_kills = hero_data.get("boss_kills", 0)
            hero.spells_cast = hero_data.get("spells_cast", 0)
            
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
    def _get_spell_by_name(name: str):
        """Get spell object by name"""
        spell_dict = {
            "Fireball": fireball,
            "Heal": heal,
            "Lightning Bolt": lightning_bolt,
            "Minor Heal": minor_heal,
            "Frost Lance": frost_lance,
            "Divine Blessing": divine_blessing
        }
        return spell_dict.get(name)
    
    @staticmethod
    def has_save_file(filename: str = SAVE_FILE) -> bool:
        """Check if a save file exists"""
        return os.path.exists(filename)
