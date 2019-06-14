class DataBlock:

    def __init__(self):
        self.__words = [1, 1, 1, 1]

    def store_data(self, data_array):
        self.__words = data_array

    def print_block(self):
        for data in self.__words:
            print(data)

