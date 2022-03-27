# type: ignore
import dataclasses
import math
import time
import typing as tp

import requests
from vkapi.config import VK_CONFIG
from vkapi.exceptions import APIError
from vkapi.session import Session

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
    fields = ", ".join(fields) if fields else ""
    query = f"friends.get?access_token={VK_CONFIG['token']}&user_id={user_id}&fields={fields}&count={count}&v={VK_CONFIG['version']}"
    domain = VK_CONFIG["domain"]
    sess = Session(f"{domain}")
    result = sess.get(query)
    friend_counts = result.json()["response"]["count"]
    data = result.json()["response"]["items"]
    return FriendsResponse(friend_counts, data)


class MutualFriends(tp.TypedDict):
    id: int
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
    sess = Session(VK_CONFIG["domain"])
    result = []
    if target_uids is not None:
        for i in target_uids:
            query = f"friends.getMutual?access_token={VK_CONFIG['token']}&source_uid={source_uid}&target_uid={i}&order={order}&count={count}&offset={offset}&v={VK_CONFIG['version']}"
            req = sess.get(query).json()
            print(req)
            result.append(
                MutualFriends(
                    id=i,
                    common_friends=req["response"],
                    common_count=len(req["response"]),
                )
            )
            time.sleep(0.34)
        return result
    else:
        url = f"friends.getMutual?access_token={VK_CONFIG['token']}&source_uid={source_uid}&target_uid={target_uid}&order={order}&count={count}&offset={offset}&v={VK_CONFIG['version']}"
        req = sess.get(url).json()
        return req["response"]
