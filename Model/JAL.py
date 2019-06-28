import sys
sys.path.append("..")  # Adds higher directory to python modules path.
import Core


# Class to execute the ADDI instruction
class JAL:

    # Receives the core instance, and the instruction to execute
    def __init__(self, core_instance: Core):
        self.__core_instance = core_instance

    # Start the execution
    def execute(self, instruction):
        current_pc = self.__core_instance.get_PC()
        # register1 <- PC
        self.__core_instance.set_register(instruction.get_instruction()[1], current_pc)
        # PC = PC + inmediate
        self.__core_instance.change_PC_by_instruction(current_pc + instruction.get_instruction()[3])