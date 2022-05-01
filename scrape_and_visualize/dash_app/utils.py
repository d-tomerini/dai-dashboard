# convenience functions for the dash app
import pandas as pd
from typing import Optional

def age_category(age)-> Optional(str):
    """
    return a classified age to an age bracket
    :param age:
    :return:
    """
    if age is pd.NA:
        return None
    if age <= 20:
        return '0-20'
    if age >= 51:
        return "51+"
    # to avoid stating all cases as 21-30, 31-40, ...
    a = int(age - 1) // 10 * 10
    return f'{a + 1}-{a + 10}'


def format_time(x) -> str:
    """
    From a timestamp in a pandas dataframe, return required format
    :param x:
    :return: formatted string
    """
    if x is pd.NaT:
        return None
    if x.hour == 0:
        return x.strftime("%M.%S,%f")[:-5]
    return x.strftime("%-H:%M.%S,%f")[:-5]
