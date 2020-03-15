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
    
