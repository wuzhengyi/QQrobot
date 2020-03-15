import sqlite3
import random

rootList = [942858979, 914349145]


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
            self.c.execute("INSERT INTO common (signDate) VALUES (date('now'))")
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
        self.c.execute("UPDATE common set signnum = signnum+1 where signdate=date('now')")
        self.c.execute("UPDATE user set sign = 1 where QQ=" + str(QQ))
        self.c.execute("select signnum from common where signdate=date('now')")
        ans = self.c.fetchone()
        return ans[0]

    def getScore(self, QQ: int) -> int:
        self.c.execute("select SCORE from user where QQ=" + str(QQ))
        ans = self.c.fetchall()
        return ans[0][0]

    def getTicket(self, QQ: int) -> int:
        self.c.execute("select Ticket from user where QQ=" + str(QQ))
        ans = self.c.fetchall()
        return ans[0][0]

    def getDiamond(self, QQ: int) -> int:
        self.c.execute("select Diamond from user where QQ=" + str(QQ))
        ans = self.c.fetchall()
        return ans[0][0]

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

    def resetScore(self):
        self.c.execute("UPDATE user set Score = 0")

    def resetTicket(self):
        self.c.execute("UPDATE user set Ticket = 0")

    def resetDiamond(self):
        self.c.execute("UPDATE user set Diamond = 0")

    def close(self):
        self.conn.commit()
        self.conn.close()
