from InstructionMemory.InstructionBlock import InstructionBlock

# Initial memory direction of the instruction memory
INITIAL_DIR = 384


class InstructionMemory:

    # Constructor to initialize the memory
    def __init__(self):
        self.__instruction_block_array = []
        self.__next_word = 0
        self.__block_amount = 0

    # Method to load all the hilillos instructions
    # Receives the instruction to insert
    def store_instruction(self, instruction):
        # Get the block number
        block_number = self.__next_word // 16

        # First instruction case
        if len(self.__instruction_block_array) == 0:
            # Creates a new block
            instruction_block = InstructionBlock()
            self.__instruction_block_array.append(instruction_block)

        if block_number == self.__block_amount:
            self.__instruction_block_array[block_number].insert_instruction(instruction)
        else:
            # Creates a new block
            instruction_block = InstructionBlock()
            instruction_block.insert_instruction(instruction)
            self.__instruction_block_array.append(instruction_block)
            # Increase the block amount
            self.__block_amount += 1

        # Increases the next word direction by 4
        self.__next_word += 4

    # Function to get a instruction block
    def get_instruction_block(self, pc):
        # Set the PC direction to the instruction memory real index
        pc_function = pc - INITIAL_DIR

        # Check the PC
        if pc_function % 4 != 0:
            raise TypeError("Se recibio un PC que no es multiplo de 4")
        # Check if the block exists
        if pc_function >= self.__next_word:
            raise TypeError("Se solicito una instruccion que no existe, direccion: " + str(pc))
        # Check if it is greater than 0
        if pc_function < 0:
            raise TypeError("El PC solicitado no corresponde a una direccion de la memoria de instrucciones")
        # Return the instruction block
        return self.__instruction_block_array[pc_function // 16]

    # Function to get a specific instruction
    def get_instruction(self, pc):
        # Set PC
        pc_function = pc - INITIAL_DIR

        # Check the PC
        if pc_function % 4 != 0:
            raise TypeError("Se recibio un PC que no es multiplo de 4")
        # Check if exists
        if pc_function >= self.__next_word:
            raise TypeError("Se solicito una instruccion que no existe, direccion: " + str(pc))
        # Check if it is greater than 0
        if pc_function < 0:
            raise TypeError("El PC solicitado no corresponde a una direccion de la memoria de instrucciones")
        # Return the instruction
        return self.__instruction_block_array[pc_function // 16].get_instruction(pc)

    # Function to print a block
    def print_instruction_block(self, index):
        self.__instruction_block_array[index].print_block()
