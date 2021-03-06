import nonebot
from nonebot import on_command, CommandSession, permission
from .data_source import Pokemon, Choice, Reward, getImage
from .header import pokeNameChn, stopWord
import sqlite3

__plugin_name__ = '宝可梦'
__plugin_usage__ = r"""
欢迎来到精灵宝可梦的世界
回复“开始游戏”即可开始寻找你的伙伴哦。
根据选项回复A B C D即可。

管理功能：
/悬赏 [精灵:数目，逗号分开] [奖励:数目，逗号分开] [限制人数] [无|备注]

成员功能：
/揭榜 [编号]
/领取悬赏 [编号]
/查询悬赏
/撤销悬赏
"""

GameList = {}
nowReward = None


@on_command('开始游戏', only_to_me=False)
async def sign(session: CommandSession):
    global GameList
    QQ = session.ctx['user_id']
    if QQ not in GameList:
        GameList[QQ] = Pokemon(QQ)
    game = GameList[QQ]
    message = game.begin()
    await session.send(message)


@on_command('A', aliases=('a',), only_to_me=False)
async def chooseA(session: CommandSession):
    global GameList
    QQ = session.ctx['user_id']
    if QQ in GameList:
        game = GameList[QQ]
        message = game.next(Choice.A)
        await session.send(message)


@on_command('B', aliases=('b',), only_to_me=False)
async def chooseB(session: CommandSession):
    global GameList
    QQ = session.ctx['user_id']
    if QQ in GameList:
        game = GameList[QQ]
        message = game.next(Choice.B)
        await session.send(message)


@on_command('C', aliases=('c',), only_to_me=False)
async def chooseC(session: CommandSession):
    global GameList
    QQ = session.ctx['user_id']
    if QQ in GameList:
        game = GameList[QQ]
        message = game.next(Choice.C)
        await session.send(message)


@on_command('D', aliases=('Ｄ', 'd',), only_to_me=False)
async def chooseD(session: CommandSession):
    global GameList
    QQ = session.ctx['user_id']
    if QQ in GameList:
        game = GameList[QQ]
        message = game.next(Choice.D)
        await session.send(message)


@on_command('Q', aliases=('q',), only_to_me=False)
async def chooseQ(session: CommandSession):
    global GameList
    QQ = session.ctx['user_id']
    if QQ in GameList:
        game = GameList[QQ]
        message = game.next(Choice.Q)
        await session.send(message)

# @on_command('PQ', aliases=('pq','Pq','pQ'), only_to_me=False)
# async def choosePQ(session: CommandSession):
#     global GameList
#     QQ = session.ctx['user_id']
#     if QQ in GameList:
#         game = GameList[QQ]
#     else:
#         GameList[QQ] = Pokemon(QQ)
#         game = GameList[QQ]
#     game.begin()
#     message = game.next(Choice.Q)
#     await session.send(message)


def echoReward(reward: {}) -> str:
    ''':reward: {'group_id': int,
                'pokemon': [[name,num],],
                'award': [[name,num],],
                'limitNum': int,
                'remard': str}'''
    return f"编号：{reward['id']}\n\
通缉：{','.join([f'{x[0]}x{x[1]}' for x in reward['pokemon']])}\n\
赏金：{','.join([f'{x[0]}x{x[1]}' for x in reward['award']])}\n\
限制人数：{'不限次数' if reward['limitNum'] < 0 else reward['limitNum']}\n\
领赏人数：{len(reward['getList'])}\n\
备注：{reward['remark']}"


@on_command('悬赏', aliases=('发布悬赏',), only_to_me=False, permission=permission.SUPERUSER)
async def sendReward(session: CommandSession):
    inpt = session.state.get('message') or session.current_arg
    inpt = inpt.replace('，', ',')
    inpt = inpt.replace('：', ':')
    args = inpt.strip().split()
    if len(args) != 3 and len(args) != 4:
        await session.send(
            '格式为 /悬赏 [精灵:数目，逗号分开] [奖励:数目，逗号分开] [限制人数] [无|备注]。\n例如： \悬赏 阿柏蛇:1,喵喵:2,皮皮:1 奖券:1 3 第一名单独多奖励一个奖券')
        return
    remark = None if len(args) == 3 else args[3]
    limitNum = int(args[2]) if args[2].isdigit() else -1
    pokemon = [x.split(':') for x in args[0].strip().split(',')]
    if not all([x[0] in pokeNameChn for x in pokemon]):
        await session.send('你悬赏的精灵不存在，请重新发布悬赏。')
        return
    award = [x.split(':') for x in args[1].strip().split(',')]
    groupID = session.ctx['group_id']
    reward = Reward()
    temp = {'group_id': groupID, 'pokemon': pokemon,
            'award': award, 'limitNum': limitNum, 'remark': remark}
    id = reward.postReward(temp)
    temp['id'] = id
    temp['getList'] = []

    if groupID is not None:
        bot = nonebot.get_bot()
        # await bot._send_group_notice(group_id=groupID, title='悬赏',
        #                              content=message)
        await session.send(echoReward(temp))


@on_command('揭榜', aliases=('领取悬赏',), only_to_me=False)
async def getReward(session: CommandSession):
    inpt = session.state.get('message') or session.current_arg
    args = inpt.strip()
    if args == '' or not args.isdigit():
        await session.send('请输入通缉令编号，格式为 /揭榜 [编号]')
    QQ = session.ctx['user_id']
    bot = nonebot.get_bot()
    group_member_info = await bot.get_group_member_info(group_id=session.ctx['group_id'], user_id=QQ,
                                                        no_cache=False)
    name = group_member_info['card'] or group_member_info['nickname']
    reward = Reward()
    if all([w not in name for w in stopWord]):
        if reward.meetReward(QQ, session.ctx['group_id'], int(args)):
            reward.getReward(QQ, int(args))
            await session.send(f'{getImage("getReward")}\n恭喜你，揭榜成功！')


@on_command('查询悬赏', aliases=('悬赏榜',), only_to_me=False)
async def getAllReward(session: CommandSession):
    group_id = session.ctx['group_id']
    rewardList = Reward().echoReward(group_id)
    if rewardList == []:
        await session.send('当前还没有悬赏任务哦，勇士晚些再来吧~')
        return
    message = '通缉令\n'
    for reward in rewardList:
        message = message + '-' * 20 + '\n' + echoReward(reward) + '\n'
    await session.send(message)


@on_command('撤销悬赏', only_to_me=False, permission=permission.SUPERUSER)
async def endReward(session: CommandSession):
    inpt = session.state.get('message') or session.current_arg
    args = inpt.strip()
    if args == '' or not args.isdigit():
        await session.send('请输入通缉令编号，格式为 /撤销悬赏 [编号]')
    if Reward().endReward(int(args), session.ctx['group_id']):
        await session.send(f'悬赏{args}撤销成功~')
    else:
        await session.send(f'撤销悬赏失败，在该群发布的编号为{args}的悬赏不存在。')
