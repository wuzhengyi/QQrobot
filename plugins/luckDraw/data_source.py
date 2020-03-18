import sqlite3
import random
from ..pokemon.header import pokeNameEng, pokeNameChn2Eng, ballEng2Chn, ballChn2Eng

# rootList = [942858979, 914349145]
rootList = [942858979]

consName = ['白羊座', '金牛座', '双子座', '巨蟹座', '狮子座',
            '处女座', '天秤座', '天蝎座', '射手座', '摩羯座', '水瓶座', '双鱼座']
cons_database = ['Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo',
                 'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces']
consNameCov = dict(zip(consName, cons_database))


def getScoreDrawRandom() -> int:
    seq = [1350, 710, 288, 50, 30, 20, 10, 8, 5, 0]
    prob = [0.0001, 0.002, 0.0109, 0.03, 0.06, 0.227, 0.46, 0.1, 0.01, 0.1]
    x = random.uniform(0, 1)
    cumprob = 0.0
    for item, item_pro in zip(seq, prob):
        cumprob += item_pro
        if x < cumprob:
            break
    return item


def getDiamonDrawRandom() -> int:
    seq = ['evelsBall', 'superBall', 'masterBall',
           '30', '60', '120', '300', 'card', 'ticket']
    prob = [0.49999, 0.24, 0.012, 0.08, 0.06, 0.04, 0.02, 0.048, 0.00001]
    x = random.uniform(0, 1)
    cumprob = 0.0
    for item, item_pro in zip(seq, prob):
        cumprob += item_pro
        if x < cumprob:
            break
    return item


def isRoot(QQ: int) -> bool:
    return QQ in rootList


def getImage(name: str) -> str:
    if name in cons_database:
        return getConsImage(cons_database.index(name))
    elif name in ballEng2Chn:
        return getBallImage(name)
    else:
        return '[CQ:image,file=kululu\%s.png]' % name


def getBallEmoji(name: str) -> str:
    if name == 'evelsBall':
        return '[CQ:emoji, id=9917]'
    elif name == 'superBall':
        return '[CQ:emoji, id=9918]'
    else:
        return '[CQ:emoji, id=127936]'


def getBallImage(name: str) -> str:
    return '[CQ:image,file=kululu\%s.png]' % name


def getConsEmoji(index: int) -> str:
    return '[CQ:emoji, id=%d]' % (index + 9800)


def getConsImage(index: int) -> str:
    return '[CQ:image,file=kululu\%s.jpg]' % cons_database[index]


