import time

from publicServer.DataCollector.Commands import Command
from publicServer.config.constants import ONE_MINUTE
from datetime import datetime


class APIInvoker:
    def __init__(self):
        self.commands = []

    def register(self, command):
        self.commands.append(command)

    def execute(self):
        for command in self.commands:
            print(command.execute())

        while True:
            time.sleep(ONE_MINUTE)
            for command in self.commands:
                command: Command
                if command.isExpired():
                    print(command.execute())
                    command.last_executed = datetime.now()

