from InstructionMemory.Instruction import Instruction


class InstructionBlock:

    def __init__(self):
        self.__words = [Instruction(), Instruction(), Instruction(), Instruction()]

    def initialize_instructions(self, instructions):
        instructions_iterator = 0
        for instruction in instructions:
            self.__words[instructions_iterator].set_instruction_values(instruction)
            instructions_iterator += 1

    def print_block(self):
        for instruction in self.__words:
            instruction.print()
