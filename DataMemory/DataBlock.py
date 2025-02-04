class DataBlock:

    def __init__(self, init_value):
        self.__words = [init_value, init_value, init_value, init_value]

    # Method to set block data as a copy of other block
    def copy_data_block(self, data_block):
        result_array = []
        data_block_array = data_block.get_words()
        for index in data_block_array:
            result_array.append(index)
        self.__words = result_array

    def get_words(self):
        return self.__words

    def print_block(self):
        print(self.__words)

    def change_word_value(self, mem_address, value):
        self.__words[int((mem_address % 16)/4)] = value

    def get_value(self, index):
        return self.__words[index]

    def print(self, index):
        values = "Valores del bloque " + str(index) + ": "
        for word in self.__words:
            values = values + " " + str(word)
        print(values)