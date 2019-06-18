from Core import Core
from PCBDataStructure import PCBDataStructure
from MainMemory import MainMemory
from threading import Barrier


class CPU:

    def __init__(self):
        self.__pcb = PCBDataStructure()
        self.threads_barrier = Barrier(2)
        self.__system_main_memory = MainMemory(self.__pcb)
        self.__core0 = Core(0, self.__pcb, self)
        self.__core1 = Core(1, self.__pcb, self)

        self.__system_clock = 0

    # Metodo para la barrera e incrementar el relog del sistema
    def wait(self, core_id):
        print("Waiting", core_id)
        barrier_thread_id = self.threads_barrier.wait()
        print(barrier_thread_id)
        if barrier_thread_id == 0:
            self.__system_clock += 1

    # Se inician los cores
    def start_cores(self):
        self.__core0.start()
        self.__core1.start()
