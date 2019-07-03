from DataMemory.DataBlock import DataBlock

class DataMemory:

    def __init__(self):
        self.__data_memory = []

    def initialize_memory(self):
        for i in range(0, 24):
            self.__data_memory.append(DataBlock(1))

    def get_memory_block(self, block_index):
        return self.__data_memory[block_index]

    def store_memory_block(self, memory_address, block):
        self.__data_memory[int(memory_address/16)] = block

    def print(self):
        for i, block in self.__data_memory:
            print("Block number " + str(i))
            block.print_block()