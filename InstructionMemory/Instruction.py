class Instruction:

    def __init__(self):
        self.__instruction = []

    # Metodo para establecer los valores de la instruccion
    def set_instruction_values(self, instruction_array):
        # Se revisa que el tamaño del arreglo que representa la instruccion sea el correcto
        if len(instruction_array) != 4:
            raise TypeError("Se recibio una instruccion con una cantidad incorrecta de bytes")
        # Se guarda la instruccion
        self.__instruction = instruction_array

    # Metodos para imprimir la instruccion
    def print_instruction(self):
        print(self.__instruction)

    def instruction_to_string(self):
        return str(self.__instruction)