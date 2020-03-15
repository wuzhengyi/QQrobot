import nonebot
from nonebot import on_command, CommandSession
from .data_source import userSQL, getRandom, isRoot
from os import path

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
