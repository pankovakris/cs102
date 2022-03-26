# type: ignore
import typing as tp

import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry


class Session:
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
        self.base_url = base_url
        self.timeout = timeout
        self.session = requests.Session()
        adapter = HTTPAdapter(max_retries=max_retries)
        self.session.mount("https://", adapter)

    def get(self, url: str, *args: tp.Any, **kwargs: tp.Any) -> requests.Response:

        if "timeout" in kwargs:
            self.timeout = kwargs["timeout"]
        return self.session.get(self.base_url + "/" + url, timeout=self.timeout, *args, **kwargs)

    def post(self, url: str, *args: tp.Any, **kwargs: tp.Any) -> requests.Response:

        if "timeout" in kwargs:
            self.timeout = kwargs["timeout"]
        return self.session.post(self.base_url + "/" + url, timeout=self.timeout, *args, **kwargs)
