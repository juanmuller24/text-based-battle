import random
from typing import List, Optional, Dict, Any
from character import Enemy
from weapon import short_bow, iron_sword, steel_sword, war_hammer, crossbow, magic_staff

class Room:
    def __init__(self, name: str, description: str, room_type: str = "normal"):
        self.name = name
        self.description = description
        self.room_type = room_type  # "normal", "treasure", "boss", "rest"
        self.completed = False
        self.enemy: Optional[Enemy] = None
        self.treasure: Optional[Dict[str, Any]] = None

class Dungeon:
    def __init__(self, name: str, min_level: int, max_level: int):
        self.name = name
        self.min_level = min_level
        self.max_level = max_level
        self.rooms = self._generate_rooms()
        self.current_room = 0
        self.completed = False
    
    def _generate_rooms(self) -> List[Room]:
        """Generate rooms for the dungeon"""
        rooms = []
        
        # Generate 5-8 rooms
        num_rooms = random.randint(5, 8)
        
        for i in range(num_rooms):
            if i == 0:
                # First room is always normal
                room_type = "normal"
            elif i == num_rooms - 1:
                # Last room is always boss
                room_type = "boss"
            else:
                # Random room types for middle rooms
                room_type = random.choice(["normal", "normal", "treasure", "rest"])
            
            room = self._create_room(room_type, i)
            rooms.append(room)
        
        return rooms
    
    def _create_room(self, room_type: str, room_number: int) -> Room:
        """Create a specific type of room"""
        room_names = {
            "normal": ["Dark Corridor", "Ancient Chamber", "Crumbling Hall", "Shadowy Passage"],
            "treasure": ["Treasure Chamber", "Hidden Vault", "Golden Room", "Secret Cache"],
            "boss": ["Throne Room", "Final Chamber", "Boss Arena", "Dark Sanctum"],
            "rest": ["Safe Haven", "Healing Spring", "Meditation Chamber", "Peaceful Alcove"]
        }
        
        descriptions = {
            "normal": "A dangerous area filled with enemies.",
            "treasure": "A room containing valuable treasures.",
            "boss": "The final chamber where a powerful enemy awaits.",
            "rest": "A safe place to rest and recover."
        }
        
        name = random.choice(room_names[room_type])
        description = descriptions[room_type]
        
        room = Room(f"Room {room_number + 1}: {name}", description, room_type)
        
        # Populate room based on type
        if room_type in ["normal", "boss"]:
            room.enemy = self._generate_room_enemy(room_type)
        elif room_type == "treasure":
            room.treasure = self._generate_treasure()
        
        return room
    
    def _generate_room_enemy(self, room_type: str) -> Enemy:
        """Generate an enemy for the room"""
        enemy_names = ["Cave Troll", "Shadow Beast", "Undead Warrior", "Dark Mage", "Stone Golem"]
        
        if room_type == "boss":
            enemy_names = ["Dungeon Lord", "Ancient Dragon", "Lich King", "Demon Prince", "Elder Beast"]
        
        name = random.choice(enemy_names)
        level = random.randint(self.min_level, self.max_level)
        base_health = random.randint(80, 120)
        health = base_health + (level * 15)
        
        # Select weapon
        weapons = [short_bow, iron_sword, steel_sword, war_hammer, crossbow, magic_staff]
        weapon = random.choice(weapons)
        
        enemy_type = "boss" if room_type == "boss" else random.choice(["normal", "elite"])
        
        return Enemy(name, health, weapon, level, enemy_type)
    
    def _generate_treasure(self) -> dict:
        """Generate treasure for treasure rooms"""
        treasures = [
            {"type": "gold", "amount": random.randint(100, 300), "name": "Gold Coins"},
            {"type": "potion", "amount": random.randint(2, 5), "name": "Health Potions"},
            {"type": "experience", "amount": random.randint(50, 150), "name": "Ancient Tome"},
        ]
        
        return random.choice(treasures)
    
    def get_current_room(self) -> Optional[Room]:
        """Get the current room"""
        if self.current_room < len(self.rooms):
            return self.rooms[self.current_room]
        return None
    
    def advance_room(self) -> bool:
        """Advance to the next room"""
        if self.current_room < len(self.rooms) - 1:
            self.current_room += 1
            return True
        else:
            self.completed = True
            return False
    
    def reset(self):
        """Reset the dungeon"""
        self.current_room = 0
        self.completed = False
        for room in self.rooms:
            room.completed = False

class DungeonSystem:
    def __init__(self):
        self.dungeons = [
            Dungeon("Goblin Caves", 1, 3),
            Dungeon("Abandoned Mine", 3, 5),
            Dungeon("Dark Forest Temple", 5, 7),
            Dungeon("Ancient Ruins", 7, 10),
            Dungeon("Dragon's Lair", 10, 15)
        ]
    
    def get_available_dungeons(self, hero_level: int) -> List[Dungeon]:
        """Get dungeons suitable for the hero's level"""
        suitable = []
        for dungeon in self.dungeons:
            if hero_level >= dungeon.min_level - 2:  # Allow slightly lower level access
                suitable.append(dungeon)
        return suitable
    
    def show_dungeons(self, hero_level: int):
        """Display available dungeons"""
        available = self.get_available_dungeons(hero_level)
        
        print("\n=== AVAILABLE DUNGEONS ===")
        for i, dungeon in enumerate(available):
            status = "✅ Completed" if dungeon.completed else "🗡️ Available"
            difficulty = "Easy" if hero_level > dungeon.max_level else "Normal" if hero_level >= dungeon.min_level else "Hard"
            
            print(f"{i+1}. {dungeon.name}")
            print(f"   Level Range: {dungeon.min_level}-{dungeon.max_level}")
            print(f"   Difficulty: {difficulty}")
            print(f"   Status: {status}")
            print(f"   Rooms: {len(dungeon.rooms)}")
            print()
        
        return available
