from abc import ABC, abstractmethod

class UIAbstractFactory(ABC):

    @abstractmethod
    def create_button(self):
        raise NotImplementedError

    @abstractmethod
    def create_textbox(self):
        raise NotImplementedError

class Button(ABC):

    @abstractmethod
    def paint(self):
        raise NotImplementedError

class TextBox(ABC):

    @abstractmethod
    def paint(self):
        raise NotImplementedError