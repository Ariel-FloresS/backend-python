
from abc import ABC, abstractmethod

class Vehicle(ABC):

    @abstractmethod
    def deliver(self):
        pass

class Car(Vehicle):

    def __init__(self, model:str)->None:
        self._model = model 


    def deliver(self)->str:
        return f'Auto: {self._model} entregado'

class Truck(Vehicle):

    def __init__(self,  model:str)->None:

        self._model = model

    def deliver(self)->None:
        return f"Camion: {self._model} entregado"