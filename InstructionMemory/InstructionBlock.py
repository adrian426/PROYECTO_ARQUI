from InstructionMemory.Instruction import Instruction

# Direccion inicial de la memoria de instrucciones
INITIAL_DIR = 384


class InstructionBlock:

    def __init__(self):
        self.__words = [Instruction(), Instruction(), Instruction(), Instruction()]
        self.__word_counter = 0

    # Metodo para insertar una instruccion en el bloque
    def insert_instruction(self, instruction):
        # Se revisa que se pueda insertar la instruccion
        if self.__word_counter >= 4:
            raise TypeError("No se pueden insertar mas de 4 instrucciones en un bloque")
        self.__words[self.__word_counter].set_instruction_values(instruction)
        self.__word_counter += 1

    # Metodo para obtener una instruccion, recibe el PC de la instruccion
    def get_instruction(self, pc):
        # Se revisa que el pc recibido sea mayor a 384
        if pc < INITIAL_DIR:
            raise TypeError("Se recibio un PC de una instruccion que no existe")

        # Se adapta el PC para utilizarlo en esta funcion
        pc_function = (pc % 16) // 4

        # Se revisa que la instruccion exista
        if pc_function > self.__word_counter:
            raise TypeError("Se solicito una instruccion que no existe")

        # Se retorna la instruccion
        return self.__words[pc_function]

    def print_block(self):
        for instruction in self.__words:
            instruction.print_instruction()
