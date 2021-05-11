from abc import ABC, abstractmethod


class BaseLoader(ABC):
    @abstractmethod
    def fetch(self):
        pass

    @abstractmethod
    def parse(self):
        pass

    @abstractmethod
    def load(self):
        pass
