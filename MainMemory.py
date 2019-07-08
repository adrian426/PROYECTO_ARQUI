from InstructionMemory.InstructionMemory import InstructionMemory
from DataMemory.DataMemory import DataMemory
from PCB import PCB
from Utils.FileReader import FileReader

# Instruction memory initial direction
INITIAL_DIR = 384


# System main memory
class MainMemory:

    # Constructor
    def __init__(self, pcb_structure, hilillos_to_run):

        self.__data_memory = DataMemory()
        self.__instruction_memory = InstructionMemory()

        self.__data_memory.initialize_memory()
        self.__file_reader = FileReader(hilillos_to_run)

        # Get all the hilillos names
        hilillos_names = self.__file_reader.get_hilillos_files_list()

        # Set the instructio counter
        instruction_counter = INITIAL_DIR

        # Creates the array and initialize the instruction memory
        for hilillo in hilillos_names:
            instructions_hilillo = self.__file_reader.read_hilillos(hilillo)

            # Initialize the instruction memory
            bytes_added = 0
            for instruction in instructions_hilillo:
                self.__instruction_memory.store_instruction(instruction)
                bytes_added += 4

            # Creates the PCB and insert it on the PCB structure
            register_array = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                              0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

            instruction_pcb = PCB(hilillo, instruction_counter, register_array)

            # Insert the PCB
            pcb_structure.queuePCB(instruction_pcb)

            # Increase the instruction counter
            instruction_counter += bytes_added

    # Method to get a instruction block
    def get_instruction_block(self, pc):
        if pc % 4 != 0:
            raise TypeError("Se recibio un PC que no es multiplo de 4")
        else:
            return self.__instruction_memory.get_instruction_block(pc)

    # Method to get a instruction
    def get_instruction(self, pc):
        if pc % 4 != 0:
            raise TypeError("Se recibio un PC que no es multiplo de 4")
        else:
            return self.__instruction_memory.get_instruction(pc)

    # Method to print a instruction block
    def print_instruction_block(self, block_id):
        self.__instruction_memory.print_instruction_block(block_id)

    # Method to get data block from data memory
    def get_data_block(self, mem_add):
        return self.__data_memory.get_memory_block(int(mem_add/16))

    # Method to set a data block on the data memory
    def set_data_block(self, mem_add, data_block):
        self.__data_memory.store_memory_block(mem_add, data_block)

    # Method to get the data memory
    def get_data_memory(self):
        return self.__data_memory