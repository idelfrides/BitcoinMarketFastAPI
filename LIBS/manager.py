from random import randint
from typing import List


def gen_randint_list(quant: int, min_limit: int, max_limit: int) -> List[int]:
    """_summary_

    Args:
        quant (int): _description_
        min_limit (int): _description_
        max_limit (int): _description_

    Returns:
        List[int]: _description_
    """
    
    result_list = []
    
    while len(result_list) < quant:
        result_list.append(randint(min_limit, max_limit))
        
    return result_list