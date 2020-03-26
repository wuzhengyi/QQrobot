from enum import Enum, unique
import sceneA, sceneB

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

allPokemon = {'xiaolada': PokeLevel.D, 'bobo': PokeLevel.D, 'lvmaochong': PokeLevel.D, 'dujiaochong': PokeLevel.D,
              'miaomiao': PokeLevel.C, 'wasidan': PokeLevel.C, 'apashe': PokeLevel.C, 'dashetou': PokeLevel.C,
              'lieque': PokeLevel.C, 'chuanshanshu': PokeLevel.C, 'niduolang': PokeLevel.C, 'niduolan': PokeLevel.C,
              'maoqiu': PokeLevel.C, 'liuwei': PokeLevel.C,
              'pikaqiu': PokeLevel.B, 'pipi': PokeLevel.B, 'pangding': PokeLevel.B, 'yibu': PokeLevel.B,
              'kabishou': PokeLevel.B, 'xipanmoou': PokeLevel.B, 'kentailuo': PokeLevel.B,
              'feitiantanglang': PokeLevel.B, 'dajia': PokeLevel.B,
              'jilidan': PokeLevel.A, 'dailong': PokeLevel.A, 'miaowazhongzi': PokeLevel.A, 'xiaohuolong': PokeLevel.A,
              'jienigui': PokeLevel.A,
              'menghuan': PokeLevel.S, 'huoyanniao': PokeLevel.S, 'jidongniao': PokeLevel.S,
              'shandianniao': PokeLevel.S, 'chaomeng': PokeLevel.S}}

pokeNameEng = sceneA.pokeNameEng + sceneB.pokeNameEng
pokeNameChn = sceneA.pokeNameChn + sceneB.pokeNameChn

pokeNameChn2Eng = dict(zip(pokeNameChn, pokeNameEng))

consNameChn = ['白羊座', '金牛座', '双子座', '巨蟹座', '狮子座',
'处女座', '天秤座', '天蝎座', '射手座', '摩羯座', '水瓶座', '双鱼座']
consNameEng = ['Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo',
'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces']
consNameChn2Eng = dict(zip(consNameChn, consNameEng))

stopWord = ['小号', '机器']
