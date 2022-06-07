from random import choice
from re import sub
from typing import List


types: List[str] = ['emeter', 'zigbee', 'lora', 'gsm']


def get_random_types() -> str:
    return choice(types)


def get_random_mac(count: int = 6) -> str:
    chars = '1234567890abcdef'
    return ''.join([choice(chars) for unused in range(count)])


def is_annagrams(s1: str, s2: str) -> bool:
    return sorted(list(sub(r'[^\w\d]', '', s1.lower()))) == sorted(list(sub(r'[^\w\d]', '', s2.lower())))

