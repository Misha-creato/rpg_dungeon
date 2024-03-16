from characters import Character
from monster import Monster


class Interface:

    end_messages: dict = {
        'dead': 'One of your characters is dead. You cannot continue game.',
        'exit': 'You choose to stop game.',
    }

    choice_messages: dict = {
        'character': 'Choose character for fight',
        'monster': 'Choose monster to attack',
        'move': 'Choose character attack',
    }

    character_move_options: dict = {
        '1': 'Use simple attack',
        '2': 'Use ability',
        'exit': 'Exit'
    }

    def get_player_choice(self, message_key: str, options: dict = None, can_use_ability: bool = False):
        if options is None:
            options = self.character_move_options
            if not can_use_ability:
                print("Character ran out of mana and can't use ability")
                options.pop('2')
        else:
            options = options.copy()
            options.update({'exit': 'Exit game'})
        choice_message = self.choice_messages[message_key]
        return self.ask_player_choice(choice_message=choice_message, options=options)

    def ask_player_choice(self, choice_message: str, options: dict):
        while True:
            print(choice_message)
            for key, value in options.items():
                print(f'{key}. {value}')
            player_choice = input('Input choice: ')
            if player_choice in options.keys():
                return player_choice
            print('Invalid choice')

    def print_monster_dead(self, name: str, mana_points: int):
        print(f'Monster {name} died!')
        print(f'All characters increase their mana for {mana_points} points')

    def print_character_dead(self, name: str):
        print(f'Character {name} died...')

    def print_start_game(self, characters: list):
        print('Hello!')
        characters_name = [character.__class__.__name__ for character in characters]
        print(f'Your characters: {characters_name}')

    def print_main_loop_info(self, monsters_quantity: int):
        print(f'You meet {monsters_quantity} monsters on your way!')

    def print_characters_turn(self):
        print('Characters are ready for fight!!!')

    def print_monsters_turn(self):
        print('Beware! Monsters are going to attack!!!')

    def print_monster_move(self, monster: Monster):
        print(f'Monster {monster.name} attacks!')

    def print_simple_attack(self, attacking: Character | Monster, victim: Character | Monster, damage: int):
        print(f'{attacking.__class__.__name__} attacks {victim.__class__.__name__} and deals {damage} damage points')

    def print_use_ability(self, message: str):
        print(f'{message}')

    def print_end_game(self, message_key: str):
        message = self.end_messages[message_key]
        print(message)
