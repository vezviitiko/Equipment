from random import shuffle
from typing import Dict, List, Tuple
import psycopg2

from data import get_random_mac, get_random_types


class DataBaseException(Exception):
    pass


class DataBase:
    def __init__(self, host: str, database: str, login: str, passwd: str):
        """
        Объект для работы с базой, postgresql требуется
        :param host - адрес машины, где база:
        :param database - имя самой базы, база должна существовать:
        :param login - логин учетки:
        :param passwd - пароль учетки:
        """
        self.__hostname = host
        self.__database = database
        self.__login = login
        self.__passwd = passwd

        try:
            self.__connection()
        except:
            raise DataBaseException("No Connection to DataBase")

    def __connection(self):
        self.__db = psycopg2.connect(
            host=self.__hostname,
            dbname=self.__database,
            user=self.__login,
            password=self.__passwd,
        )

    @staticmethod
    def __create_list_device(count: int, start: int) -> List[Tuple[int, str, str]]:
        return [(index, get_random_mac(), get_random_types()) for index in range(start, start + count)]

    def __get_id_last_row_in_table(self, table: str) -> int:
        cursor = self.__db.cursor()
        cursor.execute(f"SELECT id FROM {table} ORDER BY id DESC LIMIT 1")
        item = cursor.fetchone()
        if item is None:
            return 0
        else:
            return item[0]

    def create_count_device(self, count: int = 10):
        start: int = self.__get_id_last_row_in_table('devices') + 1
        devices: List[Tuple[int, str, str]] = self.__create_list_device(count, start)
        cursor = self.__db.cursor()
        cursor.executemany("INSERT INTO devices (id, dev_id, dev_type) VALUES (?, ?, ?)", devices)
        self.__db.commit()
        ids: List[int] = list(range(start, start + count))
        shuffle(ids)
        start = self.__get_id_last_row_in_table('endpoints') + 1
        used_ids: List[Tuple[int, int]] = [(index, ids[index - start], ) for index in range(start, start + count // 2)]
        cursor.executemany("INSERT INTO endpoints (id, device_id) VALUES (?, ?)", used_ids)
        self.__db.commit()

    def get_group_dev_type(self) -> Dict[str, int]:
        cursor = self.__db.cursor()
        cursor.execute("""
            SELECT dev_type, COUNT(dev_type) FROM devices 
            WHERE id NOT IN (SELECT device_id FROM endpoints)
            GROUP BY dev_type;
        """)

        result: Dict[str, int] = dict()
        for item in cursor.fetchall():
            result[item[0]] = item[1]

        return result
