from enum import Enum, unique


@unique
class State(Enum):
    init = 0
    scene = 1
    catch = 2


@unique
class Choice(Enum):
    A = 0
    B = 1
    C = 2
    D = 3


@unique
class PokeLevel(Enum):
    A = 0
    B = 1
    C = 2
    D = 3
    S = 4


ballName = {'evelsBall': '精灵球', 'superBall': '超级球', 'masterBall': '大师球'}
