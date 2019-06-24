from Core import Core
from PCBDataStructure import PCBDataStructure
from MainMemory import MainMemory
from threading import Barrier, Lock


class CPU:

    def __init__(self):
        self.__pcb = PCBDataStructure()
        self.threads_barrier = Barrier(2)
        self.__system_main_memory = MainMemory(self.__pcb)
        # Hay que preguntar para que ingresen en valor del quantum
        self.__core0 = Core(0, self)
        self.__core1 = Core(1, self)
        self.__system_clock = 0
        self.__default_quantum = 20
        self.__core_finished = False

        # bus datos, bus instrucciones, cache 0, cache 1
        self.__locks = [Lock(), Lock(), Lock(), Lock()]

    # Metodo para la barrera e incrementar el relog del sistema
    def wait(self):
        if not self.__core_finished:
            # print("Waiting", core_id)
            barrier_thread_id = self.threads_barrier.wait()
            # print(barrier_thread_id)
            if barrier_thread_id == 0:
                self.__system_clock += 1
        else:
            self.__system_clock += 1

    # Se inician los cores
    def start_cores(self):
        self.__core0.start()
        self.__core1.start()

    def acquire__lock(self, lock_index):
        return self.__locks[lock_index].acquire(False)

    def release_lock(self, lock_index):
        self.__locks[lock_index].release()

    def release_locks(self, acquired_locks):
        for index in range(0, 4):
            if acquired_locks[index]:
                self.__locks[index].release()

    def get_pcb_ds(self):
        return self.__pcb

    def get_main_memory(self):
        return self.__system_main_memory

    # Method to invalidate
    # Receives the number of the core (0 or 1), and the memory_address of the block to change,
    # and the new state of that block
    def change_state_of_block_on_core_cache(self, core, memory_address, new_state):
        if core == 0:
            self.__core0.change_cache_block_state(memory_address, new_state)
        else:
            self.__core1.change_cache_block_state(memory_address, new_state)

    # Return if the memory address its on the other core cache
    def get_if_mem_address_is_on_core_cache(self, core, memory_address):
        if core == 0:
            return self.__core0.get_if_mem_address_is_on_self_cache(memory_address)
        else:
            return self.__core1.get_if_mem_address_is_on_self_cache(memory_address)

    # Return the state of the memory address block on the core cache
    def get_state_of_mem_address_on_core(self, core, memory_address):
        if core == 0:
            return self.__core0.get_memory_address_state_on_cache(memory_address)
        else:
            return self.__core1.get_memory_address_state_on_cache(memory_address)

    # Method to store the cache block of the core on the main memory
    def store_data_cache_block_on_mm_on_core(self, memory_address, cache_block_new_state, core):
        if core == 0:
            return self.__core0.store_data_cache_block_on_main_mem(memory_address, cache_block_new_state)
        else:
            return self.__core1.store_data_cache_block_on_main_mem(memory_address, cache_block_new_state)

    # Method to invalidate RL on core, assumes that core has both cores and data bus locks
    def invalidate_rl_on_core(self, mem_address, core):
        if core == 0:
            return self.__core0.invalidate_self_rl(mem_address)
        else:
            return self.__core1.invalidate_self_rl(mem_address)

    # Method to set core finished bool to true
    def notify_core_finished(self):
        self.__core_finished = True

    # Method to get the default quantum
    def get_default_quantum(self):
        return self.__default_quantum
