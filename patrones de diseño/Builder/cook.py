from pizza_builder import MargheritaBuilder,PizzaBuilder

class Cook:

    def make_pizza(self, builder:PizzaBuilder):
        builder.set_dough()
        builder.set_sauce()
        builder.set_topping()
        return builder.pizza
