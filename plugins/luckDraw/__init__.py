import nonebot
from nonebot import on_command, CommandSession, permission
from nonebot import on_natural_language, NLPSession, IntentCommand
from .data_source import userSQL, getScoreDrawRandom, getDiamonDrawRandom
from .data_source import getImage, getBallImage, getConsImage, getBallEmoji, getConsEmoji
from ..pokemon.header import pokeNameChn
from .data_source import consName, stopWord
import random

__plugin_name__ = '抽奖系统'
__plugin_usage__ = r"""
抽奖系统支持功能:
签到
查询
物品/物品查询/背包/背包查询
宠物/宠物查询/我的宠物/宝可梦
积分抽奖/积分夺宝
积分五连
奖券抽奖/奖券夺宝
奖券五连
钻石抽奖/钻石夺宝 [空|次数]

管理功能:
初始化
注册 [@某人/QQ号]
奖券榜
积分榜
钻石榜
发言榜
清空奖券/奖券清零
清空积分/积分清零
清空钻石/钻石清零
清空背包/背包清零
清空宠物/宠物清零
清空精灵球/精灵球清零
清空星座卡/星座卡清零
加奖券 [@某人/QQ号] [数量]
减奖券 [@某人/QQ号] [数量]
加积分 [@某人/QQ号] [数量]
减积分 [@某人/QQ号] [数量]
加钻石 [@某人/QQ号] [数量]
减钻石 [@某人/QQ号] [数量]
加物品 [@某人/QQ号] [物品] [数目]
减物品 [@某人/QQ号] [物品] [数目]
祈福/老板发钱/桃园结义/普度众生/悬壶济世 [下限] [上限]
祈福/老板发钱/桃园结义/普度众生/悬壶济世 (默认60)
祈福/老板发钱/桃园结义/普度众生/悬壶济世 [金额]
"""


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
        value = random.randint(300, 600)
        user.addDiamond(QQ, value)
        sumDiamond = user.getDiamond(QQ)
        message = '签到成功,你是今天第' + str(count) + '位签到的。恭喜你获得' + str(value) + '个钻石，你当前总共有' + str(sumDiamond) + '个钻石。'
        await session.send(message)
    user.close()


@on_command('message', only_to_me=False)
async def message(session: CommandSession):
    QQ = session.ctx['user_id']
    # 获取可选参数，这里如果没有 message 参数，命令不会被中断，message 变量会是 None
    message = session.state.get('message')
    # 屏蔽表情包
    # if not message: return
    user = userSQL()
    if not user.isExist(QQ):
        user.insert(QQ)
    messageNum = user.getMessageNum(QQ)
    if messageNum < 5:
        user.addDiamond(QQ, 10)
    elif messageNum == 100:
        await session.send('你今天已经说了100句话了！奖励你一个钻石鼓励一下啵(#^.^#)')
        user.addDiamond(QQ, 1)
    elif messageNum == 1000:
        await session.send('你今天已经说了1000句话了！你太能唠了，扣10钻石！')
        user.subDiamond(QQ, 10)
    elif messageNum == 2000:
        await session.send('你今天已经说了2000句话了！你太能唠了，我把扣的10钻石加回来吧(灬ꈍ ꈍ灬),再奖励你一点。！')
        user.addDiamond(QQ, 11)
    elif messageNum == 3000:
        await session.send('你今天已经说了3000句话了！我劝你不要继续往下刷屏了，扣12钻石！')
        user.subDiamond(QQ, 15)
    elif messageNum == 4000:
        await session.send('你今天已经说了4000句话了！怕了你了，13颗钻石给你给你都给你！')
        user.addDiamond(QQ, 17)
    elif messageNum == 5000:
        await session.send('你是传说中的龙王吧，你今天已经说了5000句话了！是在下唐突了，罚18颗钻石以儆效尤。')
    elif messageNum == 5999:
        await session.send('你今天已经说了5999句话了！你确定要刷到6000？')
    elif messageNum == 6000:
        await session.send('一阵风吹过，6000句话说到我心里，却无事发生。')  
    elif messageNum == 6999:
        await session.send('你今天已经说了6999句话了！你确定要刷到7000？')
    elif messageNum == 7000:
        await session.send('一阵风吹过，7000句话说到我心里，却无事发生。')  
    elif messageNum == 7999:
        await session.send('你今天已经说了7999句话了！你确定要刷到8000？')
    elif messageNum == 8000:
        await session.send('一阵风吹过，8000句话说到我心里，却无事发生。')    
    elif messageNum == 9999:
        await session.send('你今天已经说了9999句话了！友谊提醒你不要再说话了，要不然怎么哭的都不知道。')
    elif messageNum == 10000:
        await session.send('你今天已经说了10000句话了，恭喜你找到了最后的彩蛋。')
        user.addDiamond(QQ, 20)
    user.addMessageNum(QQ)
    user.close()


