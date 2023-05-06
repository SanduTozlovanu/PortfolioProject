from datetime import datetime, timedelta
from abc import ABC, abstractmethod


class Command(ABC):
    def __init__(self, interval: int, priority: int, rate_cost: int):
        self.interval = interval  # in seconds
        self.priority = priority
        self.rate_cost = rate_cost
        self.last_executed = datetime.now()

    def isExpired(self):
        return datetime.now() - timedelta(seconds=self.interval) > self.last_executed

    @abstractmethod
    def execute(self):
        pass
