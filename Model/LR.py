# Class to execute the LR instruction
class LR:

    # Receives the core instance, and the instruction to execute
    def __init__(self, core_instance, instruction):
        self.__core_instance = core_instance
        self.__instruction = instruction

        # Start the execution
