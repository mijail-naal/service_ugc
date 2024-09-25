from abc import ABC, abstractmethod
from typing import Any


class BaseBrokerService(ABC):
    @abstractmethod
    def create_topic(self, *args, **kwargs) -> None:
        pass

    @abstractmethod
    def send_message(self, *args, **kwargs) -> None:
        pass


class BaseStorage(ABC):
    @abstractmethod
    def get(self, *args, **kwargs) -> dict[str, Any] | bool:
        pass

    @abstractmethod
    def insert(self, *args, **kwargs) -> bool:
        pass

    @abstractmethod
    def update(self, *args, **kwargs) -> bool:
        pass

    @abstractmethod
    def delete(self, *args, **kwargs) -> bool:
        pass
