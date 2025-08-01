from .concrete_factory import CarFactory, TruckFactory
from .creator import VehicleFactory

def client_vehicle_code(factory:VehicleFactory, vehicle_type:str):
    vehicle = factory.get_vehicle(vehicle_type = vehicle_type)
    print(vehicle.deliver())