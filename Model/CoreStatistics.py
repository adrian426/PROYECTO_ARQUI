class CoreStatistics:

    def __init__(self, core_id):
        self.id = core_id
        self.hilillos = {}
        self.cache_misses = 0
        self.memory_access_hits = 0
        self.avg_miss = 0

    def add_hilillo(self, hilillo_id):
        if hilillo_id in self.hilillos:
            self.hilillos[hilillo_id] += 1
        else:
            self.hilillos[hilillo_id] = 1

    def increase_cache_miss(self):
        self.cache_misses += 1

    def increase_memory_access_hits(self):
        self.memory_access_hits += 1

    def avg_cache_miss(self):
        self.avg_miss = self.cache_misses / self.memory_access_hits

    def print(self):
        print("Core " + str(self.id))
        for hilillo in self.hilillos:
            print("Hilillo " + hilillo + "   Repeticiones: " + self.hilillos[hilillo])
        print("Tasa de fallos: " + self.cache_misses + "\n Avg (fallos/memoria): " + self.avg_miss)
