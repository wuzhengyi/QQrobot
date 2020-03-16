import sqlite3
import random
from enum import Enum, unique


# rootList = [942858979, 914349145]
# rootList = [942858979]
pokeNameEng = ['xiaolada', 'bobo', 'miaomiao', 'wasidan', 'apashe',
               'dashetou', 'pikaqiu', 'pipi', 'pangding', 'yibu', 'jilidan', 'dailong', 'menghuan']
# pokeName = zip(pokeName_database, pokeName_chinese)

pokeNameChn = ['小拉达', '波波', '喵喵', '瓦斯弹', '阿柏蛇',
               '大舌头', '皮卡丘', '皮皮', '胖丁', '伊布', '吉利蛋', '袋龙', '梦幻']

ballName = {'evelsBall': '精灵球', 'superBall': '超级球', 'masterBall': '大师球'}
GameList = {}


def getImage(name: str) -> str:
    return '[CQ:image,file=kululu\%s.png]' % name


def getBallEmoji(name: str) -> str:
    if name == 'evelsBall':
        return '[CQ:emoji, id=9917]'
    elif name == 'superBall':
        return '[CQ:emoji, id=9918]'
    else:
        return '[CQ:emoji, id=127936]'


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
    NULL = 4


class Pokemon():
    def __init__(self, QQ: int):
        self.QQ = QQ
        self.reset()

    def reset(self):
        self.state = State.init
        self.pokemonIndex = -1

    def begin(self) -> str:
        if self.state is not State.init:
            return '你已经在游戏中了，快回复选项继续游戏吧。'
        self.state = State.scene
        return '欢迎来到宝可梦的世界，请选择你需要探索的地点:\nA.精灵乐园\nB.海底遗迹\nC.无尽森林\nD.精灵联盟'

    def next(self, choice: Choice = Choice.NULL) -> str:
        if self.state is State.scene:
            return self._dealScene(choice)
        elif self.state is State.catch:
            return self._dealCatch(choice)
        else:
            return '请重新开始游戏。'

    def _dealScene(self, choice: Choice) -> str:
        if self._getDiamond() < 10:
            return '对不起，你的钻石余额不足10，快找老蛋充值吧。'
        self._subDiamond()
        if choice is Choice.A:
            # 更新状态
            self.state = State.catch
            # 随机精灵宝可梦
            self.pokemonIndex = self._getSenceAPokemon()
            # 获得宝可梦的姓名，精灵球的数目。
            pokemonName = self._getPokemonNameChn()
            evelsBallNum = self._getBallNum('evelsBall')
            superBallNum = self._getBallNum('superBall')
            masterBallNum = self._getBallNum('masterBall')
            return '%s\n野生的%s出现了，接下来你要做什么？\nA.%s精灵球（%d个）\nB.%s超级球（%d个）\nC.%s大师球（%d个）\nD.%s逃跑' % \
                (getImage(self._getPokemonNameEng), pokemonName, getBallEmoji('evelsBall'), evelsBallNum, getBallEmoji(
                    'superBall'), superBallNum, getBallEmoji('asterBall'), masterBallNum, '[CQ:emoji, id=127939]')
        else:
            return '对不起，当前只开放了场景A.精灵乐园，请您重新选择'

    def _dealCatch(self, choice: Choice) -> str:
        temp = {Choice.A: 'evelsBall',
                Choice.B: 'superBall', Choice.C: 'masterBall'}
        if choice not in temp:
            self.reset()
            return '逃跑成功。'
        name = temp[choice]
        ballNum = self._getBallNum(name)
        if ballNum <= 0:
            return '对不起，你没有足够的%s,请重新选择。' % ballName[name]
        # 消耗对应精灵球
        self._subBallNum(name)
        # TODO：捕捉
        pokemonName = self._getPokemonNameChn()
        if False:  # TODO:如果捕捉到
            self.reset()
            return '%s\n恭喜你获得了可爱的%s，快打开宠物看看吧。' % (getImage(self._getPokemonNameEng), pokemonName)
        else:
            if False:  # TODO：宝可梦没有逃跑
                evelsBallNum = self._getBallNum('evelsBall')
                superBallNum = self._getBallNum('superBall')
                masterBallNum = self._getBallNum('masterBall')
                return '很可惜，%s捕捉失败，请再试一次吧。\n%s\nA.%s精灵球（%d个）\nB.%s超级球（%d个）\nC.%s大师球（%d个）\nD.%s逃跑' % \
                    (pokemonName, getImage(self._getPokemonNameEng), getBallEmoji('evelsBall'), evelsBallNum, getBallEmoji(
                        'superBall'), superBallNum, getBallEmoji('asterBall'), masterBallNum, '[CQ:emoji, id=127939]')

            else:
                self.reset()
                return '很可惜，%s可恶的逃跑了，再进入游戏寻找你的伙伴吧。' % pokemonName

    def _getSenceAPokemon(self) -> int:
        prob = [0.19, 0.19, 0.1, 0.1, 0.1, 0.07999,
                0.05, 0.05, 0.05, 0.05, 0.02, 0.02, 0.00001]
        x = random.uniform(0, 1)
        cumprob = 0.0
        for item, item_pro in zip(pokeNameEng, prob):
            cumprob += item_pro
            if x < cumprob:
                break
        return pokeNameEng.index(item)

    def _getDiamond(self) -> int:
        conn = sqlite3.connect('user.db')
        c = conn.cursor()
        c.execute("select Diamond from user where QQ=" + str(self.QQ))
        num = c.fetchone()[0]
        conn.close()
        return num

    def _subDiamond(self, value: int = 10) -> None:
        conn = sqlite3.connect('user.db')
        c = conn.cursor()
        c.execute("UPDATE user set Diamond = Diamond-" +
                  str(value)+" where QQ=" + str(self.QQ))
        conn.commit()
        conn.close()

    def _getState(self) -> State:
        if not self.state:
            self.state = State.init
        return self.state

    def _getPokemonNameChn(self) -> str:
        return pokeNameChn[self.pokemonIndex]

    def _getPokemonNameEng(self) -> str:
        return pokeNameEng[self.pokemonIndex]

    def _getBallNum(self, ball: str) -> int:
        conn = sqlite3.connect('user.db')
        c = conn.cursor()
        c.execute("select %s from pokemon where QQ=%d" % (ball, self.QQ))
        ans = c.fetchone()[0]
        conn.close()
        return ans

    def _subBallNum(self, ball: str, value: int = 1) -> None:
        conn = sqlite3.connect('user.db')
        c = conn.cursor()
        c.execute("UPDATE pokemon set %s = %s-%d where QQ=%d" %
                  (ball, ball, value, self.QQ))
        conn.commit()
        conn.close()
