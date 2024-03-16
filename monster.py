
class Monster:

    def __init__(self, name: str, hp: int, attack: int):
        self.name = name
        self.hp = hp
        self.attack = attack
        self.is_alive = True

    def decrease_hp(self, damage: int):
        self.hp -= damage
        if self.hp <= 0:
            self.hp = 0
            self.is_alive = False

    def __str__(self):
        return f'{self.name} [HP: {self.hp}]'
