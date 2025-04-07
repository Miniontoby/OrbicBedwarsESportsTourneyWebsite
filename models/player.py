try:
    from .team import Team
except ImportError:
    from team import Team

# Cannot import from below, so need to add to sys.path
import sys
sys.path.insert(0, '..')
from utils import get_player_data

class Player:
    __id: int
    __nickname: str
    __rank: str
    __bedwarsLevel: int
    __team: Team|None = None

    def __init__(self, Id: int, nickname: str, team: Team|int|None = None, hypixel_player_data = None):
        self.id = Id
        self.nickname = nickname
        self.team = team

        if hypixel_player_data is None:
            hypixel_player_data = get_player_data(self.nickname)

        if hypixel_player_data is not None:
            self.__rank = hypixel_player_data["rank"]["cleanName"]
            self.__bedwarsLevel = hypixel_player_data["bedwarsLevel"]["level"]

    @property
    def id(self):
        return self.__id

    @id.setter
    def id(self, value: int):
        if isinstance(value, int) and value >= 0:
            self.__id = value

    @property
    def nickname(self):
        return self.__nickname

    @nickname.setter
    def nickname(self, value: str):
        if isinstance(value, str) and len(value) >= 0:
            self.__nickname = value

    @property
    def rank(self):
        return self.__rank

    @property
    def bedwarsLevel(self):
        return self.__bedwarsLevel

    @property
    def team(self):
        return self.__team

    @team.setter
    def team(self, value: Team|int|None):
        if self.team is not None:
            self.team.remove_player(self)

        if value is None:
            self.__team = None
        elif isinstance(value, int) and value >= 0:
            self.__team = Team(value, "red")
        elif isinstance(value, Team):
            self.__team = value

        if self.team is not None:
            self.team.add_player(self)
