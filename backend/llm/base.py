from abc import ABC,abstractclassmethod

class BaseLLM(ABC) :
    @abstractclassmethod
    def analyze(self, content : str):
        pass