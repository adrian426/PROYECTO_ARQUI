# Clase para la memoria de instrucciones
class InstructionMemory:

    # Constructor que inicializa la lista con los valores
    def __init__(self):
        self.__instructionArray = [1, 2, 3, 4, 5, 6, 7, 8, 9]

    # Función para obtener el valor en el arreglo
    def get_instruction(self, index):
        return self.__instructionArray[index]
