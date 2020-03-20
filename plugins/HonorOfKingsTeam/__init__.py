import nonebot
from nonebot import on_command, CommandSession, permission
from nonebot import on_natural_language, NLPSession, IntentCommand
import random

__plugin_name__ = '王者组队'
__plugin_usage__ = r"""
命令如下：
/开车 或 /[王者|空]组队 会创建一个空的队伍
艾特我并且发送位置可以上车
位置有：打野 中单 战士 辅助 射手
"""

game = {}


def echoTeam(game: {}) -> str:
    return '\n'.join([f"{key}:{game[key]}" for key in game])


def isFullTeam(game: {}) -> bool:
    return all([game[x] for x in game])


@on_command('开车', aliases=('组队', '王者组队'), only_to_me=False)
async def createTeam(session: CommandSession):
    game = {'打野': None, '中单': None, '战士': None, '辅助': None, '射手': None}
    await session.send('[CQ:at,qq=all]开车啦开车啦，大家快上车啦。')


@on_command('打野')
async def jungle(session: CommandSession):
    if game['打野'] is None:
        bot = nonebot.get_bot()
        member = await bot.get_group_member_info(group_id=session.ctx['group_id'], user_id=session.ctx['user_id'])
        game['打野'] = member['card'] or member['nickname']
        await session.send(f'野王上车成功，当前队伍:\n{echoTeam(game)}')
    else:
        await session.send(f'上车失败，已经有野王啦，要不要试一试别的位置呀，当前队伍:\n{echoTeam(game)}')

    if isFullTeam(game):
        await session.send(f'开车成功，快进入游戏吧！当前队伍:\n{echoTeam(game)}')


@on_command('战士')
async def warrior(session: CommandSession):
    if game['战士'] is None:
        bot = nonebot.get_bot()
        member = await bot.get_group_member_info(group_id=session.ctx['group_id'], user_id=session.ctx['user_id'])
        game['战士'] = member['card'] or member['nickname']
        await session.send(f'边路霸主上车成功，当前队伍:\n{echoTeam(game)}')
    else:
        await session.send(f'上车失败，已经有边路霸主啦，要不要试一试别的位置呀，当前队伍:\n{echoTeam(game)}')

    if isFullTeam(game):
        await session.send(f'开车成功，快进入游戏吧！当前队伍:\n{echoTeam(game)}')


@on_command('中单')
async def mage(session: CommandSession):
    if game['中单'] is None:
        bot = nonebot.get_bot()
        member = await bot.get_group_member_info(group_id=session.ctx['group_id'], user_id=session.ctx['user_id'])
        game['中单'] = member['card'] or member['nickname']
        await session.send(f'中单法王上车成功，当前队伍:\n{echoTeam(game)}')
    else:
        await session.send(f'上车失败，已经有中单法王啦，要不要试一试别的位置呀，当前队伍:\n{echoTeam(game)}')

    if isFullTeam(game):
        await session.send(f'开车成功，快进入游戏吧！当前队伍:\n{echoTeam(game)}')


@on_command('辅助', aliases=('坦克',))
async def tank(session: CommandSession):
    if game['辅助'] is None:
        bot = nonebot.get_bot()
        member = await bot.get_group_member_info(group_id=session.ctx['group_id'], user_id=session.ctx['user_id'])
        game['辅助'] = member['card'] or member['nickname']
        await session.send(f'最强辅助上车成功，当前队伍:\n{echoTeam(game)}')
    else:
        await session.send(f'上车失败，已经有最强辅助啦，要不要试一试别的位置呀，当前队伍:\n{echoTeam(game)}')

    if isFullTeam(game):
        await session.send(f'开车成功，快进入游戏吧！当前队伍:\n{echoTeam(game)}')


@on_command('射手')
async def shooter(session: CommandSession):
    if game['射手'] is None:
        bot = nonebot.get_bot()
        member = await bot.get_group_member_info(group_id=session.ctx['group_id'], user_id=session.ctx['user_id'])
        game['射手'] = member['card'] or member['nickname']
        await session.send(f'无敌射手上车成功，当前队伍:\n{echoTeam(game)}')
    else:
        await session.send(f'上车失败，已经有无敌射手啦，要不要试一试别的位置呀，当前队伍:\n{echoTeam(game)}')

    if isFullTeam(game):
        await session.send(f'开车成功，快进入游戏吧！当前队伍:\n{echoTeam(game)}')
