from InstructionMemory.Instruction import Instruction

class InstructionBlock:
    def __init__(self):
        self.__words = [Instruction(), Instruction(), Instruction(), Instruction()]
        self.__word_counter = 0

    def insert_instruction(self, instruction):
        self.__words[self.__word_counter].set_instruction_values(instruction)
        self.__word_counter += 1

    def print_block(self):
        for instruction in self.__words:
            instruction.print_instruction()