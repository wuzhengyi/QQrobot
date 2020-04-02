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
    Q = 4


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
              'shandianniao': PokeLevel.S, 'chaomeng': PokeLevel.S}

pokeNameEng = ['xiaolada', 'bobo', 'miaomiao', 'wasidan', 'apashe',
               'dashetou', 'pikaqiu', 'pipi', 'pangding', 'yibu', 'jilidan', 'dailong', 'menghuan'] + \
              ['lvmaochong', 'dujiaochong', 'lieque', 'chuanshanshu', 'niduolang', 'niduolan', 'maoqiu',
               'liuwei', 'kabishou', 'xipanmoou', 'kentailuo', 'feitiantanglang', 'dajia', 'miaowazhongzi',
               'xiaohuolong', 'jienigui', 'huoyanniao', 'jidongniao', 'shandianniao', 'chaomeng']
pokeNameChn = ['小拉达', '波波', '喵喵', '瓦斯弹', '阿柏蛇',
               '大舌头', '皮卡丘', '皮皮', '胖丁', '伊布', '吉利蛋', '袋龙', '梦幻'] + \
              ['绿毛虫', '独角虫', '烈雀', '穿山鼠', '尼多朗', '尼多兰', '毛球', '六尾',
               '卡比兽', '吸盘魔偶', '肯泰罗', '飞天螳螂', '大甲', '妙蛙种子', '小火龙',
               '杰尼龟', '火焰鸟', '急冻鸟', '闪电鸟', '超梦']

pokeNameChn2Eng = dict(zip(pokeNameChn, pokeNameEng))

allPokemonQ = {'xiaoladae': PokeLevel.D, 'guisi': PokeLevel.D,
              'miaomiaoe': PokeLevel.C, 'heianya': PokeLevel.C, 'chounie': PokeLevel.C,
              'mengyao': PokeLevel.B, 'dailubi': PokeLevel.B, 'guisitong': PokeLevel.B,
              'niula': PokeLevel.A, 'galagalagui': PokeLevel.A, 'banjila': PokeLevel.S, 'genggui': PokeLevel.S, 'xuelabi': PokeLevel.S}

pokeNameEngQ = ['xiaoladae', 'guisi', 'miaomiaoe', 'heianya', 'chounie',
               'mengyao', 'dailubi', 'guisitong', 'niula', 'galagalagui', 'banjila', 'genggui', 'xuelabi']

pokeNameChnQ = ['小拉达(恶)', '鬼斯', '喵喵(恶)', '黑暗鸦', '臭泥(恶)',
               '梦妖', '戴鲁比', '鬼斯通', '纽拉', '嘎啦嘎啦(鬼)', '班吉拉', '耿鬼', '雪拉比']

pokeNameChn2EngQ = dict(zip(pokeNameChn, pokeNameEng))

consNameChn = ['白羊座', '金牛座', '双子座', '巨蟹座', '狮子座',
               '处女座', '天秤座', '天蝎座', '射手座', '摩羯座', '水瓶座', '双鱼座']
consNameEng = ['Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo',
               'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces']
consNameChn2Eng = dict(zip(consNameChn, consNameEng))

stopWord = ['小号', '机器']
