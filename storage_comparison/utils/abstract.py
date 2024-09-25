from abc import ABC, abstractmethod


class AbstractStorage(ABC):
    @abstractmethod
    def _execute_query(self, *args, **kwargs) -> None:
        pass

    @abstractmethod
    def create_table(self, *args, **kwargs) -> None:
        pass

    @abstractmethod
    def drop_table(self, *args, **kwargs) -> None:
        pass

    @abstractmethod
    def add(self, *args, **kwargs) -> None:
        pass

    @abstractmethod
    def read(self, *args, **kwargs) -> None:
        pass
