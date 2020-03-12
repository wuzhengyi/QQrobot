from nonebot import on_command, CommandSession
from os import path
import sqlite3
import random

# 以序列seq中值出现的概率来随机生成某个值


async def rand_pick(seq, probabilities):
    x = random.uniform(0, 1)
    cumprob = 0.0
    for item, item_pro in zip(seq, probabilities):
        cumprob += item_pro
        if x < cumprob:
            break
    return item
value_list = [0, 1]
probabilities = [0.4, 0.6]
print(rand_pick(value_list, probabilities))
# on_command 装饰器将函数声明为一个命令处理器
# 这里 luckyDraw 为命令的名字
@on_command('抽奖', only_to_me=False)
async def luckyDraw(session: CommandSession):
    # 获取城市的天气预报
    # luckyDraw_report = await get_luckyDraw_of_server(server)
    # 向用户发送天气预报
    QQ = session.ctx['user_id']
    conn = sqlite3.connect('E:\\酷Q Air\\data\\app\\top.zls520.jf\\user.db')
    print("Opened database successfully")
    c = conn.cursor()
    temp = c.execute("select jf from user where QQ=" + str(QQ))
    for row in temp:
        jf = int(row[0])
        print(row[0])
        if jf >= 20:
            # TODO：抽奖
            seq = [1350, 710, 288, 50, 30, 20, 10]
            prob = [0.0001, 0.0029, 0.01, 0.03, 0.05, 0.5, 0.407]
            x = random.uniform(0, 1)
            cumprob = 0.0
            for item, item_pro in zip(seq, prob):
                cumprob += item_pro
                if x < cumprob:
                    break
            c.execute("UPDATE user set jf = jf-20 where QQ=" + str(QQ))
            c.execute("UPDATE user set jf = jf+"+str(item)+" where QQ=" + str(QQ))
            conn.commit()
            await session.send('恭喜您获得'+str(item)+'积分奖励，您当前的积分余额为'+str(jf-20+item)+'，欢迎下次光临。')
        else:
            await session.send('您的积分不足20，快去找老蛋赚积分吧。')

    conn.close()
