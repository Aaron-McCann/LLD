from abc import ABC, abstractmethod

class Coffee(ABC):

    def __init_(self):
        self.description = "unknown coffee"

    def get_description(self):
        return self.description
    
    @abstractmethod
    def get_cost(self)
        pass

    def get_ingredients(self):
        return self.get_description
    

class Espresso(Coffee):
    def __init_(self):
        super().__init__()
        self.description = "Espresso"

    def get_cost(self):
        return 1.99
    

class BlackCofee(Coffee):
    def __init__(self):
        super().__init__()
        self.description = "BlackCofee"

    def get_cost(self):
        return 2