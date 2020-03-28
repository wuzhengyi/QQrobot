from typing import Dict

import header

pokeNameEng = ['lvmaochong', 'dujiaochong', 'lieque', 'chuanshanshu', 'niduolang', 'niduolan', 'maoqiu', 'liuwei',
               'kabishou', 'xipanmoou', 'kentailuo', 'feitiantanglang', 'dajia', 'miaowazhongzi', 'xiaohuolong',
               'jienigui', 'huoyanniao', 'jidongniao', 'shandianniao', 'chaomeng']
pokeNameChn = ['绿毛虫', '独角虫', '烈雀', '穿山鼠', '尼多朗', '尼多兰', '毛球', '六尾',
               '卡比兽', '吸盘魔偶', '肯泰罗', '飞天螳螂', '大甲', '妙蛙种子', '小火龙', '杰尼龟', '火焰鸟', '急冻鸟', '闪电鸟', '超梦']
pokemonProb = [0.15, 0.15, 0.09, 0.09, 0.09, 0.09, 0.08, 0.07969,
               0.03, 0.03, 0.03, 0.03, 0.03, 0.01, 0.01, 0.01, 0.0001, 0.0001, 0.0001, 0.00001]

catchProb = {header.PokeLevel.D: {'evelsBall': 0.3, 'superBall': 0.8, 'masterBall': 1.0},
             header.PokeLevel.C: {'evelsBall': 0.25, 'superBall': 0.5, 'masterBall': 1.0},
             header.PokeLevel.B: {'evelsBall': 0.2, 'superBall': 0.35, 'masterBall': 1.0},
             header.PokeLevel.A: {'evelsBall': 0.1, 'superBall': 0.25, 'masterBall': 1.0},
             header.PokeLevel.S: {'evelsBall': 0.01, 'superBall': 0.05, 'masterBall': 1.0}}

# escapeProb = {header.PokeLevel.D: 0.15, header.PokeLevel.C: 0.2,
#              header.PokeLevel.B: 0.25, header.PokeLevel.A: 0.1, header.PokeLevel.S: 0.01}
escapeProb = {header.PokeLevel.D: 0.1, header.PokeLevel.C: 0.15,
              header.PokeLevel.B: 0.2, header.PokeLevel.A: 0.1, header.PokeLevel.S: 0.01}

enterCost = 10

name = '沙狐乐园'
