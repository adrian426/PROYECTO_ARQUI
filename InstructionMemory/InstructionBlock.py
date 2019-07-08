from InstructionMemory.Instruction import Instruction

# Initial memory direction of the instruction memory
INITIAL_DIR = 384


class InstructionBlock:

    def __init__(self):
        self.__words = [Instruction(), Instruction(), Instruction(), Instruction()]
        self.__word_counter = 0

    # Method to insert a instruction on a block
    def insert_instruction(self, instruction):
        # Check if the instruction can be inserted
        if self.__word_counter >= 4:
            raise TypeError("No se pueden insertar mas de 4 instrucciones en un bloque")
        self.__words[self.__word_counter].set_instruction_values(instruction)
        self.__word_counter += 1

    # Method to get a instruction, receive the PC of the instruction
    def get_instruction(self, pc):
        # Check if the PC is greater than 384
        if pc < INITIAL_DIR:
            raise TypeError("Se recibio un PC de una instruccion que no existe")

        # Change the PC to get the direction in the instruction memory
        pc_function = (pc % 16) // 4

        # Check if the instruction exists
        if pc_function > self.__word_counter:
            raise TypeError("Se solicito una instruccion que no existe")

        # Return the isntruction
        return self.__words[pc_function]

    # Method to print the block
    def print_block(self):
        for instruction in self.__words:
            instruction.print_instruction()