@on_natural_language(only_to_me=False)
async def _(session: NLPSession):
    # 以置信度 60.0 返回 message 命令
    # 确保任何消息都在且仅在其它自然语言处理器无法理解的时候使用 message 命令
    return IntentCommand(60.0, 'message', args={'message': session.msg_text})


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
    messageNum = user.getMessageNum(QQ)
    user.close()

    message = '个人信息' + '\n' + \
              '积分:' + str(score) + '\n' + \
              '奖券:' + str(ticket) + '\n' + \
              '钻石:' + str(diamond) + '\n' + \
              '发言:' + str(messageNum) + '条'

    await session.send(message)


@on_command('物品', aliases=('物品查询', '背包', '背包查询'), only_to_me=False)
async def backpack(session: CommandSession):
    QQ = session.ctx['user_id']
    user = userSQL()
    if not user.isExist(QQ):
        user.close()
        await session.send('请先发送”/签到“进行注册')
        return
    evelsBall = user.getEvelsBall(QQ)
    superBall = user.getSuperBall(QQ)
    masterBall = user.getMasterBall(QQ)
    cons = user.getConstellation(QQ)

    user.close()

    message = '我的背包' + '\n' + \
              getBallEmoji('evelsBall') + '精灵球:' + str(evelsBall) + '\n' + \
              getBallEmoji('superBall') + '超级球:' + str(superBall) + '\n' + \
              getBallEmoji('masterBall') + '大师球:' + str(masterBall) + '\n' + \
              ''.join([getConsEmoji(i) + consName[i] + ':' + str(cons[i]) +
                       '\n' for i in range(len(cons))])
    await session.send(message[:-1])


@on_command('宠物', aliases=('宠物查询', '我的宠物', '宝可梦',), only_to_me=False)
async def pet(session: CommandSession):
    QQ = session.ctx['user_id']
    user = userSQL()
    if not user.isExist(QQ):
        user.close()
        await session.send('请先发送”/签到“进行注册')
        return
    pokemon = user.getPokemon(QQ)
    user.close()

    message = '我的宠物' + '\n' + \
              ''.join([pokeNameChn[i] + ':' + str(pokemon[i]) +
                       '\n' for i in range(len(pokemon) - 1)])
    message = message + pokeNameChn[-1] + ':' + \
              str(pokemon[-1]) + '\n' if pokemon[-1] != 0 else message
    await session.send(message[:-1])


