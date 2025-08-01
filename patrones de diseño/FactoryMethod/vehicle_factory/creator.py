from abc import ABC, abstractmethod
from .product import Vehicle

class VehicleFactory(ABC):
    @abstractmethod

    def get_vehicle(self, vehicle_type:str)->Vehicle:
        pass