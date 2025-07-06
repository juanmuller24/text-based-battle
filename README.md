# Text-Based Battle Game

An enhanced console-based RPG battle game written in Python featuring turn-based combat, character progression, shopping, inventory management, and save/load functionality.

## Features

### Core Gameplay

- **Turn-based combat** with strategic decision-making
- **Character progression** with leveling system and experience points
- **Multiple enemy types** including normal, elite, and boss enemies
- **Dynamic enemy generation** based on player level

### Combat System

- **Critical hit mechanics** with weapon-specific crit chances
- **Multiple combat actions**: Attack, Use Potion, View Stats, Run Away
- **Visual health bars** with color-coded display
- **Smart AI** for enemy behavior

### Equipment & Items

- **Diverse weapon system** with 8 different weapons
- **Weapon types**: Sharp, Ranged, Blunt, Magic
- **Equipment management** with inventory system
- **Healing potions** for health recovery

### Economy & Shop

- **Gold-based economy** with loot from defeated enemies
- **Weapon shop** with various purchasable items
- **Potion shop** for healing supplies
- **Dynamic pricing** based on weapon stats

### Progression

- **Experience system** with level-ups
- **Health increases** on level progression
- **Stat bonuses** based on character level
- **Equipment upgrades** through shop purchases

### Quality of Life

- **Save/Load system** with JSON-based persistence
- **Cross-platform compatibility** (Windows, macOS, Linux)
- **Colorful UI** with ANSI color support
- **Clear menu systems** and intuitive controls

## Game Components

### Characters

- **Hero**: Player character with full customization

  - Equipment management (equip/drop weapons)
  - Inventory system with weapon storage
  - Potion usage for healing
  - Experience and level progression
  - Gold collection and spending
  - Green health bar display
- **Enemy**: AI-controlled opponents with varying difficulty

  - Normal enemies: Standard difficulty
  - Elite enemies: 1.5x health, 2x gold reward
  - Boss enemies: 2.5x health, 3x gold reward
  - Level-scaled stats and equipment
  - Red health bar display

### Weapons Arsenal

1. **Fists** (Default): 2 damage, 5% crit chance
2. **Dagger**: 3 damage, 30% crit chance - Quick and agile
3. **Iron Sword**: 5 damage, 15% crit chance - Sturdy iron blade
4. **Short Bow**: 4 damage, 20% crit chance - Lightweight ranged weapon
5. **Magic Staff**: 6 damage, 25% crit chance - Magical energy weapon
6. **War Hammer**: 7 damage, 8% crit chance - Heavy crushing weapon
7. **Steel Sword**: 8 damage, 12% crit chance - Superior steel blade
8. **Crossbow**: 9 damage, 18% crit chance - Powerful mechanical bow

### Game Systems

- **Health System**: Visual bars with real-time updates
- **Experience System**: Level-based progression with scaling requirements
- **Economy System**: Gold-based trading and equipment purchasing
- **Save System**: JSON-based game state persistence
- **Combat System**: Turn-based with multiple action options

## Installation

1. **Clone the repository**:

   ```bash
   git clone <repository-url>
   cd text-based-battle
   ```
2. **Verify Python installation** (3.6+ required):

   ```bash
   python --version
   ```
3. **Run the game**:

   ```bash
   python main.py
   ```

No additional dependencies required - uses only Python standard library!

## Usage

### Starting the Game

```bash
python main.py
```

### Game Controls

- **Main Menu Navigation**: Choose options 1-6
- **Combat Actions**: Attack, Use Potion, View Stats, Run Away
- **Shop Interaction**: Buy weapons and potions
- **Inventory Management**: Equip/unequip weapons
- **Save/Load**: Persistent game state

### Combat Tips

- **Use potions strategically** - they're limited but restore significant health
- **Run away** from tough enemies if you're low on health
- **Check enemy stats** before engaging in combat
- **Upgrade weapons** regularly at the shop
- **Level up** by defeating enemies to increase your power

