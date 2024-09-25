from abc import ABC, abstractmethod


class BaseBrokerService(ABC):
    @abstractmethod
    def create_topic(self, *args, **kwargs) -> None:
        pass

    @abstractmethod
    def send_message(self, *args, **kwargs) -> None:
        pass
