from abc import ABC, abstractmethod
from typing import List

from models.gpu import Gpu
from models.server import Server


class AbstractGpuCacheRepository(ABC):
    @abstractmethod
    def gpu_get_all() -> List[Gpu]:
        raise NotImplementedError


class AbstractServerCacheRepository(ABC):
    @abstractmethod
    def server_get_all() -> List[Server]:
        raise NotImplementedError
