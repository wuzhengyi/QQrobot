from typing import Dict

import header
pokeNameEng = ['xiaolada', 'bobo', 'miaomiao', 'wasidan', 'apashe',
               'dashetou', 'pikaqiu', 'pipi', 'pangding', 'yibu', 'jilidan', 'dailong', 'menghuan']
pokeNameChn = ['小拉达', '波波', '喵喵', '瓦斯弹', '阿柏蛇',
               '大舌头', '皮卡丘', '皮皮', '胖丁', '伊布', '吉利蛋', '袋龙', '梦幻']
pokemonProb = [0.19, 0.19, 0.1, 0.1, 0.1, 0.07999,
                0.05, 0.05, 0.05, 0.05, 0.02, 0.02, 0.00001]

catchProb = {header.PokeLevel.D: {'evelsBall': 0.4, 'superBall': 0.8, 'masterBall': 1.0},
             header.PokeLevel.C: {'evelsBall': 0.3, 'superBall': 0.6, 'masterBall': 1.0},
             header.PokeLevel.B: {'evelsBall': 0.25, 'superBall': 0.5, 'masterBall': 1.0},
             header.PokeLevel.A: {'evelsBall': 0.2, 'superBall': 0.4, 'masterBall': 1.0},
             header.PokeLevel.S: {'evelsBall': 0.05, 'superBall': 0.1, 'masterBall': 1.0}}

escapeProb = {header.PokeLevel.D: 0.1, header.PokeLevel.C: 0.15,
              header.PokeLevel.B: 0.2, header.PokeLevel.A: 0.1, header.PokeLevel.S: 0.01}
