import sqlite3
import random

rootList = [942858979, 914349145]
pokeName_database = ['xiaolada', 'bobo', 'miaomiao', 'wasidan', 'apashe',
                     'dashetou', 'pikaqiu', 'pipi', 'pangding', 'yibu', 'jilidan', 'dailong', 'menghuan']
# pokeName_chinese = ['小拉达', '波波', '喵喵', '瓦斯弹', '阿柏蛇',
#                     '大舌头', '皮卡丘', '皮皮', '胖丁', '伊布', '吉利蛋', '袋龙', '梦幻']
# pokeName = zip(pokeName_database, pokeName_chinese)

cons_database = ['Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo',
                 'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces']
# cons_chinese = ['白羊座', '金牛座', '双子座', '巨蟹座', '狮子座',
#                 '处女座', '天秤座', '天蝎座', '射手座', '摩羯座', '水瓶座', '双鱼座']
# consName = zip(cons_database, cons_chinese)

pokeName = ['小拉达', '波波', '喵喵', '瓦斯弹', '阿柏蛇',
            '大舌头', '皮卡丘', '皮皮', '胖丁', '伊布', '吉利蛋', '袋龙', '梦幻']
consName = ['白羊座', '金牛座', '双子座', '巨蟹座', '狮子座',
            '处女座', '天秤座', '天蝎座', '射手座', '摩羯座', '水瓶座', '双鱼座']

ballName = {'evelsBall': '精灵球', 'superBall': '超级球', 'masterBall': '大师球'}


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


class userSQL():
    def __init__(self):
        self.conn = sqlite3.connect('user.db')
        self.c = self.conn.cursor()

    def isExist(self, QQ: int) -> bool:
        self.c.execute("select * from user where QQ=" + str(QQ))
        ans = self.c.fetchall()
        if ans == []:
            return False
        return True

    def insert(self, QQ: int) -> None:
        self.c.execute("INSERT INTO USER (QQ) \
                        VALUES ("+str(QQ)+")")
        self.c.execute("INSERT INTO pokemon (QQ) \
                        VALUES ("+str(QQ)+")")
        self.c.execute("INSERT INTO constellation (QQ) \
                        VALUES ("+str(QQ)+")")

    def _isNewDate(self) -> bool:
        self.c.execute("select * from common where signdate=date('now')")
        ans = self.c.fetchall()
        if ans == []:
            self.c.execute(
                "INSERT INTO common (signDate) VALUES (date('now'))")
            self.c.execute("UPDATE user set sign = 0")
            return True
        return False

    def isSigned(self, QQ: int) -> bool:
        if self._isNewDate():
            return True
        self.c.execute("select sign from user where QQ=" + str(QQ))
        ans = self.c.fetchall()
        if ans == [] or ans[0][0] == 0:
            return False
        return True

    def sign(self, QQ: int) -> int:
        self.c.execute(
            "UPDATE common set signnum = signnum+1 where signdate=date('now')")
        self.c.execute("UPDATE user set sign = 1 where QQ=" + str(QQ))
        self.c.execute("select signnum from common where signdate=date('now')")
        ans = self.c.fetchone()
        return ans[0]

    def getScore(self, QQ: int) -> int:
        self.c.execute("select SCORE from user where QQ=" + str(QQ))
        ans = self.c.fetchone()
        return ans[0]

    def getTicket(self, QQ: int) -> int:
        self.c.execute("select Ticket from user where QQ=" + str(QQ))
        ans = self.c.fetchone()
        return ans[0]

    def getDiamond(self, QQ: int) -> int:
        self.c.execute("select Diamond from user where QQ=" + str(QQ))
        ans = self.c.fetchone()
        return ans[0]

    def getEvelsBall(self, QQ: int) -> int:
        self.c.execute("select evelsball from pokemon where QQ=" + str(QQ))
        ans = self.c.fetchone()
        return ans[0]

    def getSuperBall(self, QQ: int) -> int:
        self.c.execute("select Superball from pokemon where QQ=" + str(QQ))
        ans = self.c.fetchone()
        return ans[0]

    def getMasterBall(self, QQ: int) -> int:
        self.c.execute("select Masterball from pokemon where QQ=" + str(QQ))
        ans = self.c.fetchone()
        return ans[0]

    def getPokemon(self, QQ: int) -> tuple:
        self.c.execute("select * from pokemon where QQ=" + str(QQ))
        ans = self.c.fetchone()
        return ans[4:]

    def getConstellation(self, QQ: int) -> tuple:
        self.c.execute("select * from Constellation where QQ=" + str(QQ))
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

    def subScore(self, QQ: int, value: int) -> None:
        self.c.execute("UPDATE user set SCORE = SCORE-" +
                       str(value)+" where QQ=" + str(QQ))

    def addScore(self, QQ: int, value: int) -> None:
        self.c.execute("UPDATE user set SCORE = SCORE+" +
                       str(value)+" where QQ=" + str(QQ))

    def subTicket(self, QQ: int, value: int) -> None:
        self.c.execute("UPDATE user set ticket = ticket-" +
                       str(value)+" where QQ=" + str(QQ))

    def addTicket(self, QQ: int, value: int) -> None:
        self.c.execute("UPDATE user set ticket = ticket+" +
                       str(value)+" where QQ=" + str(QQ))

    def subDiamond(self, QQ: int, value: int) -> None:
        self.c.execute("UPDATE user set Diamond = Diamond-" +
                       str(value)+" where QQ=" + str(QQ))

    def addDiamond(self, QQ: int, value: int) -> None:
        self.c.execute("UPDATE user set Diamond = Diamond+" +
                       str(value)+" where QQ=" + str(QQ))

    def addCons(self, QQ: int, index: int) -> None:
        self.c.execute("UPDATE Constellation set " +
                       cons_database[index]+"="+cons_database[index]+"+1 where QQ=" + str(QQ))

    def addBall(self, QQ: int, ball: str) -> None:
        self.c.execute("UPDATE pokemon set " + ball +
                       "="+ball+"+1 where QQ=" + str(QQ))

    def addEvelsBall(self, QQ: int, value: int) -> None:
        self.c.execute("UPDATE pokemon set EvelsBall = EvelsBall+" +
                       str(value)+" where QQ=" + str(QQ))

    def addSuperBall(self, QQ: int, value: int) -> None:
        self.c.execute("UPDATE pokemon set SuperBall = SuperBall+" +
                       str(value)+" where QQ=" + str(QQ))

    def addMasterBall(self, QQ: int, value: int) -> None:
        self.c.execute("UPDATE pokemon set MasterBall = MasterBall+" +
                       str(value)+" where QQ=" + str(QQ))

    def resetScore(self):
        self.c.execute("UPDATE user set Score = 0")

    def resetTicket(self):
        self.c.execute("UPDATE user set Ticket = 0")

    def resetDiamond(self):
        self.c.execute("UPDATE user set Diamond = 0")

    def close(self):
        self.conn.commit()
        self.conn.close()
