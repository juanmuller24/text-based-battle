"""
Quest System for Text-Based Battle Game

This module implements a quest system with NPCs, objectives, and story progression.
Quests provide additional goals for players and rewards upon completion.
"""

from typing import Dict, List, Optional, Callable
from enum import Enum


class QuestStatus(Enum):
    NOT_STARTED = "not_started"
    ACTIVE = "active"
    COMPLETED = "completed"
    FAILED = "failed"


class QuestObjective:
    """Represents a single objective within a quest"""
    
    def __init__(self, description: str, check_condition: Callable, target_value: int = 1):
        self.description = description
        self.check_condition = check_condition
        self.target_value = target_value
        self.current_value = 0
        self.completed = False
    
    def update_progress(self, hero):
        """Update objective progress"""
        self.current_value = self.check_condition(hero)
        if self.current_value >= self.target_value:
            self.completed = True
        return self.completed
    
    def get_progress_text(self) -> str:
        """Get progress text for display"""
        status = "✅" if self.completed else "❌"
        return f"{status} {self.description} ({self.current_value}/{self.target_value})"


class Quest:
    """Represents a quest with objectives and rewards"""
    
    def __init__(self, quest_id: str, name: str, description: str, objectives: List[QuestObjective],
                 reward_gold: int = 0, reward_exp: int = 0, reward_items: Optional[List] = None,
                 prerequisite_level: int = 1):
        self.quest_id = quest_id
        self.name = name
        self.description = description
        self.objectives = objectives
        self.reward_gold = reward_gold
        self.reward_exp = reward_exp
        self.reward_items = reward_items or []
        self.prerequisite_level = prerequisite_level
        self.status = QuestStatus.NOT_STARTED
        self.completed_objectives = 0
    
    def can_start(self, hero) -> bool:
        """Check if the hero meets prerequisites to start this quest"""
        return (hero.level >= self.prerequisite_level and 
                self.status == QuestStatus.NOT_STARTED)
    
    def start_quest(self):
        """Start the quest"""
        self.status = QuestStatus.ACTIVE
        print(f"📋 Quest Started: {self.name}")
        print(f"   {self.description}")
    
    def update_progress(self, hero) -> bool:
        """Update quest progress and return True if completed"""
        if self.status != QuestStatus.ACTIVE:
            return False
        
        newly_completed = []
        for objective in self.objectives:
            if not objective.completed and objective.update_progress(hero):
                newly_completed.append(objective)
        
        # Show newly completed objectives
        for objective in newly_completed:
            print(f"📋 Objective Complete: {objective.description}")
        
        # Check if all objectives are complete
        self.completed_objectives = sum(1 for obj in self.objectives if obj.completed)
        if self.completed_objectives == len(self.objectives):
            self.complete_quest(hero)
            return True
        
        return False
    
    def complete_quest(self, hero):
        """Complete the quest and give rewards"""
        self.status = QuestStatus.COMPLETED
        print(f"🎉 Quest Completed: {self.name}")
        
        # Give rewards
        if self.reward_gold > 0:
            hero.gold += self.reward_gold
            print(f"   Reward: {self.reward_gold} gold!")
        
        if self.reward_exp > 0:
            hero.gain_experience(self.reward_exp)
            print(f"   Reward: {self.reward_exp} experience!")
        
        if self.reward_items:
            for item in self.reward_items:
                print(f"   Reward: {item}!")
        
        # Give skill points for quest completion
        hero.skill_points += 1
        print("   Reward: 1 skill point!")
    
    def get_progress_text(self) -> str:
        """Get quest progress for display"""
        if self.status == QuestStatus.NOT_STARTED:
            return f"🔒 {self.name} (Level {self.prerequisite_level}+)"
        elif self.status == QuestStatus.ACTIVE:
            return f"📋 {self.name} ({self.completed_objectives}/{len(self.objectives)})"
        elif self.status == QuestStatus.COMPLETED:
            return f"✅ {self.name} (Complete)"
        else:
            return f"❌ {self.name} (Failed)"


