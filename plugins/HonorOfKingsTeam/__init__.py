import nonebot
from nonebot import on_command, CommandSession, permission
from nonebot import on_natural_language, NLPSession, IntentCommand
import random

__plugin_name__ = '王者组队'
__plugin_usage__ = r"""
命令如下：
/开车 或 /[王者|空]组队 会创建一个空的队伍

/[游戏位置] 发送位置可以上车
位置有：打野 中单 战士 辅助 射手

/换位置 [打野|中单|战士|辅助|射手]
/下车
"""

game = {'打野': None, '中单': None, '战士': None, '辅助': None, '射手': None}


def echoTeam(game: {}) -> str:
    return '\n'.join([f"{key}:{game[key]}" for key in game])


def isFullTeam(game: {}) -> bool:
    return all([game[x] for x in game])


def isInTeam(game: {}, name: str) -> bool:
    return not all([game[x] != name for x in game])


@on_command('开车', aliases=('组队', '王者组队'), only_to_me=False)
async def createTeam(session: CommandSession):
    global game
    game = {'打野': None, '中单': None, '战士': None, '辅助': None, '射手': None}
    await session.send('[CQ:at,qq=all] 开车啦开车啦，大家快上车啦。')


@on_command('打野', only_to_me=False)
async def jungle(session: CommandSession):
    global game
    if game['打野'] == None:
        bot = nonebot.get_bot()
        member = await bot.get_group_member_info(group_id=session.ctx['group_id'], user_id=session.ctx['user_id'])
        name = member['card'] or member['nickname']
        if isInTeam(game, name):
            await session.send('你已经在车上了哦，不可以坐两个位置！贪心鬼（*╹▽╹*）')
            return
        game['打野'] = name
        await session.send(f'野王上车成功，当前队伍:\n{echoTeam(game)}')
    else:
        await session.send(f'上车失败，已经有野王啦，要不要试一试别的位置呀，当前队伍:\n{echoTeam(game)}')
    if isFullTeam(game):
        await session.send(f'开车成功，快进入游戏吧！当前队伍:\n{echoTeam(game)}')


@on_command('战士', aliases=('边路', '上单',), only_to_me=False)
async def warrior(session: CommandSession):
    global game
    if game['战士'] == None:
        bot = nonebot.get_bot()
        member = await bot.get_group_member_info(group_id=session.ctx['group_id'], user_id=session.ctx['user_id'])
        name = member['card'] or member['nickname']
        if isInTeam(game, name):
            await session.send('你已经在车上了哦，不可以坐两个位置！贪心鬼（*╹▽╹*）')
            return
        game['战士'] = name
        await session.send(f'边路霸主上车成功，当前队伍:\n{echoTeam(game)}')
    else:
        await session.send(f'上车失败，已经有边路霸主啦，要不要试一试别的位置呀，当前队伍:\n{echoTeam(game)}')
    if isFullTeam(game):
        await session.send(f'开车成功，快进入游戏吧！当前队伍:\n{echoTeam(game)}')


@on_command('中单', only_to_me=False)
async def mage(session: CommandSession):
    global game
    if game['中单'] == None:
        bot = nonebot.get_bot()
        member = await bot.get_group_member_info(group_id=session.ctx['group_id'], user_id=session.ctx['user_id'])
        name = member['card'] or member['nickname']
        if isInTeam(game, name):
            await session.send('你已经在车上了哦，不可以坐两个位置！贪心鬼（*╹▽╹*）')
            return
        game['中单'] = name
        await session.send(f'中单法王上车成功，当前队伍:\n{echoTeam(game)}')
    else:
        await session.send(f'上车失败，已经有中单法王啦，要不要试一试别的位置呀，当前队伍:\n{echoTeam(game)}')
    if isFullTeam(game):
        await session.send(f'开车成功，快进入游戏吧！当前队伍:\n{echoTeam(game)}')


@on_command('辅助', aliases=('坦克',), only_to_me=False)
async def tank(session: CommandSession):
    global game
    if game['辅助'] == None:
        bot = nonebot.get_bot()
        member = await bot.get_group_member_info(group_id=session.ctx['group_id'], user_id=session.ctx['user_id'])
        name = member['card'] or member['nickname']
        if isInTeam(game, name):
            await session.send('你已经在车上了哦，不可以坐两个位置！贪心鬼（*╹▽╹*）')
            return
        game['辅助'] = name
        await session.send(f'最强辅助上车成功，当前队伍:\n{echoTeam(game)}')
    else:
        await session.send(f'上车失败，已经有最强辅助啦，要不要试一试别的位置呀，当前队伍:\n{echoTeam(game)}')
    if isFullTeam(game):
        await session.send(f'开车成功，快进入游戏吧！当前队伍:\n{echoTeam(game)}')


@on_command('射手', only_to_me=False)
async def shooter(session: CommandSession):
    global game
    if game['射手'] == None:
        bot = nonebot.get_bot()
        member = await bot.get_group_member_info(group_id=session.ctx['group_id'], user_id=session.ctx['user_id'])
        name = member['card'] or member['nickname']
        if isInTeam(game, name):
            await session.send('你已经在车上了哦，不可以坐两个位置！贪心鬼（*╹▽╹*）')
            return
        game['射手'] = name
        await session.send(f'无敌射手上车成功，当前队伍:\n{echoTeam(game)}')
    else:
        await session.send(f'上车失败，已经有无敌射手啦，要不要试一试别的位置呀，当前队伍:\n{echoTeam(game)}')
    if isFullTeam(game):
        await session.send(f'开车成功，快进入游戏吧！当前队伍:\n{echoTeam(game)}')


@on_command('换位置', only_to_me=False)
async def changePlace(session: CommandSession):
    global game
    inpt = session.state.get('message') or session.current_arg
    args = inpt.strip()
    bot = nonebot.get_bot()
    member = await bot.get_group_member_info(group_id=session.ctx['group_id'], user_id=session.ctx['user_id'])
    name = member['card'] or member['nickname']
    if args not in game:
        await session.send('对不起哦，你想换的位置不存在。')
        return
    if not isInTeam(game, name):
        await session.send('对不起哦，当前您不在我们的小车车上。')
        return
    for x in game:
        if game[x] == name:
            game[x] = None
    game[args] = name
    await session.send(f'换位置成功！当前队伍:\n{echoTeam(game)}')


@on_command('下车', only_to_me=False)
async def leaveGame(session: CommandSession):
    global game
    bot = nonebot.get_bot()
    member = await bot.get_group_member_info(group_id=session.ctx['group_id'], user_id=session.ctx['user_id'])
    name = member['card'] or member['nickname']
    if isInTeam(game, name):
        for x in game:
            if game[x] == name:
                game[x] = None
        await session.send('下车成功。')
