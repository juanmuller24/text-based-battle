from typing import List, Callable

class Achievement:
    def __init__(self, name: str, description: str, condition: Callable, reward_gold: int = 0, reward_exp: int = 0):
        self.name = name
        self.description = description
        self.condition = condition
        self.reward_gold = reward_gold
        self.reward_exp = reward_exp
        self.unlocked = False
    
    def check_condition(self, hero) -> bool:
        """Check if the achievement condition is met"""
        if not self.unlocked and self.condition(hero):
            self.unlocked = True
            return True
        return False

class AchievementSystem:
    def __init__(self):
        self.achievements = self._create_achievements()
    
    def _create_achievements(self) -> List[Achievement]:
        """Create all available achievements"""
        return [
            Achievement(
                "First Victory",
                "Win your first battle",
                lambda hero: hasattr(hero, 'battles_won') and hero.battles_won >= 1,
                50, 25
            ),
            Achievement(
                "Level Up",
                "Reach level 2",
                lambda hero: hero.level >= 2,
                25, 50
            ),
            Achievement(
                "Warrior",
                "Win 10 battles",
                lambda hero: hasattr(hero, 'battles_won') and hero.battles_won >= 10,
                200, 100
            ),
            Achievement(
                "Rich Adventurer",
                "Accumulate 500 gold",
                lambda hero: hero.gold >= 500,
                0, 100
            ),
            Achievement(
                "Elite Slayer",
                "Defeat an elite enemy",
                lambda hero: hasattr(hero, 'elite_kills') and hero.elite_kills >= 1,
                100, 75
            ),
            Achievement(
                "Boss Hunter",
                "Defeat a boss enemy",
                lambda hero: hasattr(hero, 'boss_kills') and hero.boss_kills >= 1,
                300, 200
            ),
            Achievement(
                "Mage",
                "Cast 20 spells",
                lambda hero: hasattr(hero, 'spells_cast') and hero.spells_cast >= 20,
                150, 100
            ),
            Achievement(
                "Survivor",
                "Survive 50 battles",
                lambda hero: hasattr(hero, 'battles_fought') and hero.battles_fought >= 50,
                500, 250
            ),
            Achievement(
                "Master",
                "Reach level 10",
                lambda hero: hero.level >= 10,
                1000, 500
            )
        ]
    
    def check_achievements(self, hero) -> List[Achievement]:
        """Check all achievements and return newly unlocked ones"""
        newly_unlocked = []
        for achievement in self.achievements:
            if achievement.check_condition(hero):
                newly_unlocked.append(achievement)
                print(f"🏆 Achievement Unlocked: {achievement.name}")
                print(f"   {achievement.description}")
                if achievement.reward_gold > 0:
                    hero.gold += achievement.reward_gold
                    print(f"   Reward: {achievement.reward_gold} gold!")
                if achievement.reward_exp > 0:
                    hero.gain_experience(achievement.reward_exp)
                    print(f"   Reward: {achievement.reward_exp} experience!")
        return newly_unlocked
    
    def show_achievements(self, hero):
        """Display all achievements and their status"""
        print("\n=== ACHIEVEMENTS ===")
        unlocked_count = sum(1 for a in self.achievements if a.unlocked)
        print(f"Progress: {unlocked_count}/{len(self.achievements)} achievements unlocked\n")
        
        for achievement in self.achievements:
            status = "✅" if achievement.unlocked else "❌"
            print(f"{status} {achievement.name}")
            print(f"   {achievement.description}")
            if achievement.reward_gold > 0 or achievement.reward_exp > 0:
                rewards = []
                if achievement.reward_gold > 0:
                    rewards.append(f"{achievement.reward_gold} gold")
                if achievement.reward_exp > 0:
                    rewards.append(f"{achievement.reward_exp} exp")
                print(f"   Rewards: {', '.join(rewards)}")
            print()

def initialize_achievement_tracking(hero):
    """Initialize achievement tracking attributes on hero"""
    if not hasattr(hero, 'battles_won'):
        hero.battles_won = 0
    if not hasattr(hero, 'battles_fought'):
        hero.battles_fought = 0
    if not hasattr(hero, 'elite_kills'):
        hero.elite_kills = 0
    if not hasattr(hero, 'boss_kills'):
        hero.boss_kills = 0
    if not hasattr(hero, 'spells_cast'):
        hero.spells_cast = 0
