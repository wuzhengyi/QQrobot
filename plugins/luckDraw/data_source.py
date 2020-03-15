import sqlite3
import random

rootList = [942858979, 914349145]


def getRandom() -> int:
    seq = [1350, 710, 288, 50, 30, 20, 10, 8, 5]
    prob = [0.0001, 0.002, 0.0109, 0.03, 0.06, 0.327, 0.46, 0.1, 0.01]
    x = random.uniform(0, 1)
    cumprob = 0.0
    for item, item_pro in zip(seq, prob):
        cumprob += item_pro
        if x < cumprob:
            break
    return item

def isRoot(QQ:int) -> bool:
    return QQ in rootList

class userSQL():
    def __init__(self):
        self.conn = sqlite3.connect('E:\\酷Q Air\\data\\app\\top.zls520.jf\\user.db')
        self.c = self.conn.cursor()
        
    def isExist(self, QQ: int) -> bool:
        self.c.execute("select * from user where QQ=" + str(QQ))
        ans = self.c.fetchall()
        if ans == []:
            return False
        return True

    def insert(self, QQ: int) -> None:
        self.c.execute("INSERT INTO USER (QQ,JF,TICKET) \
                        VALUES ("+str(QQ)+", 0, 0)")

    def getScore(self, QQ: int) -> int:
        self.c.execute("select JF from user where QQ=" + str(QQ))
        ans = self.c.fetchall()
        if ans == []:
            self.insert(QQ)
            return 0
        return ans[0][0]
    
    def getTicket(self, QQ: int) -> int:
        self.c.execute("select Ticket from user where QQ=" + str(QQ))
        ans = self.c.fetchall()
        if ans == []:
            self.insert(QQ)
            return 0
        if ans[0][0] == None:
            self.c.execute("UPDATE user set ticket = 0 where ticket is null")
            return 0
        return ans[0][0]

    def getTopTicket(self) -> [(int, int)]:
        self.c.execute("UPDATE user set ticket = 0 where ticket is null")
        self.c.execute("select QQ, Ticket from user ORDER BY TICKET DESC")
        ans = self.c.fetchall()
        return ans

    def getTopScore(self) -> [(int, int)]:
        self.c.execute("UPDATE user set jf = 0 where jf is null")
        self.c.execute("select QQ, jf from user ORDER BY jf DESC")
        ans = self.c.fetchall()
        return ans

    def subScore(self, QQ:int, value:int) -> None:
        self.c.execute("UPDATE user set jf = jf-"+str(value)+" where QQ=" + str(QQ))
    
    def addScore(self, QQ:int, value:int) -> None:
        self.c.execute("UPDATE user set jf = jf+"+str(value)+" where QQ=" + str(QQ))

    def subTicket(self, QQ:int, value:int) -> None:
        self.getTicket(QQ)
        self.c.execute("UPDATE user set ticket = ticket-"+str(value)+" where QQ=" + str(QQ))
    
    def addTicket(self, QQ:int, value:int) -> None:
        self.getTicket(QQ)
        self.c.execute("UPDATE user set ticket = ticket+"+str(value)+" where QQ=" + str(QQ))

    def close(self):
        self.conn.commit()
        self.conn.close()