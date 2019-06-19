from Core import Core
from PCBDataStructure import PCBDataStructure
from MainMemory import MainMemory
from threading import Barrier, Lock


class CPU:

    def __init__(self):
        self.__pcb = PCBDataStructure()
        self.threads_barrier = Barrier(2)
        self.__system_main_memory = MainMemory(self.__pcb)
        self.__core0 = Core(0, self.__pcb, self)
        self.__core1 = Core(1, self.__pcb, self)

        self.__system_clock = 0

        # bus datos, bus instrucciones, cache 0, cache 1
        self.__locks = [Lock(), Lock(),Lock(),Lock()]


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

    def acquire__lock(self, lock_index):
        self.__locks[lock_index].acquire(False)

    def release_locks(self, lock_indexes):
        for index in lock_indexes:
            self.__locks[index].release()

    def get_pcb_ds(self):
        return self.__pcb

    def get_main_memory(self):
        return self.__system_main_memory
