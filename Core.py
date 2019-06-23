from Caches.Data2WACache import Data2WACache
from Caches.DataFACache import DataFACache
from DataMemory.DataBlock import DataBlock
from InstructionMemory.Instruction import Instruction
from Caches.InstructionsCache import InstructionsCache
from PCB import PCB
from threading import Thread
from Model import ADD, ADDI, DIV, LR, LW, MUL, SC, SUB, SW


class Core(Thread):

    def __init__(self, cache_type: int, PCBStructure, cpu_instance, quantum_val):
        self.__core_id = cache_type
        self.__cpu_instance = cpu_instance
        self.__finish = False

        # Constructor del thread
        Thread.__init__(self)

        # Se crea le bloque de datos que se le va a apasar a todos los bloques
        data_block = DataBlock(0)

        # Dependiendo del tipo de cache se inicializa
        if cache_type == 0:
            self.dataCache = Data2WACache(data_block)
        elif cache_type == 1:
            self.dataCache = DataFACache(data_block)
        else:
            raise TypeError("Unknown Value for cache type.")

        # Se inicializa la cache de instrucciones
        instruction = Instruction()
        instruction.set_instruction_values([0, 0, 0, 0])
        self.instructionCache = InstructionsCache(instruction)
        self.hilillo_id = -1
        self.register = []
        self.PC = 0
        self.RL = 0
        self.quantum = quantum_val

        #Se inicializa las instrucciones
        self.__add = ADD.ADD(self)
        self.__addi = ADDI.ADDI(self)
        self.__div = DIV.DIV(self)
        self.__mul = MUL.MUL(self)
        self.__sub = SUB.SUB(self)

        # Current core locks
        self.__core_locks = [0, 0, 0, 0]

    def run(self):
        while self.__finish == False:
            self.context_switch()
            while self.quantum != 0:
                self.__cpu_instance.wait(self.__core_id)
                instruction_to_execute = self.get_instruction_to_execute(self.PC)
                instruction_to_print = str(self.hilillo_id) + " owner " + str(self.__core_id)
                print(instruction_to_print + " instruction " + instruction_to_execute.instruction_to_string())
                # Recordar agregar release_all_locks_acquired() cuando implementemos este ciclo

    def decode(self, instruction):
        instruction_code = instruction[0]
        if instruction_code == 19:
            self.__addi.execute(instruction)
        elif instruction_code == 71:
            self.__add.execute(instruction)
        elif instruction_code == 83:
            self.__sub.execute(instruction)
        elif instruction_code == 72:
            self.__mul.execute(instruction)
        elif instruction_code == 56:
            self.__div.execute(instruction)
        elif instruction_code == 5:
            pass
        elif instruction_code == 37:
            pass
        elif instruction_code == 99:
            pass
        elif instruction_code == 100:
            pass
        elif instruction_code == 51:
            pass
        elif instruction_code == 52:
            pass
        elif instruction_code == 111:
            pass
        elif instruction_code == 103:
            pass
        elif instruction_code == 999:
            pass

    # Loads the data from the pcb, used in context switch
    def load_pcb(self):
        pcb_ds = self.__cpu_instance.get_pcb_ds()
        if pcb_ds.get_count() > 0:
            pcb = pcb_ds.dequeuePCB()
            self.register = pcb.get_registers()
            self.PC = pcb.get_pc_address()
            self.hilillo_id = pcb.get_hilillo_id()

    def context_switch(self):
        # No se si se manda PC, depende donde se aumente.
        pcb = PCB(self.hilillo_id, self.PC, self.register)

        # hay que ver si esto funca con la instruccion fin, me parece que no
        # if it's not the first iteration, doesn't store the init value of the core
        if self.hilillo_id != -1:
            # if the quantum hasn't ended, the PCB is added again to the queue.
            if self.quantum != 0:
                self.__cpu_instance.get_pcb_ds().queuePCB(pcb)
            else:
                self.__cpu_instance.get_pcb_ds().queueFinishedPCB(pcb)
        # We call the pcb load function to load the next "hilillo" to execute
        self.load_pcb()

    def decrement_quantum(self):
        self.quantum -= 1

    # if the instruction block is not cached, proceeds to load it.
    # Returns the instruction to be executed
    def get_instruction_to_execute(self, mem_add):
        # no se si quieren guardar como atributo de clase la instruccion que se esta ejecutando.
        if not self.instructionCache.get_if_mem_address_is_cached(mem_add):
            instruction_block = self.__cpu_instance.get_main_memory().get_instruction_block(mem_add)
            self.instructionCache.store_block_in_cache("C", mem_add, instruction_block)
        return self.instructionCache.get_block(self.instructionCache.get_block_index(mem_add)).get_instruction(mem_add)

    # Function to get a data block from main memory
    def get_data_block(self, mem_add):
        if not self.dataCache.get_if_mem_address_is_cached(mem_add):
            data_block = self.__cpu_instance.get_main_memory().get_data_block(mem_add)
            self.dataCache.store_block_in_cache("C", mem_add, data_block)
        return self.dataCache.get_block(self.dataCache.get_block_index(mem_add))

    def set_data_block_main_memory(self, mem_add, data_block):
        self.__cpu_instance.get_main_memory().set_data_block(mem_add, data_block)

    def increment_PC(self):
        self.PC += 4

    # Method to set the cycles that the core will have to wait to load next instruction and release the locks
    def set_instruction_system_clock_cycles(self, clock_cycles):
        for i in range(0, clock_cycles):
            self.__cpu_instance.wait()

    # ***********************************************LOCKS***********************************************

    # Method to acquire the lock of the data memory bus
    def acquire_data_bus(self):
        if self.__cpu_instance.acquire__lock(0):
            self.__core_locks[0] = 1
            return True
        else:
            return False

    # Method to acquire the lock of the instruction memory bus
    def acquire_instruction_bus(self):
        if self.__cpu_instance.acquire__lock(1):
            self.__core_locks[1] = 1
            return True
        else:
            return False

    # Method to acquire the lock of self cache
    def acquire_self_cache(self):
        if self.__cpu_instance.acquire__lock(self.__core_id + 2):
            self.__core_locks[self.__core_id + 2] = 1
            return True
        else:
            return False

    # Method to acquire the lock of the other core cache
    def acquire_other_core_cache(self):
        if self.__core_id == 0:
            if self.__cpu_instance.acquire__lock(3):
                self.__core_locks[3] = 1
                return True
        else:
            if self.__cpu_instance.acquire__lock(2):
                self.__core_locks[2] = 1
                return True
        return False

    # Release locks methods
    def release_data_bus(self):
        self.__cpu_instance.release_lock(0)

    def release_instruction_bus(self):
        self.__cpu_instance.release_lock(1)

    def release_self_cache(self):
        self.__cpu_instance.release_lock(self.__core_id + 2)

    def release_other_core_cache(self):
        if self.__core_id == 0:
            self.__cpu_instance.release_lock(3)
        else:
            self.__cpu_instance.release_lock(2)

    # Method to release all core acquired locks
    def release_all_locks_acquired(self):
        self.__cpu_instance.release_locks(self.__core_locks)

    # ********************************* GET/SET registers and caches *********************************

    # Method to get the value of the memory address on the cache
    def get_data_cache_value(self, memory_address):
        return self.dataCache.get_word_index(memory_address)

    # Method to update a register value
    def set_register(self, register_index, register_value):
        self.register[register_index] = register_value

    # Method to get the register value, receives the register number x1 -> 1
    def get_register_value(self, register_number):
        return self.register[register_number]

    # *********************************************** CACHES ***********************************************

    # Method to change state of cache block
    def change_cache_block_state(self, memory_address, new_state):
        self.dataCache.change_block_state(memory_address, new_state)

    # Method to change the state on other core cache block, receives the memory address, and the new state
    def change_block_state_on_other_core_cache(self, memory_address, new_state):
        self.__cpu_instance.change_state_of_block_on_core_cache(not self.__core_id, memory_address, new_state)

    # Function to get if the memory_address block its stored on self cache
    def get_if_mem_address_is_on_self_cache(self, memory_address):
        return self.dataCache.get_if_mem_address_is_cached(memory_address)

    # Function to get if the memory_address block its stored on other core cache
    def get_if_memory_address_on_other_cache(self, memory_address):
        return self.__cpu_instance.get_if_mem_address_is_on_core_cache(not self.__core_id, memory_address)

    # Function to get the state of the block with the memory address
    def get_memory_address_state_on_cache(self, memory_address):
        return self.dataCache.get_memory_address_block_state(memory_address)

    # Function to get the state of the block with the memory address on the other core cache
    def get_memory_address_state_on_other_cache(self, memory_address):
        return self.__cpu_instance.get_state_of_mem_address_on_core(not self.__core_id, memory_address)

    # Method to store the block on the cache, returns the clock cycles to store
    # ToDo conectar con el metodo de Adrian para guardar un bloque en cache considerando el víctima
    def store_block_on_self_cache(self, state, memory_address, data_block):
        return self.dataCache.store_block_in_cache(state, memory_address, data_block)

    # Method to store the cache block on main memory and change the block state
    def store_data_cache_block_on_main_mem(self, memory_address, cache_block_new_state):
        block_to_store = DataBlock(0)
        block_to_store.copy_data_block(self.dataCache.get_block_mem_address(memory_address))
        # ToDo conectar con el metodo de Bailin
        #  self.__cpu_instance.get_main_memory().store_block(memory_address, block_to_store)
        self.change_cache_block_state(memory_address, cache_block_new_state)
        return block_to_store

    # Method to store a block on other core cache
    def store_other_core_data_cache_block_on_main_memory(self, memory_address, cache_block_new_state):
        return self.__cpu_instance.store_data_cache_block_on_mm_on_core(
            memory_address, cache_block_new_state, not self.__core_id)

    def finish_execution(self):
        self.__finish = True

