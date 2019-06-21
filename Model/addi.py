class Addi:
    def __init__(self, register1, register2, immediate):
        self.__register1 = register1
        self.__register2 = register2
        self.__immediate = immediate

    def execute(self):
        return self.__immediate + self.__register2