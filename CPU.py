from Core import Core
from PCBDataStructure import PCBDataStructure
from MainMemory import MainMemory
from threading import Barrier, Lock, Thread
from SimulationStatistics import SimulationStatistics

class CPU:

    def __init__(self, hilillos_to_run, quantum):

        self.__pcb = PCBDataStructure()
        self.threads_barrier = Barrier(2)
        self.__dead_barrier = False
        self.__killing_lock = Lock()  # Lock used to kill the barrier
        self.__waiting_lock = Lock()
        self.__system_main_memory = MainMemory(self.__pcb, hilillos_to_run)
        self.__simulation_statistics = SimulationStatistics()
        self.__core0 = Core(0, self)
        self.__core1 = Core(1, self)
        self.__core_count = 2
        self.running_cores = 2
        self.__system_clock = 0
        self.__default_quantum = quantum
        self.__core_finished = False
        self.__core_finished_counter = 0

        # Data buss, instruction buss, cache 0, cache 1
        self.__locks = [Lock(), Lock(), Lock(), Lock()]
        self.__lock_owner = [-1, -1, -1, -1]

    # Starts the cores for the simulation and prints statistics after the cores are finished
    def start_cores(self):
        self.__core1.start()
        if self.__core_count > 1:
            self.__core0.start()
        thread = Thread(target=self.print_statistics(), args=())
        thread.start()

    # Print the statistics
    def print_statistics(self):
        self.__core0.join()
        self.__core1.join()
        self.__simulation_statistics.add_cache(0, self.__core0.get_data_cache())
        self.__simulation_statistics.add_cache(1, self.__core1.get_data_cache())
        self.__simulation_statistics.add_data_memory(self.__system_main_memory.get_data_memory())
        self.__simulation_statistics.print_statistics()
        print("Simulation Finished")

    # Method to use the barrier
    def wait(self):
        if self.__core_count > 1:
            if not self.__core_finished:
                try:
                    barrier_thread_id = self.threads_barrier.wait()
                    if barrier_thread_id == 0:
                        self.__system_clock += 1
                        print("Ciclo de reloj: " + str(self.__system_clock))
                except:
                    self.__system_clock += 1
                    print("Ciclo de reloj: " + str(self.__system_clock))
            else:
                self.__system_clock += 1
                print("Ciclo de reloj: " + str(self.__system_clock))
                if self.__core_finished_counter == 2:
                    self.__simulation_statistics.add_data_memory(self.__system_main_memory.get_data_memory())

    # Method to kill the barrier
    def kill_barrier(self):
        self.__killing_lock.acquire(True)
        if not self.__dead_barrier:
            self.threads_barrier.abort()
            self.__dead_barrier = True
        self.__killing_lock.release()

    # Method to acquire specific lock
    def acquire__lock(self, lock_index, core_id):
        if self.__locks[lock_index].acquire(False):
            self.__lock_owner[lock_index] = core_id
            return True
        return False

    # Method to release specific lock
    def release_lock(self, lock_index):
        self.__lock_owner[lock_index] = -1
        self.__locks[lock_index].release()

    # Method to release all the locks acquired by the core
    def release_locks(self, core_id):
        for index in range(0, 4):
            if self.__lock_owner[index] == core_id:
                self.__locks[index].release()
                self.__lock_owner[index] = -1

    # Method to get the PCB structure
    def get_pcb_ds(self):
        return self.__pcb

    # Method to get the main memory
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
        if core == 0 or self.__core_count <= 1:
            return self.__core0.get_if_mem_address_is_on_self_cache(memory_address)
        else:
            return self.__core1.get_if_mem_address_is_on_self_cache(memory_address)

    # Return the state of the memory address block on the core cache
    def get_state_of_mem_address_on_core(self, core, memory_address):
        if core == 0 or self.__core_count <= 1:
            return self.__core0.get_memory_address_state_on_cache(memory_address)
        else:
            return self.__core1.get_memory_address_state_on_cache(memory_address)

    # Method to store the cache block of the core on the main memory
    def store_data_cache_block_on_mm_on_core(self, memory_address, cache_block_new_state, core):
        if core == 0 or self.__core_count <= 1:
            return self.__core0.store_data_cache_block_on_main_mem(memory_address, cache_block_new_state)
        else:
            return self.__core1.store_data_cache_block_on_main_mem(memory_address, cache_block_new_state)

    # Method to invalidate RL on core, assumes that core has both cores and data bus locks
    def invalidate_rl_on_core(self, mem_address, core):
        if core == 0 or self.__core_count <= 1:
            return self.__core0.invalidate_self_rl(mem_address)
        else:
            return self.__core1.invalidate_self_rl(mem_address)

    # Method to set core finished bool to true
    def notify_core_finished(self):
        self.__core_finished = True

    # Method to get the default quantum
    def get_default_quantum(self):
        return self.__default_quantum

    # Method to get the simulation statistics
    def get_simulation_statistics(self):
        return self.__simulation_statistics

    # Method to increase the finished cores counter
    def increase_finished_counter(self):
        self.__core_finished_counter += 1