class userSQL():
    def __init__(self):
        self.conn = sqlite3.connect('user.db')
        self.c = self.conn.cursor()

    def isExist(self, QQ: int) -> bool:
        self.c.execute(f"select * from user where QQ= {QQ}")
        ans = self.c.fetchall()
        if ans == []:
            return False
        return True

    def insert(self, QQ: int) -> None:
        self.c.execute("INSERT INTO USER (QQ) \
                        VALUES (" + str(QQ) + ")")
        self.c.execute("INSERT INTO pokemon (QQ) \
                        VALUES (" + str(QQ) + ")")
        self.c.execute("INSERT INTO constellation (QQ) \
                        VALUES (" + str(QQ) + ")")

    def _isNewDate(self) -> bool:
        self.c.execute("select * from common where signdate=date('now')")
        ans = self.c.fetchall()
        if ans == []:
            self.c.execute(
                "INSERT INTO common (signDate) VALUES (date('now'))")
            self.c.execute("UPDATE user set sign = 0, messageNum=0")
            return True
        return False

    def isSigned(self, QQ: int) -> bool:
        if self._isNewDate():
            return True
        self.c.execute(f"select sign from user where QQ= {QQ}")
        ans = self.c.fetchall()
        if ans == [] or ans[0][0] == 0:
            return False
        return True

    def sign(self, QQ: int) -> int:
        self.c.execute(
            "UPDATE common set signnum = signnum+1 where signdate=date('now')")
        self.c.execute(f"UPDATE user set sign = 1 where QQ= {QQ}")
        self.c.execute("select signnum from common where signdate=date('now')")
        ans = self.c.fetchone()
        return ans[0]

    def getScore(self, QQ: int) -> int:
        self.c.execute(f"select SCORE from user where QQ={QQ}")
        ans = self.c.fetchone()
        return ans[0]

    def getTicket(self, QQ: int) -> int:
        self.c.execute(f"select Ticket from user where QQ={QQ}")
        ans = self.c.fetchone()
        return ans[0]

    def getDiamond(self, QQ: int) -> int:
        self.c.execute(f"select Diamond from user where QQ={QQ}")
        ans = self.c.fetchone()
        return ans[0]

    def getEvelsBall(self, QQ: int) -> int:
        self.c.execute(f"select evelsball from pokemon where QQ={QQ}")
        ans = self.c.fetchone()
        return ans[0]

    def getSuperBall(self, QQ: int) -> int:
        self.c.execute(f"select Superball from pokemon where QQ={QQ}")
        ans = self.c.fetchone()
        return ans[0]

    def getMasterBall(self, QQ: int) -> int:
        self.c.execute(f"select Masterball from pokemon where QQ={QQ}")
        ans = self.c.fetchone()
        return ans[0]

    def getPokemon(self, QQ: int) -> tuple:
        self.c.execute(
            f"select {','.join(pokeNameEng)} from pokemon where QQ={QQ}")
        ans = self.c.fetchone()
        return ans

    def getConstellation(self, QQ: int) -> tuple:
        self.c.execute(f"select * from Constellation where QQ={QQ}")
        ans = self.c.fetchone()
        return ans[1:]

    def getTopTicket(self) -> [(int, int)]:
        self.c.execute("select QQ, Ticket from user ORDER BY TICKET DESC")
        ans = self.c.fetchall()
        return ans

    def getTopScore(self) -> [(int, int)]:
        self.c.execute("select QQ, SCORE from user ORDER BY SCORE DESC")
        ans = self.c.fetchall()
        return ans

    def getTopDiamond(self) -> [(int, int)]:
        self.c.execute("select QQ, Diamond from user ORDER BY Diamond DESC")
        ans = self.c.fetchall()
        return ans

    def getTopMessage(self) -> [(int, int)]:
        self.c.execute("select QQ, messageNum from user ORDER BY messageNum DESC")
        ans = self.c.fetchall()
        return ans

    def getMessageNum(self, QQ: int) -> int:
        self.c.execute(f"select messageNum from user where QQ={QQ}")
        ans = self.c.fetchone()
        return ans[0]

    def addMessageNum(self, QQ: int, value: int = 1) -> None:
        self.c.execute(
            f"UPDATE user set messageNum = messageNum+{value} where QQ={QQ}")

    def subScore(self, QQ: int, value: int) -> None:
        self.c.execute(f"UPDATE user set SCORE = SCORE-{value} where QQ={QQ}")

    def addScore(self, QQ: int, value: int) -> None:
        self.c.execute(f"UPDATE user set SCORE = SCORE+{value} where QQ={QQ}")

    def subTicket(self, QQ: int, value: int) -> None:
        self.c.execute(
            f"UPDATE user set ticket = ticket-{value} where QQ={QQ}")

    def addTicket(self, QQ: int, value: int) -> None:
        self.c.execute(
            f"UPDATE user set ticket = ticket-{value} where QQ={QQ}")

    def subDiamond(self, QQ: int, value: int) -> None:
        self.c.execute(
            f"UPDATE user set Diamond = Diamond-{value} where QQ={QQ}")

    def addDiamond(self, QQ: int, value: int) -> None:
        self.c.execute(
            f"UPDATE user set Diamond = Diamond+{value} where QQ={QQ}")

    def addAllDiamond(self, value: int) -> None:
        self.c.execute(f"UPDATE user set Diamond = Diamond+{value}")

    def addCons(self, QQ: int, index: int, value: int = 1) -> None:
        self.c.execute(
            f"UPDATE Constellation set {cons_database[index]}={cons_database[index]}+{value} where QQ= +{QQ}")

    def addBall(self, QQ: int, ball: str, value: int = 1) -> None:
        self.c.execute("UPDATE pokemon set %s=%s+%d where QQ=%d" %
                       (ball, ball, value, QQ))

    def addEvelsBall(self, QQ: int, value: int) -> None:
        self.c.execute(
            f"UPDATE pokemon set EvelsBall = EvelsBall+{value} where QQ={QQ}")

    def addSuperBall(self, QQ: int, value: int) -> None:
        self.c.execute(
            f"UPDATE pokemon set SuperBall = SuperBall+{value} where QQ={QQ}")

    def addMasterBall(self, QQ: int, value: int) -> None:
        self.c.execute(
            f"UPDATE pokemon set MasterBall = MasterBall+{value} where QQ={QQ}")

    def addItem(self, QQ: int, item: str, value: int) -> None:
        if item in ballChn2Eng:
            self.addBall(QQ, ballChn2Eng[item], value)
        elif item in pokeNameChn2Eng:
            self.c.execute("UPDATE pokemon set %s=%s+%d where QQ=%d" %
                           (pokeNameChn2Eng[item], pokeNameChn2Eng[item], value, QQ))
        elif item in consNameCov:
            self.c.execute("UPDATE Constellation set %s=%s+%d where QQ=%d" %
                           (consNameCov[item], consNameCov[item], value, QQ))

    def subItem(self, QQ: int, item: str, value: int) -> None:
        if item in ballChn2Eng:
            self.c.execute("UPDATE pokemon set %s=%s-%d where QQ=%d" %
                           (ballChn2Eng[item], ballChn2Eng[item], value, QQ))
        elif item in pokeNameChn2Eng:
            self.c.execute("UPDATE pokemon set %s=%s-%d where QQ=%d" %
                           (pokeNameChn2Eng[item], pokeNameChn2Eng[item], value, QQ))
        elif item in consNameCov:
            self.c.execute("UPDATE Constellation set %s=%s-%d where QQ=%d" %
                           (consNameCov[item], consNameCov[item], value, QQ))

    def resetScore(self):
        self.c.execute("UPDATE user set Score = 0")

    def resetTicket(self):
        self.c.execute("UPDATE user set Ticket = 0")

    def resetDiamond(self):
        self.c.execute("UPDATE user set Diamond = 0")

    def resetBackpack(self):
        self.resetCons()
        self.resetBall()

    def resetPokemon(self):
        self.c.execute(f"UPDATE pokemon SET {'=0,'.join(pokeNameEng)}=0")

    def resetCons(self):
        self.c.execute(
            f"UPDATE constellation SET {'=0,'.join(cons_database)}=0")

    def resetBall(self):
        self.c.execute(
            "UPDATE pokemon SET evelsBall=0, superBall=0, masterBall = 0")

    def close(self):
        self.conn.commit()
        self.conn.close()
