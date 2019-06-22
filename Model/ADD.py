from Core import Core

# Class to execute the ADDI instruction
class ADD:

    # Receives the core instance, and the instruction to execute
    def __init__(self, core_instance: Core, instruction):
        self.__core_instance = core_instance
        self.__instruction = instruction

    # Start the execution
    def execute(self):
        result = self.__core_instance.get_register_value(self.__instruction[2]) \
                 + self.__core_instance.get_register_value(self.__instruction[3])
        self.__core_instance.set_register(self.__instruction[1], result)
