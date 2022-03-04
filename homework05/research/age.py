import datetime as dt
import statistics
import typing as tp

from vkapi.friends import get_friends


def age_predict(user_id: int) -> tp.Optional[float]:
    """
    Наивный прогноз возраста пользователя по возрасту его друзей.

    Возраст считается как медиана среди возраста всех друзей пользователя

    :param user_id: Идентификатор пользователя.
    :return: Медианный возраст пользователя.
    """
    friends = get_friends(user_id, 5000, 0, ["city", "bdate"])
    agelist = []
    for i in friends.items:
        try:
            date = i["bdate"].split(".")
            if len(date) == 3:
                agelist.append(2022 - int(date[2]))
        except:
            pass

    return statistics.median(agelist)
