from pizza_builder import MargheritaBuilder
from cook import Cook

cook = Cook()
margherita_builder = MargheritaBuilder()

pizza = cook.make_pizza(builder = margherita_builder)
print(pizza)

