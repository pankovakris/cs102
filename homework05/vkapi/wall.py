# type: ignore
import textwrap
import time
import typing as tp
from string import Template

import pandas as pd
import requests
from pandas import json_normalize
from vkapi import config, session
from vkapi.exceptions import APIError


def get_posts_2500(
    owner_id: str = "",
    domain: str = "",
    offset: int = 0,
    count: int = 10,
    max_count: int = 2500,
    filter: str = "owner",
    extended: int = 0,
    fields: tp.Optional[tp.List[str]] = None,
) -> tp.Dict[str, tp.Any]:
    pass


def get_wall_execute(
    owner_id: str = "",
    domain: str = "",
    offset: int = 0,
    count: int = 10,
    max_count: int = 2500,
    filter: str = "owner",
    extended: int = 0,
    fields: tp.Optional[tp.List[str]] = None,
    progress=None,
) -> pd.DataFrame:
    """
    Возвращает список записей со стены пользователя или сообщества.
    @see: https://vk.com/dev/wall.get
    :param owner_id: Идентификатор пользователя или сообщества, со стены которого необходимо получить записи.
    :param domain: Короткий адрес пользователя или сообщества.
    :param offset: Смещение, необходимое для выборки определенного подмножества записей.
    :param count: Количество записей, которое необходимо получить (0 - все записи).
    :param max_count: Максимальное число записей, которое может быть получено за один запрос.
    :param filter: Определяет, какие типы записей на стене необходимо получить.
    :param extended: 1 — в ответе будут возвращены дополнительные поля profiles и groups, содержащие информацию о пользователях и сообществах.
    :param fields: Список дополнительных полей для профилей и сообществ, которые необходимо вернуть.
    :param progress: Callback для отображения прогресса.
    """

    mas = []
    sess = session.Session(config.VK_CONFIG["domain"])
    for i in range(0, count, 200):
        code1 = f"""
                    return API.wall.get ({{
                    "owner_id": "{owner_id}",
                    "domain": "{domain}",
                    "offset": {i},
                    "count": "200",
                    "filter": "{filter}",
                    "extended": "0",
                    "fields": ""
        }});
        """
        data = {
        "code": code1,
        "access_token": config.VK_CONFIG["token"],
        "v": config.VK_CONFIG["version"]
        }
        response = sess.post("execute", data=data).json()
        for i in response["response"]["items"]:
            mas.append(i)
        time.sleep(0.33)
    return json_normalize(mas)