@on_command('初始化', only_to_me=False, permission=permission.SUPERUSER)
async def initGroupList(session: CommandSession):
    bot = nonebot.get_bot()
    memberList = await bot.get_group_member_list(group_id=session.ctx['group_id'])
    user = userSQL()
    for member in memberList:
        QQ = member['user_id']
        if not user.isExist(QQ):
            user.insert(QQ)
    user.close()
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
            await session.send(getImage('ticket') + '\n恭喜你获得1奖券，你当前的积分余额为' + str(score - 20 + item) + '，欢迎下次光临。')
        else:
            user.addScore(QQ, item)
            await session.send(getImage(str(item) + 'score') + '\n恭喜你获得' + str(item) + '积分，你当前的积分余额为' + str(
                score - 20 + item) + '，欢迎下次光临。')
    else:
        await session.send('你的积分不足20，快去找老蛋赚积分吧。')
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
        await session.send('恭喜你获得\n' + ' '.join(
            [getImage(str(j) + 'score') + '\n' + str(j) + '积分\n' if j != 0 else getImage('ticket') + '\n1奖券\n' for j in
             items]) + '，\n你当前的积分余额为' + str(score - 100 + sum(items)) + '，欢迎下次光临。')
    else:
        await session.send('你的积分不足100，快去找老蛋赚积分吧。')
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
            await session.send(getImage('ticket') + '\n恭喜你获得1奖券，你当前的奖券余额为' + str(ticket) + '，欢迎下次光临。')
        else:
            user.addScore(QQ, item)
            await session.send(
                getImage(str(item) + 'score') + '\n恭喜你获得' + str(item) + '积分，你当前的奖券余额为' + str(ticket - 1) + '，欢迎下次光临。')
    else:
        await session.send('你的奖券不足，快去找老蛋赚奖券吧。')
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
        await session.send('恭喜你获得\n' + ' '.join(
            [getImage(str(j) + 'score') + '\n' + str(j) + '积分\n' if j != 0 else getImage('ticket') + '\n1奖券\n' for j in
             items]) + '，\n你当前的奖券余额为' + str(ticket - 5 + items.count(0)) + '，欢迎下次光临。')
    else:
        await session.send('你的奖券不足，快去找老蛋赚奖券吧。')
    user.close()


@on_command('钻石抽奖', aliases=('钻石夺宝',), only_to_me=False)
async def diamonDraw(session: CommandSession):
    inpt = session.state.get('message') or session.current_arg
    args = inpt.strip().split()
    times = 1
    if len(args) == 0:
        times = 1
    elif len(args) == 1 and args[0].isdigit():
        times = int(args[0])
    else:
        await session.send('格式为 /钻石抽奖 或者 /钻石抽奖 [次数]。')
        return
    QQ = session.ctx['user_id']
    user = userSQL()
    diamond = user.getDiamond(QQ)
    if diamond >= times * 60:
        message = ''
        user.subDiamond(QQ, times * 60)
        ans = [getDiamonDrawRandom() for i in range(times)]
        ticketNum = ans.count('ticket')
        if ticketNum > 0:
            user.addTicket(QQ, ticketNum)
            message = message + getImage('ticket') + \
                      '\n恭喜你获得' + str(ticketNum) + '奖券\n'
        cardNum = ans.count('card')
        if cardNum > 0:
            cardIndex = [random.randint(0, 11) for i in range(cardNum)]
            for i in range(12):
                num = cardIndex.count(i)
                if num > 0:
                    user.addCons(QQ, i, num)
                    message = message + getConsImage(i) + '\n恭喜你获得' + \
                              str(num) + '张' + consName[i] + '卡片\n'
        diamondSum = sum([int(i) for i in ans if i.isdigit()])
        if diamondSum > 0:
            user.addDiamond(QQ, diamondSum)
            if diamondSum in [30, 60, 120, 300]:
                message = message + \
                          getImage(str(diamondSum) + 'diamond') + \
                          '\n恭喜你获得' + str(diamondSum) + '钻石\n'
            else:
                message = message + '恭喜你获得' + str(diamondSum) + '钻石\n'
        evelsBall = ans.count('evelsBall')
        if evelsBall > 0:
            user.addEvelsBall(QQ, evelsBall)
            message = message + \
                      getBallImage('evelsBall') + '\n恭喜你获得' + str(evelsBall) + '个精灵球\n'
        superBall = ans.count('superBall')
        if superBall > 0:
            user.addSuperBall(QQ, superBall)
            message = message + \
                      getBallImage('superBall') + '\n恭喜你获得' + str(superBall) + '个超级球\n'
        masterBall = ans.count('masterBall')
        if masterBall > 0:
            user.addMasterBall(QQ, masterBall)
            message = message + \
                      getBallImage('masterBall') + '\n恭喜你获得' + \
                      str(masterBall) + '个大师球\n欢迎下次光临。'
        await session.send(message)
    else:
        await session.send('你的钻石不足，快去找老蛋赚钻石吧。')
    user.close()


