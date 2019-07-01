from Model.HililloStatistics import HililloStatistics
class CoreStatistics:

    def __init__(self, core_id):
        self.__id = core_id
        self.__hilillos = {}
        self.__cache_misses = 0
        self.__memory_access_hits = 0
        self.__avg_miss = 0

    #Agrega las estadisticas de cada hilillo y hace un update de si ya estaban
    def add_hilillo_statistics(self, hilillo: HililloStatistics):
        if hilillo.get_id() in self.__hilillos:
            hilillo_temp: HililloStatistics = self.__hilillos[hilillo.get_id()]
            hilillo.add_cycles(hilillo_temp.cycles)
            hilillo.add_runs(1)
            self.__hilillos[hilillo.get_id()] = hilillo
        else:
            self.__hilillos[hilillo.get_id()] = hilillo

    def increase_cache_miss(self):
        self.__cache_misses += 1

    def increase_memory_access_hits(self):
        self.__memory_access_hits += 1

    def avg_cache_miss(self):
        self.__avg_miss = self.__cache_misses / self.__memory_access_hits

    def print(self):
        print("Core " + str(self.__id))
        for hilillo in self.__hilillos:
            print("Hilillo " + str(hilillo) + "   Repeticiones: ")
            self.__hilillos[hilillo].print()
        print("Tasa de fallos: " + str(self.__cache_misses) + "\n Avg (fallos/memoria): " + str(self.__avg_miss))
