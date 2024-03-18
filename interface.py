import time
from characters import Character
from monsters import Monster


class Interface:

    end_messages: dict = {
        'dead': 'One of your characters is dead. You cannot continue game.',
        'exit': 'You chose to stop game.',
    }

    choice_messages: dict = {
        'character': 'Choose character for fight',
        'monster': 'Choose monster to attack',
        'move': 'Choose character attack',
    }

    character_move_options: dict = {
        '1': 'Use simple attack',
        '2': 'Use ability',
        'q': 'Exit'
    }

    def get_player_choice(self, message_key: str, options: dict = None, can_use_ability: bool = False):
        if options is None:
            options = self.character_move_options
            if not can_use_ability:
                print("Character ran out of mana and can't use ability")
                options.pop('2')
        else:
            options = options.copy()
            options.update({'q': 'Exit game'})
        choice_message = self.choice_messages[message_key]
        return self.ask_player_choice(choice_message=choice_message, options=options)

    def ask_player_choice(self, choice_message: str, options: dict):
        while True:
            print('\n', choice_message)
            for key, value in options.items():
                if type(value) != str:
                    value = self.get_character_info(character=value)
                time.sleep(0.5)
                print(f'{key}. {value}')
            player_choice = input('\n Input choice: ')
            if player_choice in options.keys():
                return player_choice
            print('Invalid choice')

    def get_character_info(self, character: Character | Monster):
        if isinstance(character, Monster):
            return f'{character.__class__.__name__} [HP: {character.hp}]'
        return (f'{character.__class__.__name__} '
         f'[HP: {character.hp} ATTACK: {character.attack} MANA: {character.mana} '
         f'ABILITY: {character.ability_info}]')

    def print_monster_dead(self, monster: Monster, mana_points: int):
        time.sleep(0.5)
        print(f'Monster {monster.__class__.__name__} died!')
        time.sleep(0.5)
        print(f'All characters increase their mana for {mana_points} points')

    def print_character_dead(self, character: Character):
        time.sleep(1)
        print(f'Character {character.__class__.__name__} died...')

    def print_start_game(self, characters: list):
        print('Hello!')
        characters_name = [character.__class__.__name__ for character in characters]
        print(f'Your characters: {characters_name}')

    def print_main_loop_info(self, monsters_quantity: int):
        time.sleep(0.5)
        print(f'You meet {monsters_quantity} monsters on your way!')

    def print_characters_turn(self):
        time.sleep(0.5)
        print('Characters are ready for fight!!!')

    def print_monsters_turn(self):
        time.sleep(0.5)
        print('Beware! Monsters are going to attack!!!')

    def print_use_simple_attack(self, attacking: Character | Monster, victim: Character | Monster, damage: int):
        time.sleep(1)
        print(f'\n{attacking.__class__.__name__} attacks {victim.__class__.__name__} and deals {damage} damage points')

    def print_use_ability(self, message: str):
        time.sleep(1)
        print(f'{message}')

    def print_end_game(self, message_key: str):
        time.sleep(0.5)
        message = self.end_messages[message_key]
        print(message)