@on_command('奖券榜', only_to_me=False)
async def topTicket(session: CommandSession):
    user = userSQL()
    rank = user.getTopTicket()
    user.close()
    bot = nonebot.get_bot()
    QQname = []
    for QQ in rank:
        try:
            group_member_info = await bot.get_group_member_info(group_id=session.ctx['group_id'], user_id=QQ[0],
                                                                no_cache=False)
            name = group_member_info['card'] or group_member_info['nickname']
            if all([w not in name for w in stopWord]):
                QQname.append((name, QQ[1]))
        except:  # 非本群人员
            pass
        # if len(QQname) > 5:
        #     break
    message = '[CQ:emoji, id=128179]奖券排行榜[CQ:emoji, id=128179]\n' + ''.join(['Top ' + str(i + 1) + '. ' + QQname[i][0] +
                                   '\t ' + str(QQname[i][1]) + '\n' for i in range(len(QQname))])
    await session.send(message[:-1])


@on_command('钻石榜', only_to_me=False)
async def topDiamond(session: CommandSession):
    user = userSQL()
    rank = user.getTopDiamond()
    user.close()
    bot = nonebot.get_bot()
    QQname = []
    for QQ in rank:
        try:
            group_member_info = await bot.get_group_member_info(group_id=session.ctx['group_id'], user_id=QQ[0],
                                                                no_cache=False)
            name = group_member_info['card'] or group_member_info['nickname']
            if all([w not in name for w in stopWord]):
                QQname.append((name, QQ[1]))
        except:  # 非本群人员
            pass
        # if len(QQname) > 5:
        #     break
    message = '[CQ:emoji, id=128142]钻石排行榜[CQ:emoji, id=128142]\n' + ''.join(['Top ' + str(i + 1) + '. ' + QQname[i][0] +
                                   '\t ' + str(QQname[i][1]) + '\n' for i in range(len(QQname))])
    await session.send(message[:-1])


@on_command('发言榜', only_to_me=False)
async def topMessage(session: CommandSession):
    user = userSQL()
    rank = user.getTopMessage()
    user.close()
    bot = nonebot.get_bot()
    QQname = []
    for QQ in rank:
        try:
            group_member_info = await bot.get_group_member_info(group_id=session.ctx['group_id'], user_id=QQ[0],
                                                                no_cache=False)
            name = group_member_info['card'] or group_member_info['nickname']
            if all([w not in name for w in stopWord]):
                QQname.append((name, QQ[1]))
        except:  # 非本群人员
            pass
        # if len(QQname) > 5:
        #     break
    message = '[CQ:emoji, id=128172]发言排行榜[CQ:emoji, id=128172]\n' + ''.join(['Top ' + str(i + 1) + '. ' + QQname[i][0] +
                                   '\t ' + str(QQname[i][1]) + '\n' for i in range(len(QQname))])
    await session.send(message[:-1])


@on_command('积分榜', only_to_me=False)
async def topScore(session: CommandSession):
    user = userSQL()
    rank = user.getTopScore()
    user.close()
    bot = nonebot.get_bot()
    QQname = []
    for QQ in rank:
        try:
            group_member_info = await bot.get_group_member_info(group_id=session.ctx['group_id'], user_id=QQ[0],
                                                                no_cache=False)
            name = group_member_info['card'] or group_member_info['nickname']
            if all([w not in name for w in stopWord]):
                QQname.append((name, QQ[1]))
        except:  # 非本群人员
            pass
        # if len(QQname) > 5:
        #     break
    message = '[CQ:emoji, id=128176]积分排行榜[CQ:emoji, id=128176]\n' + ''.join(['Top ' + str(i + 1) + '. ' + QQname[i][0] +
                                   '\t ' + str(QQname[i][1]) + '\n' for i in range(len(QQname))])
    await session.send(message[:-1])


