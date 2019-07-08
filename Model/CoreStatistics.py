from Model.HililloStatistics import HililloStatistics
class CoreStatistics:

    def __init__(self, core_id):
        self.__id = core_id
        self.__hilillos = {}
        self.__cache_misses = 0
        self.__memory_access_hits = 0
        self.__avg_miss = 0.0

    def increase_cache_miss(self):
        self.__cache_misses += 1

    def increase_memory_access_hits(self):
        self.__memory_access_hits += 1

    def avg_cache_miss(self):
        if self.__memory_access_hits != 0:
            self.__avg_miss = self.__cache_misses / float(self.__memory_access_hits)

    def print(self):
        self.avg_cache_miss()
        print("\nCore " + str(self.__id)+"\n-----------------")
        print("\nTasa de fallos: " + str(self.__cache_misses) + "\n Avg (fallos/memoria): " + str(self.__avg_miss))
