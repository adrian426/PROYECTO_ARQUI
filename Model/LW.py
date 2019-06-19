# Class to execute the LW instruction
class LW:

    # Receives the core instance, and the instruction to execute
    def __init__(self, core_instance, instruction):
        self.__core_instance = core_instance
        self.__instruction = instruction

        # Start the execution
