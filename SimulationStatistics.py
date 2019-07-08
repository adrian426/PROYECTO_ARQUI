from Model import HililloStatistics, CoreStatistics

class SimulationStatistics:

    def __init__(self):
        self.__coreStatistics0 = CoreStatistics.CoreStatistics(0)
        self.__coreStatistics1 = CoreStatistics.CoreStatistics(1)
        self.__hilillos = {}
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

    #Adds or updates statistics of each hilillo
    def add_hilillo_statistics(self, hilillo: HililloStatistics):
        if hilillo.get_id() != -1:
            if hilillo.get_id() in self.__hilillos:
                hilillo_temp: HililloStatistics = self.__hilillos[hilillo.get_id()]
                hilillo_temp.add_cycles(hilillo.cycles)
                hilillo_temp.add_runs(hilillo.core)
                self.__hilillos[hilillo.get_id()] = hilillo_temp
            else:
                self.__hilillos[hilillo.get_id()] = hilillo

    #prints statistics of the whole simulation
    def print_statistics(self):
        print("\n ------------------------------------------------------\n"
              "Estadisticas de la simulacion \n "
              "------------------------------------------------------\n")
        for hilillo in self.__hilillos:
            self.__hilillos[hilillo].print()
        self.__coreStatistics0.print()
        print("Cache Data2WACache")
        self.cache0.print()
        print("\n ------------------------------------------------------\n")
        self.__coreStatistics1.print()
        print("Cache Data2FACache")
        self.cache1.print()
        print("\n ------------------------------------------------------\n")
        print("Data memory:\n")
        self.__data_memory.print()