@on_command('加积分', only_to_me=False, permission=permission.SUPERUSER)
async def addScore(session: CommandSession):
    # 解析命令格式
    inpt = session.state.get('message') or session.current_arg
    args = inpt.strip().split()
    if len(args) != 2:
        await session.send('格式为:/加积分 [@某人/QQ号] [积分数]')
        return
    if args[1].isdigit():
        score = int(args[1])
        if args[0][:6] == '[CQ:at':
            target = int(args[0][10:-1])
        elif (args[0]).isdigit():
            target = int(args[0])
        else:
            await session.send('加分目标应为QQ号或@某人，格式为:/加积分 [@某人/QQ号] [积分数]')
            return
    else:
        await session.send('积分数应为一个整数，格式为:/加积分 [@某人/QQ号] [积分数]')
        return

    # 对用户进行加分操作
    user = userSQL()
    if not user.isExist(target):
        user.close()
        await session.send('QQ为' + str(target) + '的用户不存在')
        return
    user.addScore(target, score)
    now = user.getScore(target)
    user.close()
    await session.send('增加成功，当前目标用户的积分为' + str(now))


@on_command('减积分', only_to_me=False, permission=permission.SUPERUSER)
async def subScore(session: CommandSession):

    # 解析命令格式
    inpt = session.state.get('message') or session.current_arg
    args = inpt.strip().split()
    if len(args) != 2:
        await session.send('格式为:/减积分 [@某人/QQ号] [积分数]')
        return
    if args[1].isdigit():
        score = int(args[1])
        if args[0][:6] == '[CQ:at':
            target = int(args[0][10:-1])
        elif (args[0]).isdigit():
            target = int(args[0])
        else:
            await session.send('减分目标应为QQ号或@某人，格式为:/减积分 [@某人/QQ号] [积分数]')
            return
    else:
        await session.send('积分数应为一个整数，格式为:/减积分 [@某人/QQ号] [积分数]')
        return

    # 对用户进行加分操作
    user = userSQL()
    if not user.isExist(target):
        user.close()
        await session.send('QQ为' + str(target) + '的用户不存在')
        return
    user.subScore(target, score)
    now = user.getScore(target)
    user.close()
    await session.send('减少成功，当前目标用户的积分为' + str(now))


@on_command('加奖券', only_to_me=False, permission=permission.SUPERUSER)
async def addTicket(session: CommandSession):
     # 解析命令格式
    inpt = session.state.get('message') or session.current_arg
    args = inpt.strip().split()
    if len(args) != 2:
        await session.send('格式为:/加奖券 [@某人/QQ号] [奖券数]')
        return
    if args[1].isdigit():
        ticket = int(args[1])
        if args[0][:6] == '[CQ:at':
            target = int(args[0][10:-1])
        elif (args[0]).isdigit():
            target = int(args[0])
        else:
            await session.send('加分目标应为QQ号或@某人，格式为:/加奖券 [@某人/QQ号] [奖券数]')
            return
    else:
        await session.send('奖券数应为一个整数，格式为:/加奖券 [@某人/QQ号] [奖券数]')
        return

    # 对用户进行加分操作
    user = userSQL()
    if not user.isExist(target):
        user.close()
        await session.send('QQ为' + str(target) + '的用户不存在')
        return
    user.addTicket(target, ticket)
    now = user.getTicket(target)
    user.close()
    await session.send('增加成功，当前目标用户的奖券为' + str(now))


@on_command('减奖券', only_to_me=False, permission=permission.SUPERUSER)
async def subTicket(session: CommandSession):
    # 解析命令格式
    inpt = session.state.get('message') or session.current_arg
    args = inpt.strip().split()
    if len(args) != 2:
        await session.send('格式为:/减奖券 [@某人/QQ号] [奖券数]')
        return
    if args[1].isdigit():
        ticket = int(args[1])
        if args[0][:6] == '[CQ:at':
            target = int(args[0][10:-1])
        elif (args[0]).isdigit():
            target = int(args[0])
        else:
            await session.send('减分目标应为QQ号或@某人，格式为:/减奖券 [@某人/QQ号] [奖券数]')
            return
    else:
        await session.send('奖券数应为一个整数，格式为:/减奖券 [@某人/QQ号] [奖券数]')
        return

    # 对用户进行加分操作
    user = userSQL()
    if not user.isExist(target):
        user.close()
        await session.send('QQ为' + str(target) + '的用户不存在')
        return
    user.subTicket(target, ticket)
    now = user.getTicket(target)
    user.close()
    await session.send('减少成功，当前目标用户的奖券为' + str(now))


