import redis
from typing import Dict, Union

from data import is_annagrams


class RedisDataBaseException(Exception):
    pass


class RedisDataBase:
    def __init__(self, host: str, port: int):
        """
        Объект - подключение к редису, редис должен быть установлен и настроен
        :param host - имя или адрес хоста с редисом:
        :param port - порт, который слушает редис:
        """
        self.__hostname = host
        self.__port = port

        try:
            self.__initialize()
        except:
            raise RedisDataBaseException('No Connection to Redis')
        self.__key: str = 'count'
        self.__redis.set(self.__key, '0')

    def __initialize(self):
        self.__redis = redis.Redis(host=self.__hostname, port=self.__port)

    def check(self, s1: str, s2: str) -> Dict[str, Union[bool, int]]:
        result: Dict[str, Union[bool, int]] = dict()
        result['is_anagram'] = is_annagrams(s1, s2)
        if result['is_anagram']:
            self.__redis.set(self.__key, str(int(self.__redis.get(self.__key)) + 1))
        result['count'] = int(self.__redis.get(self.__key))

        return result
