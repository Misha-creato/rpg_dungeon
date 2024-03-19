import random
import sys
from characters import Character
from monsters import Monster
from interface import Interface
from constants import (
    MIN_MONSTERS_QUANTITY,
    MAX_MONSTERS_QUANTITY,
    CHARACTERS_CLASSES,
    MONSTERS_CLASSES,
)


class Game:
    monsters: dict = {}
    characters: dict = {}
    monster: Monster | None = None
    character: Character | None = None
    interface: Interface = Interface()

    def set_characters(self):
        characters_classes = [cls() for cls in CHARACTERS_CLASSES]
        characters_keys_range = range(1, len(characters_classes) + 1)
        characters_keys = [str(key) for key in characters_keys_range]
        characters = dict(zip(characters_keys, characters_classes))
        self.characters = characters

    def set_monsters(self): # continue
        monsters_quantity = random.randint(a=MIN_MONSTERS_QUANTITY, b=MAX_MONSTERS_QUANTITY)
        monsters_keys_range = range(1, monsters_quantity + 1)
        monsters_keys = [str(key) for key in monsters_keys_range]
        random_monsters_classes = random.choices(population=MONSTERS_CLASSES, k=monsters_quantity)
        random_monsters = [cls() for cls in random_monsters_classes]

        self.monsters = dict(zip(monsters_keys, random_monsters))

    def choose_character(self, available_characters: dict):

        player_choice = self.interface.get_player_choice(
            message_key='character',
            options=available_characters,
        )

        self.character = self.characters.get(player_choice, None)

        if self.character is None:
            self.end(message_key='exit')

        self.character.is_blocked = True

    def character_move(self, player_choice: str):
        if player_choice == '1':
            self.use_simple_attack(attacking=self.character, victim=self.monster)
        elif player_choice == '2':
            self.use_ability()
        else:
            self.end(message_key='exit')

    def characters_turn(self):

        def filter_characters(pair: tuple):
            key, value = pair
            if value.is_blocked:
                return False
            return True

        self.interface.print_characters_turn()
        available_characters = self.characters

        while available_characters and self.monsters:
            self.choose_character(
                available_characters=available_characters,
            )
            self.choose_monster()
            can_use_ability = bool(self.character.mana)
            player_choice = self.interface.get_player_choice(
                message_key='move',
                can_use_ability=can_use_ability
            )
            self.character_move(
                player_choice=player_choice
            )
            self.update_dead_monsters()
            available_characters = dict(filter(filter_characters, available_characters.items()))

    def track_character_death(self):
        if not self.character.is_alive:
            self.interface.print_character_dead(character=self.character)
            self.end(message_key='dead')

    def update_dead_monsters(self):
        dead_monsters = []
        for key, monster in self.monsters.items():
            if not monster.is_alive:
                dead_monsters.append(key)
                self.characters_increase_mana()
                self.interface.print_monster_dead(
                    monster=monster,
                    mana_points=self.character.increase_mana_points
                )
        for monster in dead_monsters:
            self.monsters.pop(monster)

    def characters_increase_mana(self):
        for character in self.characters.values():
            character.increase_mana()

    def end(self, message_key: str):
        self.interface.print_end_game(message_key=message_key)
        sys.exit(0)

    def monsters_turn(self):
        self.interface.print_monsters_turn()
        for monster in self.monsters.values():
            self.character = random.choice(list(self.characters.values()))
            self.monster = monster
            self.use_simple_attack(attacking=self.monster, victim=self.character)
            self.track_character_death()

    def choose_monster(self):
        player_choice = self.interface.get_player_choice(
            message_key='monster',
            options=self.monsters,
        )

        self.monster = self.monsters.get(player_choice, None)

        if self.monster is None:
            self.end(message_key='exit')

    def start(self):
        self.set_characters()
        self.interface.print_start_game()
        while True:
            self.set_monsters()
            self.interface.print_main_loop_info(monsters_quantity=len(self.monsters))
            self.main_loop()

    def main_loop(self):
        while self.monsters:
            self.characters_turn()
            self.unblock_characters()
            self.monsters_turn()

    def unblock_characters(self):
        for character in self.characters.values():
            character.is_blocked = False

    def use_simple_attack(self, attacking: Character | Monster, victim: Character | Monster):
        damage = attacking.attack
        victim.decrease_hp(damage=damage)
        self.interface.print_use_simple_attack(attacking=attacking, victim=victim, damage=damage)

    def use_ability(self):
        # Получение аргументов метода способности персонажа
        required_arguments = self.character.ability.__annotations__.keys()

        # Значения для аргументов метода способности персонажа
        values = [getattr(self, argument) for argument in required_arguments]
        kwargs = dict(zip(required_arguments, values))

        returned_data = self.character.ability(**kwargs)
        for key, value in returned_data.items():
            if key == 'message':
                self.interface.print_use_ability(message=value)
            else:
                setattr(self, key, value)