@on_command('加钻石', only_to_me=False, permission=permission.SUPERUSER)
async def addDiamond(session: CommandSession):
    # 解析命令格式
    inpt = session.state.get('message') or session.current_arg
    args = inpt.strip().split()
    if len(args) != 2:
        await session.send('格式为:/加钻石 [@某人/QQ号] [钻石数]')
        return
    if args[1].isdigit():
        diamond = int(args[1])
        if args[0][:6] == '[CQ:at':
            target = int(args[0][10:-1])
        elif (args[0]).isdigit():
            target = int(args[0])
        else:
            await session.send('加分目标应为QQ号或@某人，格式为:/加钻石 [@某人/QQ号] [钻石数]')
            return
    else:
        await session.send('钻石数应为一个整数，格式为:/加钻石 [@某人/QQ号] [钻石数]')
        return

    # 对用户进行加分操作
    user = userSQL()
    if not user.isExist(target):
        user.close()
        await session.send('QQ为' + str(target) + '的用户不存在')
        return
    user.addDiamond(target, diamond)
    now = user.getDiamond(target)
    user.close()
    await session.send('增加成功，当前目标用户的钻石为' + str(now))


@on_command('减钻石', only_to_me=False, permission=permission.SUPERUSER)
async def subDiamond(session: CommandSession):
    # 解析命令格式
    inpt = session.state.get('message') or session.current_arg
    args = inpt.strip().split()
    if len(args) != 2:
        await session.send('格式为:/减钻石 [@某人/QQ号] [钻石数]')
        return
    if args[1].isdigit():
        diamond = int(args[1])
        if args[0][:6] == '[CQ:at':
            target = int(args[0][10:-1])
        elif (args[0]).isdigit():
            target = int(args[0])
        else:
            await session.send('减分目标应为QQ号或@某人，格式为:/减钻石 [@某人/QQ号] [钻石数]')
            return
    else:
        await session.send('钻石数应为一个整数，格式为:/减钻石 [@某人/QQ号] [钻石数]')
        return

    # 对用户进行加分操作
    user = userSQL()
    if not user.isExist(target):
        user.close()
        await session.send('QQ为' + str(target) + '的用户不存在')
        return
    user.subDiamond(target, diamond)
    now = user.getDiamond(target)
    user.close()
    await session.send('减少成功，当前目标用户的钻石为' + str(now))


@on_command('注册', only_to_me=False, permission=permission.SUPERUSER)
async def register(session: CommandSession):
    # 解析命令格式
    inpt = session.state.get('message') or session.current_arg
    args = inpt.strip()
    if len(args) != 1:
        await session.send('格式为:/注册 [@某人/QQ号]')
        return
    if args[:6] == '[CQ:at':
        target = int(args[10:-1])
    elif args.isdigit():
        target = int(args)
    else:
        await session.send('注册目标应为QQ号或@某人，格式为:/注册 [@某人/QQ号]')
        return

    user = userSQL()
    if user.isExist(target):
        user.close()
        await session.send('QQ为' + str(target) + '的用户已存在，请勿重复注册')
        return
    user.insert(target)
    user.close()
    await session.send('注册成功')


@on_command('清空积分', aliases=('积分清零',), only_to_me=False, permission=permission.SUPERUSER)
async def resetScore(session: CommandSession):
    user = userSQL()
    user.resetScore()
    user.close()
    await session.send('全体积分清空成功')


