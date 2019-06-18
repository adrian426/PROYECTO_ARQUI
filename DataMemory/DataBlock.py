class DataBlock:

    def __init__(self, init_value):
        self.__words = [init_value, init_value, init_value, init_value]

    def store_data(self, data_array):
        self.__words = data_array

    def print_block(self):
        for data in self.__words:
            print(data)

