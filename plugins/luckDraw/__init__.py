import nonebot
from nonebot import on_command, CommandSession
from .data_source import userSQL, getScoreDrawRandom, isRoot
from os import path
import random

# on_command 装饰器将函数声明为一个命令处理器
# 这里 luckyDraw 为命令的名字
@on_command('签到', only_to_me=False)
async def sign(session: CommandSession):
    QQ = session.ctx['user_id']
    user = userSQL()
    if not user.isExist(QQ):
        user.insert(QQ)
    if user.isSigned(QQ):
        await session.send('你今天已经签过到啦，明天再来吧。')
    else:
        count = user.sign(QQ)
        # 签到奖励
        value = random.randint(10, 300)
        user.addDiamond(QQ, value)
        sumDiamond = user.getDiamond(QQ)
        user.close()
        await session.send('签到成功,你是今天第'+str(count)+'位签到的。恭喜你获得'+str(value)+'个钻石，你当前总共有'+str(sumDiamond)+'个钻石。')


@on_command('查询', only_to_me=False)
async def query(session: CommandSession):
    QQ = session.ctx['user_id']
    user = userSQL()
    if not user.isExist(QQ):
        user.close()
        await session.send('请先发送”/签到“进行注册')
        return
    score = user.getScore(QQ)
    ticket = user.getTicket(QQ)
    diamond = user.getDiamond(QQ)
    user.close()

    message = '个人信息' + '\n' +\
              '积分：' + str(score) + '\n' +\
              '奖券：' + str(ticket) + '\n' +\
              '钻石：' + str(diamond)

    await session.send(message)


@on_command('初始化', only_to_me=False)
async def initGroupList(session: CommandSession):
    QQ = session.ctx['user_id']
    if not isRoot(QQ):
        return
    bot = nonebot.get_bot()
    memberList = await bot.get_group_member_list(group_id=session.ctx['group_id'])
    user = userSQL()
    for member in memberList:
        QQ = member['user_id']
        if not user.isExist(QQ):
            user.insert(QQ)
    await session.send('初始化群成员数据成功,已将所有成员注册。')


@on_command('积分抽奖', aliases=('积分夺宝',), only_to_me=False)
async def scoreDraw(session: CommandSession):
    QQ = session.ctx['user_id']
    user = userSQL()
    score = user.getScore(QQ)
    if score >= 20:
        item = getScoreDrawRandom()
        user.subScore(QQ, 20)
        if item == 0:
            user.addTicket(QQ, 1)
        else:
            user.addScore(QQ, item)
        await session.send('恭喜您获得'+str(item)+'积分，您当前的积分余额为'+str(score-20+item)+'，欢迎下次光临。')
    else:
        await session.send('您的积分不足20，快去找老蛋赚积分吧。')
    user.close()


@on_command('积分五连', only_to_me=False)
async def scoreDraw2(session: CommandSession):
    QQ = session.ctx['user_id']
    user = userSQL()
    score = user.getScore(QQ)
    if score >= 100:
        items = [getScoreDrawRandom() for i in range(5)]
        user.subScore(QQ, 100)
        user.addScore(QQ, sum(items))
        user.addTicket(QQ, items.count(0))
        await session.send('恭喜您获得\n'+' '.join([str(j)+'积分' if j != 0 else '1奖券' for j in items]) + '，\n您当前的积分余额为'+str(score-100+sum(items))+'，欢迎下次光临。')
    else:
        await session.send('您的积分不足100，快去找老蛋赚积分吧。')
    user.close()


@on_command('奖券抽奖', aliases=('奖券夺宝',), only_to_me=False)
async def ticketDraw(session: CommandSession):
    QQ = session.ctx['user_id']
    user = userSQL()
    ticket = user.getTicket(QQ)
    if ticket >= 1:
        item = getScoreDrawRandom()
        user.subTicket(QQ, 1)
        if item == 0:
            user.addTicket(QQ, 1)
            await session.send('恭喜您获得1奖券，您当前的奖券余额为'+str(ticket)+'，欢迎下次光临。')
        else:
            user.addScore(QQ, item)
            await session.send('恭喜您获得'+str(item)+'积分，您当前的奖券余额为'+str(ticket-1)+'，欢迎下次光临。')
    else:
        await session.send('您的奖券不足，快去找老蛋赚奖券吧。')
    user.close()


