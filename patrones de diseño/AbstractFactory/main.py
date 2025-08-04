from concrete_factory import DarkUIFactory, LightUIFactory
from abstract_factory import UIAbstractFactory


def client_code(factory: UIAbstractFactory)-> None:

    button = factory.create_button()
    text_box = factory.create_textbox()

    button.paint()
    text_box.paint()


if __name__ == '__main__':
    client_code(DarkUIFactory())
    client_code(LightUIFactory())