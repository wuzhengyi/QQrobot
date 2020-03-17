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


ballEng2Chn = {'evelsBall': '精灵球', 'superBall': '超级球', 'masterBall': '大师球'}
ballChn2Eng = {'精灵球': 'evelsBAll', '超级球': 'superBall', '大师球': 'masterBall'}

allPokemon = {'xiaolada': PokeLevel.D, 'bobo': PokeLevel.D,
              'miaomiao': PokeLevel.C, 'wasidan': PokeLevel.C, 'apashe': PokeLevel.C, 'dashetou': PokeLevel.C,
              'pikaqiu': PokeLevel.B, 'pipi': PokeLevel.B, 'pangding': PokeLevel.B, 'yibu': PokeLevel.B,
              'jilidan': PokeLevel.A, 'dailong': PokeLevel.A, 'menghuan': PokeLevel.S}

pokeNameEng = ['xiaolada', 'bobo', 'miaomiao', 'wasidan', 'apashe',
               'dashetou', 'pikaqiu', 'pipi', 'pangding', 'yibu', 'jilidan', 'dailong', 'menghuan']

pokeNameChn = ['小拉达', '波波', '喵喵', '瓦斯弹', '阿柏蛇',
               '大舌头', '皮卡丘', '皮皮', '胖丁', '伊布', '吉利蛋', '袋龙', '梦幻']

pokeNameChn2Eng = dict(zip(pokeNameChn, pokeNameEng))