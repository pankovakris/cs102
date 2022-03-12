# type: ignore
import dataclasses
import math
import time
import typing as tp

import requests
from vkapi import config, session
from vkapi.exceptions import APIError

QueryParams = tp.Optional[tp.Dict[str, tp.Union[str, int]]]


@dataclasses.dataclass(frozen=True)
class FriendsResponse:
    count: int
    items: tp.Union[tp.List[int], tp.List[tp.Dict[str, tp.Any]]]


def get_friends(
    user_id: int,
    count: int = 5000,
    offset: int = 0,
    fields: tp.Optional[tp.List[str]] = None,
) -> FriendsResponse:
    """
    Получить список идентификаторов друзей пользователя или ра
    сширенную информацию
    о друзьях пользователя (при использовании параметра fields).
    :param user_id: Идентификатор пользователя, список друзей для которого нужно получить.
    :param count: Количество друзей, которое нужно вернуть.
    :param offset: Смещение, необходимое для выборки определенного подмножества друзей.
    :param fields: Список полей, которые нужно получить для каждого пользователя.
    :return: Список идентификаторов друзей пользователя или список пользователей.
    """
    req = requests.get(
        config.VK_CONFIG["domain"] + "friends.get",
        params={
            "access_token": config.VK_CONFIG["token"],
            "v": config.VK_CONFIG["version"],
            "user_id": user_id,
            "count": count,
            "offset": offset,
            "fields": fields,
        },
    )
    data = req.json()["response"]["items"]
    if fields is None:
        friend_counts = len(data)
    else:
        friend_counts = len(data[0])

    return FriendsResponse(friend_counts, data)


class MutualFriends(tp.TypedDict):
    id: tp.Optional[int]
    common_friends: tp.List[int]
    common_count: int


def get_mutual(
    source_uid: tp.Optional[int] = None,
    target_uid: tp.Optional[int] = None,
    target_uids: tp.Optional[tp.List[int]] = None,
    order: str = "",
    count: tp.Optional[int] = None,
    offset: int = 0,
    progress=None,
) -> tp.Union[tp.List[int], tp.List[MutualFriends]]:
    """
    Получить список идентификаторов общих друзей между парой пользователей.
    :param source_uid: Идентификатор пользователя, чьи друзья пересекаются с друзьями пользователя с идентификатором target_uid.
    :param target_uid: Идентификатор пользователя, с которым необходимо искать общих друзей.
    :param target_uids: Cписок идентификаторов пользователей, с которыми необходимо искать общих друзей.
    :param order: Порядок, в котором нужно вернуть список общих друзей.
    :param count: Количество общих друзей, которое нужно вернуть.
    :param offset: Смещение, необходимое для выборки определенного подмножества общих друзей.
    :param progress: Callback для отображения прогресса.
    """
    result = []
    if target_uids is not None:
        for i in target_uids:
            req = requests.get(
                config.VK_CONFIG["domain"] + "friends.getMutual",
                params={
                    "access_token": config.VK_CONFIG["token"],
                    "v": config.VK_CONFIG["version"],
                    "source_uid": source_uid,
                    "target_uid": i,
                    "order": order,
                    "count": count,
                    "offset": offset,
                },
            ).json()
            print(req)
            result.append(
                MutualFriends(
                    id=i,
                    common_friends=req["response"],
                    common_count=len(req["response"]),
                )
            )
        return result
    else:
        req = requests.get(
            config.VK_CONFIG["domain"] + "friends.getMutual",
            params={
                "access_token": config.VK_CONFIG["token"],
                "v": config.VK_CONFIG["version"],
                "source_uid": source_uid,
                "target_uid": target_uid,
                "order": order,
                "count": count,
                "offset": offset,
            },
        ).json()
        return [
            MutualFriends(
                id=source_uid,
                common_friends=req["response"],
                common_count=len(req["response"]),
            )
        ]
