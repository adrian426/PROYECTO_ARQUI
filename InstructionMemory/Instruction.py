class Instruction:

    def __init__(self):
        self.__instruction = []

    # Method to set the instruction values
    def set_instruction_values(self, instruction_array):
        # Check if the data size is correct
        if len(instruction_array) != 4:
            raise TypeError("Se recibio una instruccion con una cantidad incorrecta de bytes")
        # Store the instruction
        self.__instruction = instruction_array

    # Method to get the instruction array
    def get_instruction(self):
        return self.__instruction

    # Method to print the instruction
    def print_instruction(self):
        print(self.__instruction)

    # Method to get a string with the instruction values
    def instruction_to_string(self):
        return str(self.__instruction)