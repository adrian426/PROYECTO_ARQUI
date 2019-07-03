from Model import HililloStatistics, CoreStatistics

class SimulationStatistics:

    def __init__(self):
        self.__coreStatistics0 = CoreStatistics.CoreStatistics(0)
        self.__coreStatistics1 = CoreStatistics.CoreStatistics(1)
        self.__data_memory = []
        self.cache0 = ""
        self.cache1 = ""

    def getCoreStatistics(self, core_id):
        if core_id == 0:
            return self.__coreStatistics0
        else:
            return self.__coreStatistics1

    def add_data_memory(self, data_memory):
        self.__data_memory = data_memory

    def add_cache(self, cache_type, cache):
        if cache_type == 0:
            self.cache0 = cache
        else:
            self.cache1 = cache

    def print_statistics(self):
        print("\n ------------------------------------------------------\n"
              "Estadisticas de la simulacion \n "
              "------------------------------------------------------")
        self.__coreStatistics0.print()
        print("Cache Data2WACache")
        self.cache0.print()
        print("\n ------------------------------------------------------\n")
        self.__coreStatistics1.print()
        print("Cache Data2FACache")
        self.cache1.print()
        print("Data memory:")