@on_command('奖券五连', only_to_me=False)
async def ticketDraw2(session: CommandSession):
    QQ = session.ctx['user_id']
    user = userSQL()
    ticket = user.getTicket(QQ)
    if ticket >= 5:
        items = [getScoreDrawRandom() for i in range(5)]
        user.subTicket(QQ, 5)
        user.addScore(QQ, sum(items))
        user.addTicket(QQ, items.count(0))
        await session.send('恭喜您获得\n'+' '.join([str(j)+'积分' if j != 0 else '1奖券' for j in items]) + '，\n您当前的奖券余额为'+str(ticket-5+items.count(0))+'，欢迎下次光临。')
    else:
        await session.send('您的奖券不足，快去找老蛋赚奖券吧。')
    user.close()


@on_command('奖券榜', only_to_me=False)
async def topTicket(session: CommandSession):
    QQ = session.ctx['user_id']
    if not isRoot(QQ):
        return
    user = userSQL()
    rank = user.getTopTicket()
    user.close()
    bot = nonebot.get_bot()
    QQname = []
    for QQ in rank:
        group_member_info = await bot.get_group_member_info(group_id=session.ctx['group_id'], user_id=QQ[0], no_cache=True)
        QQname.append(group_member_info['card'])
        if len(QQname) > 5:
            break
    message = '奖券排行榜\n' + ''.join(['Top '+str(i+1)+'. '+QQname[i] +
                                   '\t '+str(rank[i][1])+'\n' for i in range(len(QQname))])
    await session.send(message)


@on_command('钻石榜', only_to_me=False)
async def topDiamond(session: CommandSession):
    QQ = session.ctx['user_id']
    if not isRoot(QQ):
        return
    user = userSQL()
    rank = user.getTopDiamond()
    user.close()
    bot = nonebot.get_bot()
    QQname = []
    for QQ in rank:
        group_member_info = await bot.get_group_member_info(group_id=session.ctx['group_id'], user_id=QQ[0], no_cache=True)
        QQname.append(group_member_info['card'])
        if len(QQname) > 5:
            break
    message = '钻石排行榜\n' + ''.join(['Top '+str(i+1)+'. '+QQname[i] +
                                   '\t '+str(rank[i][1])+'\n' for i in range(len(QQname))])
    await session.send(message)


@on_command('积分榜', only_to_me=False)
async def topScore(session: CommandSession):
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
    message = '积分排行榜\n' + ''.join(['Top '+str(i+1)+'. '+QQname[i] +
                                   '\t '+str(rank[i][1])+'\n' for i in range(len(QQname))])
    await session.send(message)


@on_command('加积分', only_to_me=False)
async def addScore(session: CommandSession):
    # 判断目标发起人是否为管理员
    QQ = session.ctx['user_id']
    if not isRoot(QQ):
        return

    # 解析命令格式
    inpt = session.state.get('message') or session.current_arg
    args = inpt.strip().split()
    if len(args) != 2:
        await session.send('格式为：/加积分 [@某人/QQ号] [积分数]')
        return
    if args[1].isdigit():
        score = int(args[1])
        if args[0][:6] == '[CQ:at':
            target = int(args[0][10:-1])
        elif (args[0]).isdigit():
            target = int(args[0])
        else:
            await session.send('加分目标应为QQ号或@某人，格式为：/加积分 [@某人/QQ号] [积分数]')
            return
    else:
        await session.send('积分数应为一个整数，格式为：/加积分 [@某人/QQ号] [积分数]')
        return

    # 对用户进行加分操作
    user = userSQL()
    if not user.isExist(target):
        user.close()
        await session.send('QQ为'+str(target)+'的用户不存在')
        return
    user.addScore(target, score)
    now = user.getScore(target)
    user.close()
    await session.send('增加成功，当前目标用户的积分为'+str(now))


@on_command('减积分', only_to_me=False)
async def subScore(session: CommandSession):
    # 判断目标发起人是否为管理员
    QQ = session.ctx['user_id']
    if not isRoot(QQ):
        return

    # 解析命令格式
    inpt = session.state.get('message') or session.current_arg
    args = inpt.strip().split()
    if len(args) != 2:
        await session.send('格式为：/减积分 [@某人/QQ号] [积分数]')
        return
    if args[1].isdigit():
        score = int(args[1])
        if args[0][:6] == '[CQ:at':
            target = int(args[0][10:-1])
        elif (args[0]).isdigit():
            target = int(args[0])
        else:
            await session.send('减分目标应为QQ号或@某人，格式为：/减积分 [@某人/QQ号] [积分数]')
            return
    else:
        await session.send('积分数应为一个整数，格式为：/减积分 [@某人/QQ号] [积分数]')
        return

    # 对用户进行加分操作
    user = userSQL()
    if not user.isExist(target):
        user.close()
        await session.send('QQ为'+str(target)+'的用户不存在')
        return
    user.subScore(target, score)
    now = user.getScore(target)
    user.close()
    await session.send('减少成功，当前目标用户的积分为'+str(now))


