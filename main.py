from character import Hero, Enemy
from weapon import short_bow, iron_sword

hero = Hero("Hero", 100)
hero.equip(iron_sword)
enemy = Enemy("Enemy", 100, short_bow)


while True:
    hero.attack(enemy)
    enemy.attack(hero)
    print(f"Health of {hero.name}: {hero.health}")
    print(f"Health of {enemy.name}: {enemy.health}")

    input()