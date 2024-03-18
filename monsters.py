
class Monster:

    hp: int
    attack: int
    is_alive: bool = True

    def decrease_hp(self, damage: int):
        self.hp -= damage
        if self.hp <= 0:
            self.hp = 0
            self.is_alive = False


class Rat(Monster):

    hp = 10
    attack = 3


class Goblin(Monster):

    hp = 18
    attack = 7


class MainGoblin(Goblin):

    hp = 25
    attack = 10


class YoungDragon(Monster):

    hp = 37
    attack = 8


class Dragon(YoungDragon):

    hp = 50
    attack = 15


