from abc import ABC, abstractmethod
from producto import PC


class ProductBuilderInterface(ABC):

    @abstractmethod
    def set_cpu(self,cpu:str)->None:
        raise NotImplementedError
    
    @abstractmethod
    def set_ram(self,ram:str)->None:
        raise NotImplementedError
    
    @abstractmethod
    def set_storage(self,storage:str)->None:
        raise NotImplementedError
    
    @abstractmethod
    def set_gpu(self, gpu:str)->None:
        raise NotImplementedError
    
    @abstractmethod
    def build(self)->PC:
        raise NotImplementedError
    
    