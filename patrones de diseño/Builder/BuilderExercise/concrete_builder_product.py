from builder_interface_product import ProductBuilderInterface
from producto import PC

class ConcretePCBuilder(ProductBuilderInterface):

    def __init__(self)->None:
        self.pc = PC()

    def set_cpu(self, cpu: str):
        self.pc.cpu = cpu
        return self   

    def set_ram(self, ram: str):
        self.pc.ram = ram
        return self

    def set_storage(self, storage: str):
        self.pc.storage = storage
        return self

    def set_gpu(self, gpu: str):
        self.pc.gpu = gpu
        return self

    def build(self) -> PC:
        return self.pc