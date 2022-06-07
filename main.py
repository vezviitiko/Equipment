import sys
from aiohttp import web
from typing import Dict

from database import DataBaseException, DataBase
from redis_db import RedisDataBaseException, RedisDataBase

routes = web.RouteTableDef()
database: DataBase
redis: RedisDataBase


@routes.post('/redis')
async def redis_post_handler(request: web.Request):
    args = await request.post()
    s1: str = args.get('value1')
    s2: str = args.get('value2')
    result = redis.check(s1, s2)
    return web.json_response(result)


@routes.get('/database/get')
async def database_get_handler(request: web.Request):
    items: Dict[str, int] = database.get_group_dev_type()
    return web.json_response(items)


@routes.post('/database/post')
async def database_post_handler(request: web.Request):
    args = await request.post()
    count = args.get('count')
    if count is None or not isinstance(count, int) or count <= 0:
        count = 10
    database.create_count_device(count)
    return web.Response(status=201)


if __name__ == '__main__':
    try:
        # Прописать параметры нужные для подключения к postgresql
        database: DataBase = DataBase(host='', database='', login='', passwd='')
    except DataBaseException as error:
        print(error)
        sys.exit(error)

    try:
        # Прописать параметры нужные для подключения к redis
        redis: RedisDataBase = RedisDataBase(host='localhost', port=6379)
    except RedisDataBaseException as error:
        print(error)
        sys.exit(error)

    app = web.Application()
    app.add_routes(routes)

    web.run_app(app)
