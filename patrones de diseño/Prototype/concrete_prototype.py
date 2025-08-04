from prototype import Prototype
import copy

class SystemConfigPrototype(Prototype):

    def __init__(self, configuration):
        self.configuration = configuration

    def clone(self)->'SystemConfigPrototype':
        return copy.deepcopy(self)