import nonebot
from nonebot import on_command, CommandSession
from os import path
import random
from .data_source import Pokemon, State, GameList, Choice

__plugin_name__ = '宝可梦'
__plugin_usage__ = r"""
欢迎来到精灵宝可梦的世界
回复“开始游戏”即可开始寻找你的伙伴哦。
根据选项回复A B C D即可。
"""

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

@on_command('D', aliases=('Ｄ',),only_to_me=False)
async def chooseD(session: CommandSession):
    global GameList
    QQ = session.ctx['user_id']
    if QQ in GameList:
        game = GameList[QQ]
        message = game.next(Choice.D)
        await session.send(message)

@on_command('发群公告', aliases=('悬赏',),only_to_me=False)
async def groupNotice(session: CommandSession):
    global GameList
    groupID = session.ctx['group_id']
    if groupID not None:
        bot = nonebot.get_bot()
        bot._send_group_notice(groupID, '悬赏', '悬赏内容111111111111111111111111111111111111111')