@on_command('加奖券', only_to_me=False)
async def addTicket(session: CommandSession):
    # 判断目标发起人是否为管理员
    QQ = session.ctx['user_id']
    if not isRoot(QQ):
        return

    # 解析命令格式
    inpt = session.state.get('message') or session.current_arg
    args = inpt.strip().split()
    if len(args) != 2:
        await session.send('格式为：/加奖券 [@某人/QQ号] [奖券数]')
        return
    if args[1].isdigit():
        ticket = int(args[1])
        if args[0][:6] == '[CQ:at':
            target = int(args[0][10:-1])
        elif (args[0]).isdigit():
            target = int(args[0])
        else:
            await session.send('加分目标应为QQ号或@某人，格式为：/加奖券 [@某人/QQ号] [奖券数]')
            return
    else:
        await session.send('奖券数应为一个整数，格式为：/加奖券 [@某人/QQ号] [奖券数]')
        return

    # 对用户进行加分操作
    user = userSQL()
    if not user.isExist(target):
        user.close()
        await session.send('QQ为'+str(target)+'的用户不存在')
        return
    user.addTicket(target, ticket)
    now = user.getTicket(target)
    user.close()
    await session.send('增加成功，当前目标用户的奖券为'+str(now))


@on_command('减奖券', only_to_me=False)
async def subTicket(session: CommandSession):
    # 判断目标发起人是否为管理员
    QQ = session.ctx['user_id']
    if not isRoot(QQ):
        return

    # 解析命令格式
    inpt = session.state.get('message') or session.current_arg
    args = inpt.strip().split()
    if len(args) != 2:
        await session.send('格式为：/减奖券 [@某人/QQ号] [奖券数]')
        return
    if args[1].isdigit():
        ticket = int(args[1])
        if args[0][:6] == '[CQ:at':
            target = int(args[0][10:-1])
        elif (args[0]).isdigit():
            target = int(args[0])
        else:
            await session.send('减分目标应为QQ号或@某人，格式为：/减奖券 [@某人/QQ号] [奖券数]')
            return
    else:
        await session.send('奖券数应为一个整数，格式为：/减奖券 [@某人/QQ号] [奖券数]')
        return

    # 对用户进行加分操作
    user = userSQL()
    if not user.isExist(target):
        user.close()
        await session.send('QQ为'+str(target)+'的用户不存在')
        return
    user.subTicket(target, ticket)
    now = user.getTicket(target)
    user.close()
    await session.send('减少成功，当前目标用户的奖券为'+str(now))


@on_command('注册', only_to_me=False)
async def register(session: CommandSession):
    # 判断目标发起人是否为管理员
    QQ = session.ctx['user_id']
    if not isRoot(QQ):
        return

    # 解析命令格式
    inpt = session.state.get('message') or session.current_arg
    args = inpt.strip()
    if len(args) != 1:
        await session.send('格式为：/注册 [@某人/QQ号]')
        return
    if args[:6] == '[CQ:at':
        target = int(args[10:-1])
    elif args.isdigit():
        target = int(args)
    else:
        await session.send('注册目标应为QQ号或@某人，格式为：/注册 [@某人/QQ号]')
        return

    user = userSQL()
    if user.isExist(target):
        user.close()
        await session.send('QQ为'+str(target)+'的用户已存在，请勿重复注册')
        return
    user.insert(target)
    user.close()
    await session.send('注册成功')


@on_command('清空积分', aliases=('积分清零',), only_to_me=False)
async def resetScore(session: CommandSession):
    # 判断目标发起人是否为管理员
    QQ = session.ctx['user_id']
    if not isRoot(QQ):
        return
    user = userSQL()
    user.resetScore()
    user.close()
    await session.send('全体积分清空成功')


@on_command('清空奖券', aliases=('奖券清零',), only_to_me=False)
async def resetTicket(session: CommandSession):
    # 判断目标发起人是否为管理员
    QQ = session.ctx['user_id']
    if not isRoot(QQ):
        return
    user = userSQL()
    user.resetTicket()
    user.close()
    await session.send('全体奖券清空成功')


@on_command('清空钻石', aliases=('钻石清零',), only_to_me=False)
async def resetDiamond(session: CommandSession):
    # 判断目标发起人是否为管理员
    QQ = session.ctx['user_id']
    if not isRoot(QQ):
        return
    user = userSQL()
    user.resetDiamond()
    user.close()
    await session.send('全体钻石清空成功')
