from Model.HililloStatistics import HililloStatistics
class CoreStatistics:

    def __init__(self, core_id):
        self.__id = core_id
        self.__hilillos = {}
        self.__cache_misses = 0
        self.__memory_access_hits = 0
        self.__avg_miss = 0

    # Agrega las corridas de cada hilillo en los cores
    def add_hilillo_runs(self, hilillo_id):
        if hilillo_id in self.__hilillos:
            self.__hilillos[hilillo_id] += 1
        else:
            self.__hilillos[hilillo_id] = 1


    def add_hilillo_statistics(self, hilillo: HililloStatistics):
        if hilillo in self.__hilillos:
            hilillo_temp:HililloStatistics = self.__hilillos[hilillo.get_id()]
            pass
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
            print("Hilillo " + hilillo + "   Repeticiones: " + self.__hilillos[hilillo])
        print("Tasa de fallos: " + self.__cache_misses + "\n Avg (fallos/memoria): " + self.__avg_miss)
