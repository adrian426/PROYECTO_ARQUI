# coding=utf-8
from InstructionMemory.InstructionBlock import InstructionBlock

# Clase para la memoria de instrucciones
class InstructionMemory:

    # Constructor que inicializa la lista con los valores
    def __init__(self):
        self.__instruction_block_array = []
        self.__next_word = 0
        self.__block_amount = 0

    # Método para cargar todos los bloques de instrucciones de la memoria principal
    # Recibe la instruccion a insertar
    def store_instruction(self, instruction):
        # Se calcula el numero de bloque
        block_number = self.__next_word / 16

        if block_number == self.__block_amount:
            self.__instruction_block_array[block_number].insert_instruction(instruction)
        else:
            # Se crea un nuevo bloque y se agrega
            instruction_block = InstructionBlock()
            instruction_block.insert_instruction(instruction)
            self.__instruction_block_array.append(instruction_block)
            # Se incrementa la cantidad de bloques
            self.__block_amount += 1

        # Se incrementa en 4 para la siguiente instruccion
        self.__next_word += 4

    # Función para imprimir el bloque
    def print_instruction_block(self, index):
        self.__instruction_block_array[index].print_block()
