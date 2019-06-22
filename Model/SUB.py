import sys
sys.path.append("..")  # Adds higher directory to python modules path.
import Core

# Class to execute the ADDI instruction
class SUB:

    # Receives the core instance, and the instruction to execute
    def __init__(self, core_instance: Core):
        self.__core_instance = core_instance

    # Start the execution
    def execute(self, instruction):
        result = self.__core_instance.get_register_value(instruction[2]) \
                 - self.__core_instance.get_register_value(instruction[3])
        self.__core_instance.set_register(instruction[1], result)
        self.__core_instance.set_instruction_system_clock_cycles(1)
        self.__core_instance.decrement_quantum()
