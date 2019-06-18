from Core import Core
from PCBDataStructure import PCBDataStructure
from MainMemory import MainMemory


class CPU:

    def __init__(self):
        self.__pcb = PCBDataStructure()
        self.__system_main_memory = MainMemory(self.__pcb)
        self.__core0 = Core(0, self.__pcb)
        self.__core1 = Core(1, self.__pcb)

    # Se inician los cores
    def start_cores(self):
        self.__core0.start()
        self.__core1.start()
