from Model import HililloStatistics, CoreStatistics

class SimulationStatistics:

    def __init__(self):
        self.__coreStatistics0 = CoreStatistics.CoreStatistics(0)
        self.__coreStatistics1 = CoreStatistics.CoreStatistics(1)

    def addStatistics(self, hililloStatistics: HililloStatistics.HililloStatistics):
        pass

    def getCoreStatistics(self, core_id):
        if core_id == 0:
            return self.__coreStatistics0
        else:
            return self.__coreStatistics1

    def printStatistics(self):
        pass
