import sqlite3
import random
import sys
import os
import json

sys.path.append(os.path.join('plugins', 'pokemon'))
from header import State, Choice, PokeLevel, ballEng2Chn, ballChn2Eng, allPokemon, pokeNameChn2Eng, consNameChn2Eng
import sceneA, sceneB
Scenes = {Choice.A: sceneA, Choice.B: sceneB}

DEBUG = False


def getImage(name: str) -> str:
    return '[CQ:image,file=kululu\%s.png]' % name


def getBallEmoji(name: str) -> str:
    if name == 'evelsBall':
        return '[CQ:emoji, id=9917]'
    elif name == 'superBall':
        return '[CQ:emoji, id=9918]'
    else:
        return '[CQ:emoji, id=127936]'


def getPokeLevel(name: str) -> PokeLevel:
    if name in allPokemon:
        return allPokemon[name]
    else:
        return PokeLevel.S


class Reward():
    def __init__(self):
        self.jsonPath = 'reward.json'
        self.loadData()

    def loadData(self):
        if os.path.exists(self.jsonPath):
            with open(self.jsonPath, encoding='utf-8') as f:
                self.allReward = json.load(f)
                self.nextID = max([x['id'] for x in self.allReward]) + \
                    1 if self.allReward != [] else 1024
        else:
            self.allReward = []
            self.nextID = 1024

    def saveData(self):
        with open(self.jsonPath, 'w', encoding='utf-8') as f:
            json.dump(self.allReward, f, indent=4, ensure_ascii=False)

    def postReward(self, reward: {}) -> int:
        ''':reward: {'group_id': int,
                    'pokemon': [[name,num],],
                    'award': [[name,num],],
                    'limitNum': int,
                    'remard': str}'''
        reward['id'] = self.nextID
        reward['getList'] = []
        self.nextID = self.nextID + 1
        self.allReward.append(reward)
        self.saveData()
        return reward['id']

    def meetReward(self, QQ: int, group_id: int, id: int) -> bool:
        if DEBUG:
            return True
        if self.allReward == []:
            return False
        for reward in self.allReward:
            if reward['id'] == id:
                break

        if reward['id'] != id or len(reward['getList']) >= reward['limitNum'] or QQ in reward['getList'] or reward[
                'group_id'] != group_id:
            return False

        conn = sqlite3.connect('user.db')
        c = conn.cursor()
        nameList = [pokeNameChn2Eng[x[0]] for x in reward['pokemon']]
        c.execute(f"select {','.join(nameList)} from pokemon where QQ={QQ}")
        num = c.fetchone()
        conn.close()
        return all([reward['pokemon'][i][1] <= num[i] for i in range(len(num))])

    def getReward(self, QQ: int, id: int) -> None:
        for reward in self.allReward:
            if reward['id'] == id:
                break
        conn = sqlite3.connect('user.db')
        c = conn.cursor()
        nameList = [
            f"{pokeNameChn2Eng[x[0]]}={pokeNameChn2Eng[x[0]]}-{x[1]}" for x in reward['pokemon']]
        c.execute(f"UPDATE pokemon set {','.join(nameList)} where QQ={QQ}")
        for x in reward['award']:
            if x[0] in pokeNameChn2Eng:
                name = pokeNameChn2Eng[x[0]]
                c.execute(
                    f"UPDATE pokemon set {name}={name}+{x[1]} where QQ={QQ}")
            elif x[0] == '奖券':
                c.execute(
                    f"UPDATE user set ticket = ticket+ {x[1]} where QQ={QQ}")
            elif x[0] == '钻石':
                c.execute(
                    f"UPDATE user set diamond = diamond+ {x[1]} where QQ={QQ}")
            elif x[0] == '积分':
                c.execute(
                    f"UPDATE user set score = score+ {x[1]} where QQ={QQ}")
            elif x[0] in ballChn2Eng:
                name = ballChn2Eng[x[0]]
                c.execute(
                    f"UPDATE pokemon set {name} = {name}+ {x[1]} where QQ={QQ}")
            elif x[0] in consNameChn2Eng:
                name = consNameChn2Eng[x[0]]
                c.execute(
                    f"UPDATE constellation set {name} = {name}+ {x[1]} where QQ={QQ}")
        conn.commit()
        conn.close()
        reward['getList'].append(QQ)
        if len(reward['getList']) == reward['limitNum']:
            self.allReward.remove(reward)
        self.saveData()

    def echoReward(self, group_id: int) -> []:
        return [x for x in self.allReward if x['group_id'] == group_id]

    def endReward(self, id: int, group_id: int):
        for reward in self.allReward:
            if reward['id'] == id:
                break
        if reward['id'] != id or reward['group_id'] != group_id:
            return False
        self.allReward.remove(reward)
        self.saveData()
        return True


