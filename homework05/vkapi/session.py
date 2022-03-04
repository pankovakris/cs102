import typing as tp

import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry


class Session(requests.Session):
    """
    Сессия.

    :param base_url: Базовый адрес, на который будут выполняться запросы.
    :param timeout: Максимальное время ожидания ответа от сервера.
    :param max_retries: Максимальное число повторных запросов.
    :param backoff_factor: Коэффициент экспоненциального нарастания задержки.
    """

    def __init__(
        self,
        base_url: str,
        timeout: float = 5.0,
        max_retries: int = 3,
        backoff_factor: float = 0.3,
    ) -> None:
        self.timeout = timeout
        self.max_retries = max_retries
        self.backoff_factor = backoff_factor
        self.base_url = base_url
        self.retries = Retry(total=max_retries, backoff_factor=0.3)
        self.adapter = HTTPAdapter(max_retries=self.retries)
        self.mount("https://", self.adapter)
        self.mount("http://", self.adapter)

    def get(self, url, **kwargs: tp.Any) -> requests.Response:
        if url is None:
            url = self.base_url
        return requests.get(str(url))

    def post(self, url, data=None, json=None, **kwargs: tp.Any) -> requests.Response:
        if url is None:
            url = self.base_url
        if json is not None:
            return requests.post(url, data=json.dumps(param_dict))
        else:
            return requests.post(url, data=data)