@on_command('清空奖券', aliases=('奖券清零',), only_to_me=False, permission=permission.SUPERUSER)
async def resetTicket(session: CommandSession):
    user = userSQL()
    user.resetTicket()
    user.close()
    await session.send('全体奖券清空成功')


@on_command('清空钻石', aliases=('钻石清零',), only_to_me=False, permission=permission.SUPERUSER)
async def resetDiamond(session: CommandSession):
    user = userSQL()
    user.resetDiamond()
    user.close()
    await session.send('全体钻石清空成功')


@on_command('清空背包', aliases=('背包清零',), only_to_me=False, permission=permission.SUPERUSER)
async def resetBackpack(session: CommandSession):
    user = userSQL()
    user.resetBackpack()
    user.close()
    await session.send('全体背包清空成功')


@on_command('清空宠物', aliases=('宠物清零',), only_to_me=False, permission=permission.SUPERUSER)
async def resetPokemon(session: CommandSession):
    user = userSQL()
    user.resetPokemon()
    user.close()
    await session.send('全体宠物清空成功')


@on_command('清空精灵球', aliases=('精灵球清零',), only_to_me=False, permission=permission.SUPERUSER)
async def resetBall(session: CommandSession):
    user = userSQL()
    user.resetBall()
    user.close()
    await session.send('全体精灵球清空成功')


@on_command('清空星座卡', aliases=('星座卡清零',), only_to_me=False, permission=permission.SUPERUSER)
async def resetCons(session: CommandSession):
    user = userSQL()
    user.resetCons()
    user.close()
    await session.send('全体星座卡清空成功')


@on_command('祈福', aliases=('老板发钱', '桃园结义', '普度众生', '悬壶济世'), only_to_me=False, permission=permission.SUPERUSER)
async def bless(session: CommandSession):
    # 解析命令格式
    inpt = session.state.get('message') or session.current_arg
    args = inpt.strip().split()
    args = [int(i) for i in args if i.isdigit()]
    if len(args) > 2:
        await session.send('格式为:\n/祈福 [下限] [上限]\n或 /祈福\n或 /祈福 [金额]')
        return
    elif len(args) == 2:
        args.sort()
        money = random.randint(args[0], args[1])
    elif len(args) == 1:
        money = args[0]
    else:
        money = 60

    # 对用户进行加钻石操作
    user = userSQL()
    user.addAllDiamond(money)
    user.close()
    await session.send('增加成功，全体用户增加%d钻石。' % money)


@on_command('加物品', only_to_me=False, permission=permission.SUPERUSER)
async def addItem(session: CommandSession):
    inpt = session.state.get('message') or session.current_arg
    args = inpt.strip().split()
    if len(args) != 3 or not args[2].isdigit():
        await session.send('格式为 /加物品 [@某人/QQ号] [物品] [数目]。')
        return
    value = int(args[2])
    item = args[1]
    if args[0][:6] == '[CQ:at':
        target = int(args[0][10:-1])
    elif (args[0]).isdigit():
        target = int(args[0])
    else:
        await session.send('加物品目标应为QQ号或@某人，格式为 /加物品 [@某人/QQ号] [物品] [数目]。')
        return
    user = userSQL()
    user.addItem(target, item, value)
    user.close()
    await session.send('添加成功')


@on_command('减物品', only_to_me=False, permission=permission.SUPERUSER)
async def subItem(session: CommandSession):
    inpt = session.state.get('message') or session.current_arg
    args = inpt.strip().split()
    if len(args) != 3 or not args[2].isdigit():
        await session.send('格式为 /减物品 [@某人/QQ号] [物品] [数目]。')
        return
    value = int(args[2])
    item = args[1]
    if args[0][:6] == '[CQ:at':
        target = int(args[0][10:-1])
    elif (args[0]).isdigit():
        target = int(args[0])
    else:
        await session.send('减物品目标应为QQ号或@某人，格式为 /减物品 [@某人/QQ号] [物品] [数目]。')
        return
    user = userSQL()
    user.subItem(target, item, value)
    user.close()
    await session.send('减少成功')
