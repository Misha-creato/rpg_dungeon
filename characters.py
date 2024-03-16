import random
from monster import Monster


class Character:
    hp: int
    max_hp: int
    mana: int
    max_mana: int
    attack: int
    ability_name: str
    is_blocked: bool = False
    increase_mana_points: int = 10
    decrease_mana_points: int
    is_alive: bool = True

    def __init__(self):
        self.max_hp = self.hp
        self.max_mana = self.mana

    def ability(self, **kwargs) -> dict:
        pass

    def decrease_mana(self):
        self.mana -= self.decrease_mana_points

    def increase_mana(self):
        self.mana += self.increase_mana_points
        if self.mana > self.max_mana:
            self.mana = self.max_mana

    def decrease_hp(self, damage: int):
        self.hp -= damage
        if self.hp <= 0:
            self.is_alive = False

    def increase_hp(self, heal_points: int):
        self.hp += heal_points
        if self.hp > self.max_hp:
            self.hp = self.max_hp

    @property
    def ability_info(self):
        pass

    def __str__(self):
        return (f'{self.__class__.__name__} '
                f'[HP: {self.hp} ATTACK: {self.attack} MANA: {self.mana}'
                f' ABILITY: {self.ability_info}]')


class Wizard(Character):

    ability_damage_min: int = 10
    ability_damage_max: int = 25

    def __init__(self):
        self.hp = 45
        self.mana = 50
        self.attack = 7
        self.decrease_mana_points = 10
        self.ability_name = 'fireball'
        super().__init__()

    def ability(self, monster: Monster):
        self.decrease_mana()
        damage = random.randint(self.ability_damage_min, self.ability_damage_max)
        monster.decrease_hp(damage=damage)

        message = (f'{self.__class__.__name__} deals {monster.name} {damage} damage '
                   f'and loses {self.decrease_mana_points} mana')

        return {'monster': monster, 'ability_message': message}

    @property
    def ability_info(self):
        return (f'{self.ability_name} - '
                f'deals {self.ability_damage_min}-{self.ability_damage_max} damage '
                f'and takes {self.decrease_mana_points} mana')


class Paladin(Character):

    ability_damage_min: int = 8
    ability_damage_max: int = 12

    def __init__(self):
        self.hp = 70
        self.mana = 30
        self.attack = 12
        self.decrease_mana_points = 8
        self.ability_name = 'saint ground'
        super().__init__()

    def ability(self, monsters: dict):
        self.decrease_mana()
        damage = random.randint(self.ability_damage_min, self.ability_damage_max)

        for monster in monsters.values():
            monster.decrease_hp(damage=damage)

        message = (f'{self.__class__.__name__} deals {damage} damage to all monsters '
                   f'and loses {self.decrease_mana_points} mana')

        return {'monsters': monsters, 'ability_message': message}

    @property
    def ability_info(self):
        return (f'{self.ability_name} - deals {self.ability_damage_min}-{self.ability_damage_max} damage '
                f'to all monsters and takes {self.decrease_mana_points} mana')

class Priest(Character):

    ability_heal_points: int = 20

    def __init__(self):
        self.hp = 50
        self.mana = 120
        self.attack = 5
        self.decrease_mana_points = 10
        self.ability_name = 'healing light'
        super().__init__()

    def ability(self, characters: dict):
        self.decrease_mana()
        for character in characters.values():
            character.increase_hp(heal_points=self.ability_heal_points)

        message = (f'{self.__class__.__name__} heals all characters with {self.ability_heal_points} points'
                   f'and loses {self.decrease_mana_points} mana')

        return {'characters': characters, 'ability_message': message}

    @property
    def ability_info(self):
        return (f'{self.ability_name} - heals all player characters for {self.ability_heal_points} points,'
                f' takes {self.decrease_mana_points} mana')