class Pokemon():
    def __init__(self, QQ: int):
        self.QQ = QQ
        self.reset()
        self.sceneMsg = '欢迎来到宝可梦的世界，请选择你需要探索的地点:\n'+'\n'.join([
            f"{choice.name}.{scene.name}（{scene.enterCost}钻石/次）" for choice, scene in Scenes.items()])
        self.sceneErrorMsg = '对不起，当前只开放了场景\n'+''.join([
            f"{choice.name}.{scene.name}（{scene.enterCost}钻石/次）\n" for choice, scene in Scenes.items()]) + '请您重新选择。'

    def reset(self):
        self.state = State.init
        self.PokemonNameEng = ''
        self.PokemonNameChn = ''
        self.pokemonLevel = ''
        self.pokemonNum = 0
        self.currentScene = None

    def begin(self) -> str:
        if self.state is not State.init:
            return '你已经在游戏中了，快回复选项继续游戏吧。'
        self.state = State.scene
        return self.sceneMsg

    def next(self, choice: Choice) -> str:
        if self.state is State.scene:
            return self._dealScene(choice)
        elif self.state is State.catch:
            return self._dealCatch(choice)
        else:
            return '请重新开始游戏。'

    def _dealScene(self, choice: Choice) -> str:
        if choice not in Scenes:
            return self.sceneErrorMsg
        cost = Scenes[choice].enterCost
        if self._diamondNum < cost:
            return f'对不起，你的钻石余额不足{cost}，快找老蛋充值吧。'
        self._subDiamond(cost)
        self.state = State.catch
        self._getScenePokemon(choice)
        self.currentScene = choice
        # 获得宝可梦的姓名，精灵球的数目。
        evelsBallNum = self._getBallNum('evelsBall')
        superBallNum = self._getBallNum('superBall')
        masterBallNum = self._getBallNum('masterBall')
        return "%s\n野生的%s [%s级,您有%d只] 出现了，接下来你要做什么？\nA.%s精灵球（%d个）\nB.%s超级球（%d个）\nC.%s大师球（%d个）\nD.%s逃跑" % \
               (self._pokemonImage, self.pokemonNameChn, self.pokemonLevel, self.pokemonNum, getBallEmoji('evelsBall'),
                evelsBallNum,
                getBallEmoji(
                    'superBall'), superBallNum, getBallEmoji('asterBall'), masterBallNum, '[CQ:emoji, id=127939]')

    def _dealCatch(self, choice: Choice) -> str:
        temp = {Choice.A: 'evelsBall',
                Choice.B: 'superBall', Choice.C: 'masterBall'}
        if choice not in temp:
            self.reset()
            return '逃跑成功。'
        name = temp[choice]
        ballNum = self._getBallNum(name)
        if ballNum <= 0:
            return f'对不起，你没有足够的{ballEng2Chn[name]},请重新选择。'
        # 消耗对应精灵球
        self._subBallNum(name)
        # 开始捕捉
        catchProb = self._getSceneCatchProb(name, self.currentScene)
        escapeProb = self._getSceneEscapeProb(self.currentScene)
        if random.uniform(0, 1) <= catchProb:
            # 如果捕捉到
            message = f'{self._pokemonImage}\n恭喜你获得了可爱的{self.pokemonNameChn}，快打开宠物看看吧。'
            self._addPokemon(self.pokemonNameEng)
            self.reset()
            return message
        else:
            if random.uniform(0, 1) <= escapeProb:
                # 宝可梦逃跑
                message = f'很可惜，{self.pokemonNameChn}可恶的逃跑了，再进入游戏寻找你的伙伴吧。'
                self.reset()
                return message
            else:
                # 宝可梦没有逃跑
                evelsBallNum = self._getBallNum('evelsBall')
                superBallNum = self._getBallNum('superBall')
                masterBallNum = self._getBallNum('masterBall')
                return '%s\n很可惜，%s [%s级,您有%d只] 捕捉失败，请再试一次吧。\nA.%s精灵球（%d个）\nB.%s超级球（%d个）\nC.%s大师球（%d个）\nD.%s逃跑' % \
                       (self._pokemonImage, self.pokemonNameChn, self.pokemonLevel, self.pokemonNum,
                        getBallEmoji('evelsBall'), evelsBallNum,
                        getBallEmoji(
                            'superBall'), superBallNum, getBallEmoji('asterBall'), masterBallNum,
                        '[CQ:emoji, id=127939]')

    def _getSceneCatchProb(self, ball: str, choice: Choice) -> float:
        return Scenes[choice].catchProb[getPokeLevel(self.pokemonNameEng)][ball]

    def _getSceneEscapeProb(self, choice: Choice) -> float:
        return Scenes[choice].escapeProb[getPokeLevel(self.pokemonNameEng)]

    def _getScenePokemon(self, choice: Choice) -> None:
        scene = Scenes[choice]
        prob = scene.pokemonProb
        x = random.uniform(0, 1)
        cumprob = 0.0
        for item, item_pro in zip(sceneA.pokeNameEng, prob):
            cumprob += item_pro
            if x < cumprob:
                break
        self.pokemonNameEng = item
        self.pokemonNameChn = sceneA.pokeNameChn[sceneA.pokeNameEng.index(
            item)]
        self.pokemonLevel = allPokemon[item].name
        self.pokemonNum = self._getPokeNum

    @property
    def _pokemonImage(self) -> str:
        return getImage(self.pokemonNameEng)

    @property
    def _diamondNum(self) -> int:
        if DEBUG:
            return 1000
        conn = sqlite3.connect('user.db')
        c = conn.cursor()
        c.execute("select Diamond from user where QQ=" + str(self.QQ))
        num = c.fetchone()[0]
        conn.close()
        return num

    def _subDiamond(self, value: int = 10) -> None:
        if DEBUG:
            return
        conn = sqlite3.connect('user.db')
        c = conn.cursor()
        c.execute(
            "UPDATE user set Diamond = Diamond-{0} where QQ={1}".format(str(value), str(self.QQ)))
        conn.commit()
        conn.close()

    @property
    def _state(self) -> State:
        if not self.state:
            self.state = State.init
        return self.state

    def _getBallNum(self, ball: str) -> int:
        if DEBUG:
            return 1000
        conn = sqlite3.connect('user.db')
        c = conn.cursor()
        c.execute("select %s from pokemon where QQ=%d" % (ball, self.QQ))
        ans = c.fetchone()[0]
        conn.close()
        return ans

    @property
    def _getPokeNum(self) -> int:
        if DEBUG:
            return 1000
        conn = sqlite3.connect('user.db')
        c = conn.cursor()
        c.execute("select %s from pokemon where QQ=%d" %
                  (self.pokemonNameEng, self.QQ))
        ans = c.fetchone()[0]
        conn.close()
        return ans

    def _subBallNum(self, ball: str, value: int = 1) -> None:
        if DEBUG:
            return
        conn = sqlite3.connect('user.db')
        c = conn.cursor()
        c.execute("UPDATE pokemon set %s = %s-%d where QQ=%d" %
                  (ball, ball, value, self.QQ))
        conn.commit()
        conn.close()

    def _addPokemon(self, name: str, value: int = 1) -> None:
        if DEBUG:
            return
        conn = sqlite3.connect('user.db')
        c = conn.cursor()
        c.execute("UPDATE pokemon set %s = %s+%d where QQ=%d" %
                  (name, name, value, self.QQ))
        conn.commit()
        conn.close()


if __name__ == "__main__":
    DEBUG = True
    game = Pokemon(123)
    print(game.begin())
    print(game.next(Choice.B))
    print(game.next(Choice.C))
    print(game.next(Choice.A))
    # print(game.next(Choice.B))
    print(game.next(Choice.C))
    print(game.begin())
    print(game.next(Choice.A))
    # print(game.next(Choice.A))
    # print(game.next(Choice.A))
    print(game.next(Choice.D))
    for i in allPokemon:
        print(i)
