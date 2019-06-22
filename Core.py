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
        self.__Sub = SUB.SUB(self)

    def run(self):
        while self.__finish:
            self.context_switch()
            self.__cpu_instance.wait(self.__core_id)

            instruction_to_execute = self.get_instruction_to_execute(self.PC)
            instruction_to_print = str(self.hilillo_id) + " owner " + str(self.__core_id)
            print(instruction_to_print + " instruction " + instruction_to_execute.instruction_to_string())
            # Test to execute LW instruction
            # lw_exec = LW(self, instruction_to_execute)
            # print("Iteracion # ", iterator, "del nucleo # ", self.__core_id)

    def decode(self, instruction):
        instruction_code = instruction[0]
        if instruction_code == 19:
            self.__addi.execute(instruction)
        elif instruction_code == 71:
            pass
        elif instruction_code == 83:
            pass
        elif instruction_code == 72:
            pass
        elif instruction_code == 56:
            pass
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

    # if the instruction block is not cached, proceeds to load it.
    # Returns the instruction to be executed
    def get_instruction_to_execute(self, mem_add):
        # no se si quieren guardar como atributo de clase la instruccion que se esta ejecutando.
        if not self.instructionCache.get_if_mem_address_is_cached(mem_add):
            instruction_block = self.__cpu_instance.get_main_memory().get_instruction_block(mem_add)
            self.instructionCache.store_block_in_cache("C", mem_add, instruction_block)
        return self.instructionCache.get_block(self.instructionCache.get_block_index(mem_add)).get_instruction(mem_add)

    def increment_PC(self):
        self.PC += 4

    def exec_instruction(self):
        pass
    # ToDo Metodo para ejecutar la instrucción, que va a llamar al decoder y a ejecutar la instruccion dependiendo
    #  de cual es

    # Method to set the cycles that the core will have to wait to load next instruction and release the locks
    def set_instruction_system_clock_cycles(self, clock_cycles):
        for i in range(0, clock_cycles):
            self.__cpu_instance.wait()

    # ***********************************************LOCKS***********************************************

    # Method to acquire the lock of the data memory bus
    def acquire_data_bus(self):
        return self.__cpu_instance.acquire__lock(0)

    # Method to acquire the lock of the instruction memory bus
    def acquire_instruction_bus(self):
        return self.__cpu_instance.acquire__lock(1)

    # Method to acquire the lock of self cache
    def acquire_self_cache(self):
        return self.__cpu_instance.acquire__lock(self.__core_id + 2)

    # Method to acquire the lock of the other core cache
    def acquire_other_core_cache(self):
        if self.__core_id == 0:
            result = self.__cpu_instance.acquire__lock(3)
        else:
            result = self.__cpu_instance.acquire__lock(2)
        return result

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

    # Try to acquire the self cache and data bus lock
    def acquire_self_cache_and_data_bus_locks(self):
        if self.acquire_self_cache():
            if self.acquire_data_bus():
                return True
            else:
                self.release_self_cache()
        return False

    # Try to acquire the self cache, other core cache, and the dara bus
    def acquire_both_caches_and_data_bus_locks(self):
        if self.acquire_self_cache():
            if self.acquire_other_core_cache():
                if self.acquire_data_bus():
                    return True
                else:
                    self.release_other_core_cache()
                    self.release_self_cache()
            else:
                self.release_self_cache()
        return False

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

    def finish_execution(self):
        self.__finish = True

