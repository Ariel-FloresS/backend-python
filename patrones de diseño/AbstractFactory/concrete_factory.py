from abstract_factory import UIAbstractFactory, Button, TextBox

class Darkbutton(Button):

    def paint(self):
        print('Dark Button')

class DarkTextBox(TextBox):

    def paint(self):
        print('Dark text Box')

class LightButton(Button):

    def paint(self):
        print('light button')

class LightTextBox(TextBox):

    def paint(self):
        print('Light Text Box')


class DarkUIFactory(UIAbstractFactory):

    def create_button(self):
        return Darkbutton()

    def create_textbox(self):
        return DarkTextBox()


class LightUIFactory(UIAbstractFactory):

    def create_button(self):
        return LightButton()

    def create_textbox(self):
        return LightTextBox()