class NPC:
    """Non-Player Character that can give quests"""
    
    def __init__(self, name: str, description: str, quests: Optional[List[str]] = None, shop_items: Optional[List] = None):
        self.name = name
        self.description = description
        self.quests = quests or []  # Quest IDs this NPC can give
        self.shop_items = shop_items or []  # Items this NPC sells
        self.dialogue = {}  # Different dialogue based on quest status
    
    def get_dialogue(self, hero, quest_system) -> str:
        """Get appropriate dialogue based on hero's quest status"""
        available_quests = [quest_system.get_quest(qid) for qid in self.quests 
                          if quest_system.get_quest(qid).can_start(hero)]
        
        if available_quests:
            return f"{self.description}\n\n'{self.name} has a task for you...'"
        else:
            return f"{self.description}\n\n'{self.name} nods at you respectfully.'"


class QuestSystem:
    """Main quest system manager"""
    
    def __init__(self):
        self.quests: Dict[str, Quest] = {}
        self.npcs: Dict[str, NPC] = {}
        self._initialize_quests()
        self._initialize_npcs()
    
    def _initialize_quests(self):
        """Initialize all available quests"""
        
        # Quest 1: First Steps
        first_steps = Quest(
            quest_id="first_steps",
            name="First Steps",
            description="Learn the basics of adventure by winning your first battle and buying equipment.",
            objectives=[
                QuestObjective(
                    "Win 1 battle",
                    lambda hero: getattr(hero, 'battles_won', 0),
                    1
                ),
                QuestObjective(
                    "Buy 1 item from shop",
                    lambda hero: getattr(hero, 'items_purchased', 0),
                    1
                )
            ],
            reward_gold=100,
            reward_exp=50,
            prerequisite_level=1
        )
        
        # Quest 2: Apprentice Warrior
        apprentice_warrior = Quest(
            quest_id="apprentice_warrior",
            name="Apprentice Warrior",
            description="Prove yourself in combat by defeating multiple enemies and reaching level 3.",
            objectives=[
                QuestObjective(
                    "Win 5 battles",
                    lambda hero: getattr(hero, 'battles_won', 0),
                    5
                ),
                QuestObjective(
                    "Reach level 3",
                    lambda hero: hero.level,
                    3
                )
            ],
            reward_gold=200,
            reward_exp=150,
            prerequisite_level=2
        )
        
        # Quest 3: Spell Caster
        spell_caster = Quest(
            quest_id="spell_caster",
            name="Aspiring Mage",
            description="Master the magical arts by learning spells and casting them in battle.",
            objectives=[
                QuestObjective(
                    "Learn 3 spells",
                    lambda hero: len(hero.spells),
                    3
                ),
                QuestObjective(
                    "Cast 10 spells",
                    lambda hero: getattr(hero, 'spells_cast', 0),
                    10
                )
            ],
            reward_gold=300,
            reward_exp=200,
            prerequisite_level=2
        )
        
        # Quest 4: Dungeon Explorer
        dungeon_explorer = Quest(
            quest_id="dungeon_explorer",
            name="Dungeon Explorer",
            description="Explore the depths of dungeons and defeat their guardians.",
            objectives=[
                QuestObjective(
                    "Complete 2 dungeons",
                    lambda hero: getattr(hero, 'dungeons_completed', 0),
                    2
                ),
                QuestObjective(
                    "Defeat 3 elite enemies",
                    lambda hero: getattr(hero, 'elite_kills', 0),
                    3
                )
            ],
            reward_gold=500,
            reward_exp=300,
            prerequisite_level=3
        )
        
        # Quest 5: Master Adventurer
        master_adventurer = Quest(
            quest_id="master_adventurer",
            name="Master Adventurer",
            description="Achieve mastery in all aspects of adventure and become a legend.",
            objectives=[
                QuestObjective(
                    "Reach level 8",
                    lambda hero: hero.level,
                    8
                ),
                QuestObjective(
                    "Accumulate 1000 gold",
                    lambda hero: hero.gold,
                    1000
                ),
                QuestObjective(
                    "Defeat 1 boss enemy",
                    lambda hero: getattr(hero, 'boss_kills', 0),
                    1
                )
            ],
            reward_gold=1000,
            reward_exp=500,
            prerequisite_level=5
        )
        
        # Add quests to system
        for quest in [first_steps, apprentice_warrior, spell_caster, dungeon_explorer, master_adventurer]:
            self.quests[quest.quest_id] = quest
    
    def _initialize_npcs(self):
        """Initialize NPCs and their quest associations"""
        
        village_elder = NPC(
            name="Village Elder",
            description="An wise old man who has seen many adventurers come and go.",
            quests=["first_steps", "master_adventurer"]
        )
        
        training_master = NPC(
            name="Training Master",
            description="A grizzled veteran warrior who trains new recruits.",
            quests=["apprentice_warrior"]
        )
        
        court_wizard = NPC(
            name="Court Wizard",
            description="A mysterious mage who studies the arcane arts.",
            quests=["spell_caster"]
        )
        
        dungeon_keeper = NPC(
            name="Dungeon Keeper",
            description="A keeper of ancient knowledge about dangerous places.",
            quests=["dungeon_explorer"]
        )
        
        self.npcs = {
            "village_elder": village_elder,
            "training_master": training_master,
            "court_wizard": court_wizard,
            "dungeon_keeper": dungeon_keeper
        }
    
    def get_quest(self, quest_id: str) -> Optional[Quest]:
        """Get a quest by ID"""
        return self.quests.get(quest_id)
    
    def get_available_quests(self, hero) -> List[Quest]:
        """Get all quests available to start for the hero"""
        return [quest for quest in self.quests.values() if quest.can_start(hero)]
    
    def get_active_quests(self) -> List[Quest]:
        """Get all currently active quests"""
        return [quest for quest in self.quests.values() if quest.status == QuestStatus.ACTIVE]
    
    def update_all_quests(self, hero):
        """Update progress for all active quests"""
        newly_completed = []
        for quest in self.get_active_quests():
            if quest.update_progress(hero):
                newly_completed.append(quest)
        return newly_completed
    
    def show_quest_log(self, hero):
        """Display the quest log"""
        print("\n=== QUEST LOG ===")
        
        active_quests = self.get_active_quests()
        completed_quests = [q for q in self.quests.values() if q.status == QuestStatus.COMPLETED]
        available_quests = self.get_available_quests(hero)
        
        if active_quests:
            print("\nActive Quests:")
            for quest in active_quests:
                print(f"  {quest.get_progress_text()}")
                for objective in quest.objectives:
                    print(f"    {objective.get_progress_text()}")
        
        if available_quests:
            print("\nAvailable Quests:")
            for quest in available_quests:
                print(f"  {quest.get_progress_text()}")
        
        if completed_quests:
            print(f"\nCompleted Quests: {len(completed_quests)}")
            for quest in completed_quests:
                print(f"  {quest.get_progress_text()}")
        
        if not active_quests and not available_quests and not completed_quests:
            print("No quests available at your current level.")
    
    def visit_npc(self, npc_id: str, hero):
        """Visit an NPC and interact with them"""
        npc = self.npcs.get(npc_id)
        if not npc:
            print("NPC not found!")
            return
        
        print(f"\n=== {npc.name} ===")
        print(npc.get_dialogue(hero, self))
        
        # Show available quests from this NPC
        available_quests = []
        for qid in npc.quests:
            quest = self.get_quest(qid)
            if quest and quest.can_start(hero):
                available_quests.append(quest)
        
        if available_quests:
            print("\nAvailable Quests:")
            for i, quest in enumerate(available_quests):
                print(f"{i+1}. {quest.name}")
                print(f"   {quest.description}")
                rewards = []
                if quest.reward_gold > 0:
                    rewards.append(f"{quest.reward_gold} gold")
                if quest.reward_exp > 0:
                    rewards.append(f"{quest.reward_exp} exp")
                if rewards:
                    print(f"   Rewards: {', '.join(rewards)}")
                print()
            
            try:
                choice = int(input(f"Accept quest (1-{len(available_quests)}) or 0 to leave: "))
                if 1 <= choice <= len(available_quests):
                    quest = available_quests[choice - 1]
                    quest.start_quest()
                    return True
            except ValueError:
                pass
        
        return False


def initialize_quest_tracking(hero):
    """Initialize quest tracking attributes on hero"""
    if not hasattr(hero, 'items_purchased'):
        hero.items_purchased = 0
    if not hasattr(hero, 'dungeons_completed'):
        hero.dungeons_completed = 0
