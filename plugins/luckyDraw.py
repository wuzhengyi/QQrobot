from nonebot import on_command, CommandSession
from os import path
import sqlite3
import random

seq = [1350, 710, 288, 50, 30, 20, 10, 8, 5]
prob = [0.0001, 0.002, 0.0109, 0.03, 0.06, 0.327, 0.46, 0.1, 0.01]

# on_command 装饰器将函数声明为一个命令处理器
# 这里 luckyDraw 为命令的名字
@on_command('抽奖', only_to_me=False)
async def luckyDraw(session: CommandSession):
    QQ = session.ctx['user_id']
    conn = sqlite3.connect('E:\\酷Q Air\\data\\app\\top.zls520.jf\\user.db')
    print("Opened database successfully")
    c = conn.cursor()
    temp = c.execute("select jf from user where QQ=" + str(QQ))
    for row in temp:
        jf = int(row[0])
        if jf >= 20:
            # TODO：抽奖
            item = getRandom()
            c.execute("UPDATE user set jf = jf-20 where QQ=" + str(QQ))
            c.execute("UPDATE user set jf = jf+" +
                      str(item)+" where QQ=" + str(QQ))
            conn.commit()
            await session.send('恭喜您获得'+str(item)+'积分奖励，您当前的积分余额为'+str(jf-20+item)+'，欢迎下次光临。')
        else:
            await session.send('您的积分不足20，快去找老蛋赚积分吧。')

    conn.close()

@on_command('五连', only_to_me=False)
async def luckyDraw2(session: CommandSession):
    QQ = session.ctx['user_id']
    conn = sqlite3.connect('E:\\酷Q Air\\data\\app\\top.zls520.jf\\user.db')
    print("Opened database successfully")
    c = conn.cursor()
    temp = c.execute("select jf from user where QQ=" + str(QQ))
    for row in temp:
        jf = int(row[0])
        if jf >= 100:
            items = [getRandom() for i in range(5)]
            c.execute("UPDATE user set jf = jf-100 where QQ=" + str(QQ))
            c.execute("UPDATE user set jf = jf+" +
                      str(sum(items))+" where QQ=" + str(QQ))
            conn.commit()
            await session.send('恭喜您获得'+' '.join(items) +'积分奖励，您当前的积分余额为'+str(jf-100+sum(items))+'，欢迎下次光临。')
        else:
            await session.send('您的积分不足100，快去找老蛋赚积分吧。')

    conn.close()

def getRandom() -> int:
    x = random.uniform(0, 1)
    cumprob = 0.0
    for item, item_pro in zip(seq, prob):
        cumprob += item_pro
        if x < cumprob:
            break
    return item