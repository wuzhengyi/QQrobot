from typing import Dict

import header
pokeNameEng = ['xiaoladae', 'guisi', 'miaomiaoe', 'heianya', 'chounie',
               'mengyao', 'dailubi', 'guisitong', 'niula', 'galagalagui', 'banjila', 'genggui', 'xuelabi']
pokeNameChn = ['小拉达(恶)', '鬼斯', '喵喵(恶)', '黑暗鸦', '臭泥(恶)',
               '梦妖', '戴鲁比', '鬼斯通', '纽拉', '嘎啦嘎啦(鬼)', '班吉拉', '耿鬼', '雪拉比']
pokemonProb = [0.2, 0.2, 0.109, 0.12, 0.12,
                0.07, 0.07, 0.06, 0.03, 0.02, 0.0005, 0.0005, 0]

catchProb = {header.PokeLevel.D: {'evelsBall': 0.4, 'superBall': 0.8, 'masterBall': 1.0},
             header.PokeLevel.C: {'evelsBall': 0.3, 'superBall': 0.6, 'masterBall': 1.0},
             header.PokeLevel.B: {'evelsBall': 0.25, 'superBall': 0.5, 'masterBall': 1.0},
             header.PokeLevel.A: {'evelsBall': 0.2, 'superBall': 0.4, 'masterBall': 1.0},
             header.PokeLevel.S: {'evelsBall': 0.05, 'superBall': 0.1, 'masterBall': 1.0}}

escapeProb = {header.PokeLevel.D: 0.2, header.PokeLevel.C: 0.3,
              header.PokeLevel.B: 0.4, header.PokeLevel.A: 0.1, header.PokeLevel.S: 0.01}

enterCost = 5

name = '百鬼夜行'