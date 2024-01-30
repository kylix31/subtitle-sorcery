from abc import ABC, abstractmethod


class Command(ABC):
    """
    The Command interface declares a method for executing a command.
    """

    @abstractmethod
    def execute(self):
        """
        The execute method is where the logic of the command will be implemented.
        Each concrete command will provide its own implementation of this method.
        """
        pass
