from lib import object_types
from lib.model.game_object import GameObject


class Character(GameObject):

    def __init__(self, idx, nick, health, position, items):
        super(Character, self).__init__(idx, position, object_types.CHARACTER)
        self.nick = nick
        self.health = health
        self.items = items
