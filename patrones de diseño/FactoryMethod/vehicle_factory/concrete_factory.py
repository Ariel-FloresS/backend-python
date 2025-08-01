from .creator import VehicleFactory
from .product import Car,Truck

class CarFactory(VehicleFactory):

    def get_vehicle(self, vehicle_type:str)->Car:
        return Car(model = vehicle_type)

class TruckFactory(VehicleFactory):

    def get_vehicle(self, vehicle_type:str)->Truck:
        return Truck(model = vehicle_type)
