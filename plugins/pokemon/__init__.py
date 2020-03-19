import nonebot
from nonebot import on_command, CommandSession, permission
from .data_source import Pokemon, Choice, Reward
from .header import pokeNameChn
__plugin_name__ = '宝可梦'
__plugin_usage__ = r"""
欢迎来到精灵宝可梦的世界
回复“开始游戏”即可开始寻找你的伙伴哦。
根据选项回复A B C D即可。
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


@on_command('A', only_to_me=False)
async def chooseA(session: CommandSession):
    global GameList
    QQ = session.ctx['user_id']
    if QQ in GameList:
        game = GameList[QQ]
        message = game.next(Choice.A)
        await session.send(message)


@on_command('B', only_to_me=False)
async def chooseB(session: CommandSession):
    global GameList
    QQ = session.ctx['user_id']
    if QQ in GameList:
        game = GameList[QQ]
        message = game.next(Choice.B)
        await session.send(message)


@on_command('C', only_to_me=False)
async def chooseC(session: CommandSession):
    global GameList
    QQ = session.ctx['user_id']
    if QQ in GameList:
        game = GameList[QQ]
        message = game.next(Choice.C)
        await session.send(message)


@on_command('D', aliases=('Ｄ',), only_to_me=False)
async def chooseD(session: CommandSession):
    global GameList
    QQ = session.ctx['user_id']
    if QQ in GameList:
        game = GameList[QQ]
        message = game.next(Choice.D)
        await session.send(message)


@on_command('悬赏', aliases=('发布悬赏',), only_to_me=False, permission=permission.SUPERUSER)
async def sendReward(session: CommandSession):
    inpt = session.state.get('message') or session.current_arg
    inpt=inpt.replace('，', ',')
    inpt=inpt.replace('：', ':')
    args = inpt.strip().split()
    if len(args) != 3 and len(args) != 4:
        await session.send('格式为 /悬赏 [精灵:数目，逗号分开] [奖励:数目，逗号分开] [限制人数] [无|备注]。\n例如： \悬赏 阿柏蛇:1,喵喵:2,皮皮:1 奖券:1 3 第一名单独多奖励一个奖券')
        return
    remark = None if len(args)==3 else args[3]
    limitNum = int(args[2]) if args[2].isdigit() else None
    pokemon = [x.split(':') for x in args[0].strip().split(',')]
    if not all([x[0] in pokeNameChn for x in pokemon]):
        print([x[0] in pokeNameChn for x in pokemon])
        await session.send('你悬赏的精灵不存在，请重新发布悬赏。')
        return
    award =  [x.split(':') for x in args[1].strip().split(',')]
    reward = {'pokemon': pokemon, 'award': award, 'limitNum':limitNum, 'remard':remark, 'nowNum':0}
    nowReward = Reward(reward)
    groupID = session.ctx['group_id']
    if groupID is not None:
        bot = nonebot.get_bot()
        
        message = f"通缉：{','.join([f'{x[0]}x{x[1]}' for x in reward['pokemon']])}\n赏金：{','.join([f'{x[0]}x{x[1]}' for x in reward['award']])}\n备注：{remark}\n"
        await bot._send_group_notice(group_id=groupID, title='悬赏',
                                     content=message)

    @on_command('揭榜', aliases=('领取悬赏',), only_to_me=False)
    async def getReward(session: CommandSession):
        QQ = session.ctx['user_id']
        if nowReward.meetReward(QQ):
            nowReward.getReward(QQ)
            await session.send('恭喜你，揭榜成功！')
