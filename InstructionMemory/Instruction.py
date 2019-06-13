class Instruction:

    def __init__(self):
        self.__instruction = []

    def set_instruction_values(self, instruction_array):
        self.__instruction = instruction_array

    def print(self):
        print(self.__instruction)
