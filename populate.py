from datetime import datetime
from aiohttp import ClientSession
from asyncio import gather, run 
from random import randint
from typing import List

# from LIBS.manager import gen_randint_list
# from UTILS import SYMBOLS, PERSON_NAMES

from databases.init_db import create_database
from services import UserService, FavoriteService


USER_NAMES = [
    "João", "Maria", "José", "Ana", "Pedro", "Paula", "Carlos", "Fernanda", "Lucas", "Juliana", "Marcos", "Amanda", "Rafael", "Camila", "Bruno", "Beatriz", "Gabriel", "Mariana", "Felipe", "Larissa", "Matheus", "Sofia", "Guilherme", "Vitória", "Leonardo", "Isabela", "André", "Letícia", "Ricardo", "Daniela"
]

SYMBOLS = [
    'BTC', 'ETH', 'BNB', 'USDT', 'ADA', 'SOL', 'XRP', 'DOT', 'DOGE', 'USDC', 'LUNA', 'AVAX', 'SHIB', 'LINK', 'UNI', 'LTC', 'ALGO', 'XLM', 'VET', 'ICP', 'AXS', 'FIL', 'TRX', 'ETC', 'ATOM', 'XTZ', 'FTT', 'XMR', 'EGLD', 'THETA'
]


def gen_randint_list(quant: int, min_limit: int, max_limit: int) -> List[int]:
    """#### Generate a list of random integers values

    Args:
        quant (int): Quantity of values to be genarated
        min_limit (int): the minimum limit of interval
        max_limit (int): the maximum limit of interval

    Returns:
        List[int]: the result list of random integers
    """
    
    result_list = []
    
    while len(result_list) < quant:
        result_list.append(randint(min_limit, max_limit))
        
    return result_list


async def populate():
    quantity = 10
    random_index = gen_randint_list(quantity, 1, 29)
    await create_database()
    await gather(*[
        UserService.create_user(name=USER_NAMES[i]) 
        for i in random_index
    ])

    tasks = []
    for i in range(1, quantity + 1):
        random_index = gen_randint_list(quantity, 1, 29)
        tasks += [
            FavoriteService.add_favorite(user_id=i, symbol=SYMBOLS[j]) 
            for j in random_index[:7]
        ]
        
    await gather(*tasks)
    

run(populate())
