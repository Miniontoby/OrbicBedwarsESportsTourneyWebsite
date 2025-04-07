class Team:
    __id: int
    __color: str
    __score: int
    __players: list

    def __init__(self, Id: int, color: str, score: int = 0):
        self.id = Id
        self.color = color
        self.score = score
        self.__players = []

    @property
    def id(self):
        return self.__id

    @id.setter
    def id(self, value: int):
        if isinstance(value, int) and value >= 0:
            self.__id = value

    @property
    def color(self):
        return self.__color

    @color.setter
    def color(self, value: str):
        if isinstance(value, str) and len(value) > 0:
            self.__color = value

    @property
    def score(self):
        return self.__score

    @score.setter
    def score(self, value: int):
        if isinstance(value, int) and value >= 0:
            self.__score = value

    @property
    def players(self):
        return self.__players

    def add_player(self, player):
        try:
            from .player import Player
        except ImportError:
            from player import Player

        if isinstance(player, Player):
            if not player in self.players:
                self.players.append(player)

    def remove_player(self, player):
        try:
            from .player import Player
        except ImportError:
            from player import Player

        if isinstance(player, Player):
            if player in self.players:
                self.players.remove(player)