## Project Structure

```
text-based-battle/
├── main.py              # Main game loop and entry point
├── character.py         # Character classes (Hero, Enemy, Character)
├── weapon.py           # Weapon class and weapon instances
├── health_bar.py       # Health bar visualization system
├── game_utils.py       # Game utilities, menus, and helper functions
├── save_system.py      # Save/load functionality
├── requirements.txt    # Project dependencies (none required)
├── README.md          # This file
├── .gitignore         # Git ignore rules
└── __pycache__/       # Python bytecode cache (auto-generated)
```

## Code Architecture

### Character System

- **Base Character class**: Core functionality for all characters
- **Hero class**: Player-specific features (inventory, potions, equipment)
- **Enemy class**: AI behavior and different enemy types

### Weapon System

- **Weapon class**: Properties and critical hit calculations
- **Weapon instances**: Pre-configured weapons with unique stats
- **Equipment mechanics**: Equip/unequip functionality

### Game Management

- **GameState class**: Tracks game progression and state
- **Shop class**: Handles commerce and item purchasing
- **EnemyGenerator class**: Procedural enemy creation
- **SaveSystem class**: Game persistence functionality

## Customization

### Adding New Weapons

```python
# In weapon.py
new_weapon = Weapon(
    name="Excalibur",
    weapon_type="legendary",
    damage=15,
    value=100,
    crit_chance=0.4,
    description="The legendary sword of kings"
)
```

### Creating Custom Enemies

```python
# Custom enemy with specific weapon and stats
custom_enemy = Enemy(
    name="Dragon",
    health=500,
    weapon=fire_breath,
    level=10,
    enemy_type="boss"
)
```

### Modifying Game Balance

- **Weapon stats**: Adjust damage, crit chance, and value in `weapon.py`
- **Level progression**: Modify experience requirements in `character.py`
- **Enemy difficulty**: Adjust health multipliers in `game_utils.py`
- **Shop prices**: Change item costs in `game_utils.py`

## Visual Features

### Health Bar System

- **Color-coded bars**: Green for hero, red for enemies
- **Unicode block characters**: Visual representation of health
- **Real-time updates**: Reflects current health status
- **ANSI color support**: Enhanced terminal display

### Menu System

- **Clear navigation**: Numbered options for easy selection
- **Input validation**: Prevents invalid choices
- **Consistent formatting**: Clean, readable interface
- **Cross-platform compatibility**: Works on all major operating systems

## Save System

The game includes a robust save/load system:

- **Automatic detection**: Checks for existing save files on startup
- **Complete state preservation**: Saves all character stats, inventory, and progress
- **JSON format**: Human-readable save files
- **Error handling**: Graceful handling of corrupted save files

## Future Enhancements

### Planned Features

- **Multiple character classes** (Warrior, Mage, Archer)
- **Skill trees** and special abilities
- **Dungeon exploration** with multiple rooms
- **Crafting system** for weapon upgrades
- **Achievement system** with unlockable rewards
- **Multiplayer support** for cooperative gameplay

### Technical Improvements

- **Database integration** for larger save files
- **Configuration files** for easy balance adjustments
- **Sound effects** and music integration
- **GUI version** using tkinter or pygame
- **Web version** with Flask/Django

## Development

### System Requirements

- **Python 3.6+** (tested on 3.6-3.11)
- **Terminal with ANSI support** (most modern terminals)
- **10MB disk space** for game files
- **Cross-platform compatible** (Windows, macOS, Linux)

### Code Quality

- **Type hints** throughout the codebase
- **Modular design** with clear separation of concerns
- **Error handling** for robust gameplay
- **Clean code practices** with meaningful variable names

## License

This project is open source and available under the MIT License.

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for:

- Bug fixes
- New features
- Performance improvements
- Documentation updates
- Balance adjustments

## Acknowledgments

- Built with Python standard library only
- Inspired by classic text-based RPGs
- Designed for educational purposes and fun gameplay
