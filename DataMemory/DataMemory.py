from DataMemory.DataBlock import DataBlock

class DataMemory:

    def __init__(self):
        self.__data_memory = []

    def initialize_memory(self):
        for i in range(0, 24):
            self.__data_memory[i] = DataBlock(1)

    def get_memory_block(self, block_index):
        return self.__data_memory[block_index]

    def store_memory_block(self, block_index, block):
        self.__data_memory[block_index] = block

