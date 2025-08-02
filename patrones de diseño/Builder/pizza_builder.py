from pizza import Pizza

class PizzaBuilder:

    def set_dough(self, dough:str)->None:
        raise NotImplementedError

    def set_sauce(self, sauce:str)->None:
        raise NotImplementedError 

    def set_topping(self, topping:str)->None:
        raise NotImplementedError

class MargheritaBuilder(PizzaBuilder):

    def __init__(self):
        self.pizza = Pizza()

    def set_dough(self):
        self.pizza.dough = 'Regular'

    def set_sauce(self):
        self.pizza.sauce = 'Tomate'

    def set_topping(self):
        self.pizza.topping = 'Mozzarella'