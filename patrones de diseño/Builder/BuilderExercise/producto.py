class PC:
    def __init__(self):
        self.cpu = None
        self.ram = None
        self.storage = None
        self.gpu = None

    def __str__(self):
        return (f"PC configurada con: CPU={self.cpu}, RAM={self.ram}, "
                f"Storage={self.storage}, GPU={self.gpu}")
