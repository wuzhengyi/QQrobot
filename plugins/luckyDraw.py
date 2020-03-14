import nonebot
from nonebot import on_command, CommandSession
from os import path
import sqlite3
import random

seq = [1350, 710, 288, 50, 30, 20, 10, 8, 5]
prob = [0.0001, 0.002, 0.0109, 0.03, 0.06, 0.327, 0.46, 0.1, 0.01]
rootList = [942858979, 914349145]

# on_command 装饰器将函数声明为一个命令处理器
# 这里 luckyDraw 为命令的名字
@on_command('抽奖', only_to_me=False)
async def luckyDraw(session: CommandSession):
    QQ = session.ctx['user_id']
    user = userSQL()
    score = user.getScore(QQ)
    if score >= 20:
        item = getRandom()
        user.subScore(QQ, 20)
        user.addScore(QQ, item)
        await session.send('恭喜您获得'+str(item)+'积分奖励，您当前的积分余额为'+str(score-20+item)+'，欢迎下次光临。')
    else:
        await session.send('您的积分不足20，快去找老蛋赚积分吧。')
    user.close()

@on_command('五连', only_to_me=False)
async def luckyDraw2(session: CommandSession):
    QQ = session.ctx['user_id']
    user = userSQL()
    score = user.getScore(QQ)
    if score >= 100:
        items = [getRandom() for i in range(5)]
        user.subScore(QQ, 100)
        user.addScore(QQ, sum(items))
        await session.send('恭喜您获得'+' '.join([str(j) for j in items]) +'积分奖励，您当前的积分余额为'+str(score-100+sum(items))+'，欢迎下次光临。')
    else:
        await session.send('您的积分不足100，快去找老蛋赚积分吧。')
    user.close()

@on_command('奖券榜', only_to_me=False)
async def TopTicket(session: CommandSession):
    QQ = session.ctx['user_id']
    if not isRoot(QQ):
        return
    user = userSQL()
    rank = user.getTopTicket()
    user.close()
    # await session.send(str(rank))
    bot = nonebot.get_bot()
    QQname = []
    for QQ in rank:
        group_member_info = await bot.get_group_member_info(group_id=session.ctx['group_id'], user_id=QQ[0], no_cache=True)
        QQname.append(group_member_info['card'])
        if len(QQname) > 5:
            break
    message = '奖券排行榜\n' + ''.join(['Top '+str(i+1)+'. '+QQname[i]+'\t '+str(rank[i][1])+'\n' for i in range(len(QQname))])
    await session.send(message)

@on_command('积分榜', only_to_me=False)
async def TopScore(session: CommandSession):
    QQ = session.ctx['user_id']
    if not isRoot(QQ):
        return
    user = userSQL()
    rank = user.getTopScore()
    user.close()
    bot = nonebot.get_bot()
    QQname = []
    for QQ in rank:
        group_member_info = await bot.get_group_member_info(group_id=session.ctx['group_id'], user_id=QQ[0], no_cache=True)
        QQname.append(group_member_info['card'])
        if len(QQname) > 5:
            break
    message = '积分排行榜\n' + ''.join(['Top '+str(i+1)+'. '+QQname[i]+'\t '+str(rank[i][1])+'\n' for i in range(len(QQname))])
    await session.send(message)

def getRandom() -> int:
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