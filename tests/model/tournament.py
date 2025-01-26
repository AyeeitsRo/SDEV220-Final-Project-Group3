from abc import ABC, abstractmethod 

class Tournament(ABC):
    def __init__(self, name, date, time):
        self.name = name
        self.date = date
        self.time = time


    @abstractmethod
    def schedule(self):
        pass

    @abstractmethod
    def displaylive(self):
        pass

    @abstractmethod
    def results(self):
        pass
