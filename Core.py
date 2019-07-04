from Caches.Data2WACache import Data2WACache
from Caches.DataFACache import DataFACache
from DataMemory.DataBlock import DataBlock
from InstructionMemory.Instruction import Instruction
from Caches.InstructionsCache import InstructionsCache
from PCB import PCB
from threading import Thread
from StatesEnum import StatesEnum
from Model import ADD, ADDI, DIV, LR, LW, MUL, SC, SUB, SW, JAL, JALR, BNE, BEQ
from Model.HililloStatistics import HililloStatistics

INVALID_RL_VALUE = -1

class Core(Thread):

    def __init__(self, cache_type: int, cpu_instance):
        self.__core_id = cache_type
        self.__cpu_instance = cpu_instance

        # Core execution finished
        self.__finished = False

        # Constructor del thread
        Thread.__init__(self)

        # Se crea le bloque de datos que se le va a a pasar a todos los bloques
        data_block = DataBlock(0)

        # Dependiendo del tipo de cache se inicializa
        if cache_type == 0:
            self.data_cache = Data2WACache(data_block)
        elif cache_type == 1:
            self.data_cache = DataFACache(data_block)
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
        self.quantum = 0
        self.__hilillo_finished = True
        self.__cycles = 0

        # Se inicializa las instrucciones
        self.__add = ADD.ADD(self)
        self.__addi = ADDI.ADDI(self)
        self.__div = DIV.DIV(self)
        self.__mul = MUL.MUL(self)
        self.__sub = SUB.SUB(self)
        self.__jal = JAL.JAL(self)
        self.__jalr = JALR.JALR(self)
        self.__bne = BNE.BNE(self)
        self.__beq = BEQ.BEQ(self)
        self.__lw = LW.LW(self)
        self.__sw = SW.SW(self)
        self.__lr = LR.LR(self)
        self.__sc = SC.SC(self)

    def run(self):
        while not self.__finished:
            self.context_switch()
            # if self.PC == 424:
            #     print("")
            # print("PC here " + str(self.PC))
            self.__cycles = 0
            while self.quantum != 0 and self.__hilillo_finished:
                self.__cpu_instance.wait()
                instruction_to_execute = self.get_instruction_to_execute(self.PC)
                self.increment_PC_default()  # increment of the PC after geting the instruction to execute
                instruction_to_print = str(self.hilillo_id) + " owner " + str(self.__core_id)
                self.decode(instruction_to_execute)
                self.set_instruction_system_clock_cycles(1)
                self.release_all_locks_acquired()
                # print(instruction_to_print + " instruction " + instruction_to_execute.instruction_to_string())
                # Recordar agregar release_all_locks_acquired() cuando implementemos este ciclo
            hilillo_statistics = HililloStatistics(self.__core_id, self.hilillo_id, self.register, self.__cycles, self.RL, 1)
            self.__cpu_instance.get_simulation_statistics().getCoreStatistics(self.__core_id).add_hilillo_statistics(hilillo_statistics)
        self.__cpu_instance.increase_finished_counter()

    #decodes and execute the instruction pointed by the PC
    def decode(self, instruction):
        instruction_code = int(instruction.get_instruction()[0])
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
            self.__lw.execute(instruction)
        elif instruction_code == 37:
            self.__sw.execute(instruction)
        elif instruction_code == 99:
            self.__beq.execute(instruction)
        elif instruction_code == 100:
            self.__bne.execute(instruction)
        elif instruction_code == 51:
            self.__lr.execute(instruction)
        elif instruction_code == 52:
            self.__sc.execute(instruction)
        elif instruction_code == 111:
            self.__jal.execute(instruction)
        elif instruction_code == 103:
            self.__jalr.execute(instruction)
        elif instruction_code == 999:
            self.__cpu_instance.wait()
            self.quantum = 0
        self.decrease_quantum()

        if instruction_code != 999:
            if self.quantum == 0:
                self.__hilillo_finished = False

    # Loads the data from the pcb, used in context switch
    def load_pcb(self):
        pcb_ds = self.__cpu_instance.get_pcb_ds()
        if pcb_ds.get_count() > 0:
            pcb = pcb_ds.dequeuePCB()
            self.register = pcb.get_registers()
            self.PC = pcb.get_pc_address()
            self.hilillo_id = pcb.get_hilillo_id()
            self.quantum = self.__cpu_instance.get_default_quantum()
            return True
        return False

    def context_switch(self):
        # No se si se manda PC, depende donde se aumente.
        pcb = PCB(self.hilillo_id, self.PC, self.register)

        # hay que ver si esto funca con la instruccion fin, me parece que no
        # if it's not the first iteration, doesn't store the init value of the core
        if self.hilillo_id != -1:
            # if the quantum hasn't ended, the PCB is added again to the queue.
            if not self.__hilillo_finished:
                self.__cpu_instance.get_pcb_ds().queuePCB(pcb)
            else:
                self.__cpu_instance.get_pcb_ds().queueFinishedPCB(pcb)
            self.__hilillo_finished = True
        # We call the pcb load function to load the next "hilillo" to execute
        if not self.load_pcb():
            # print("Empty PCB structure")
            self.finish_execution()
            self.quantum = 0

    def decrease_quantum(self):
        if self.quantum > 0:
            self.quantum -= 1

    # if the instruction block is not cached, proceeds to load it.
    # Returns the instruction to be executed
    def get_instruction_to_execute(self, mem_add):
        # no se si quieren guardar como atributo de clase la instruccion que se esta ejecutando.
        if not self.instructionCache.get_if_mem_address_is_cached(mem_add):
            instruction_block = self.__cpu_instance.get_main_memory().get_instruction_block(mem_add)
            self.instructionCache.store_block_in_cache(StatesEnum.SHARED, mem_add, instruction_block)
        return self.instructionCache.get_block(self.instructionCache.get_block_index(mem_add)).get_instruction(mem_add)

    # Function to get a data block from main memory
    def get_data_block(self, mem_add):
        return self.__cpu_instance.get_main_memory().get_data_block(mem_add)

    def set_data_block_main_memory(self, mem_add, data_block):
        self.__cpu_instance.get_main_memory().set_data_block(mem_add, data_block)

    # If inc_pc is false, the pc is not incremented because it was already done by the instructions
    # beq, bne, jal and jalr
    def increment_PC_default(self):
        self.PC += 4

    # Used by beq, bne, jal and jalr to change where the PC should point
    def change_PC_by_instruction(self, mem_address_to_point):
        self.PC = mem_address_to_point

    def get_PC(self):
        return self.PC

    # Method to set the cycles that the core will have to wait to load next instruction and release the locks
    def set_instruction_system_clock_cycles(self, clock_cycles):
        self.__cycles += clock_cycles
        for i in range(0, clock_cycles):
            self.__cpu_instance.wait()

    # ***********************************************LOCKS***********************************************

    # Method to acquire the lock of the data memory bus
    def acquire_data_bus(self):
        if self.__cpu_instance.acquire__lock(0, self.__core_id):
            return True
        else:
            return False

    # Method to acquire the lock of the instruction memory bus
    def acquire_instruction_bus(self):
        if self.__cpu_instance.acquire__lock(1, self.__core_id):
            return True
        else:
            return False

    # Method to acquire the lock of self cache
    def acquire_self_cache(self):
        if self.__cpu_instance.acquire__lock(self.__core_id + 2, self.__core_id):
            return True
        else:
            return False

    # Method to acquire the lock of the other core cache
    def acquire_other_core_cache(self):
        if self.__core_id == 0:
            if self.__cpu_instance.acquire__lock(3, self.__core_id):
                return True
        else:
            if self.__cpu_instance.acquire__lock(2, self.__core_id):
                return True
        return False

    # Release locks methods
    def release_data_bus(self):
        # if self.__core_id == 0:
            # print("RELEASE lock: data bus core: " + str(self.__core_id))
        self.__cpu_instance.release_lock(0)

    def release_instruction_bus(self):
        # if self.__core_id == 0:
            # print("RELEASE lock: instruction bus core: " + str(self.__core_id))
        self.__cpu_instance.release_lock(1)

    def release_self_cache(self):
        # if self.__core_id == 0:
            # print("RELEASE lock: cache core: " + str(self.__core_id))
        self.__cpu_instance.release_lock(self.__core_id + 2)

    def release_other_core_cache(self):
        # if self.__core_id == 0:
            # print("RELEASE lock: other cache core: " + str(self.__core_id))
        if self.__core_id == 0:
            self.__cpu_instance.release_lock(3)
        else:
            self.__cpu_instance.release_lock(2)

    # Method to release all core acquired locks
    def release_all_locks_acquired(self):
        self.__cpu_instance.release_locks(self.__core_id)

    # Try to acquire other core cache, and the data bus
    def acquire_other_and_data_bus_locks(self):
        if self.acquire_other_core_cache():
            if self.acquire_data_bus():
                return True
            else:
                self.release_other_core_cache()
        return False

    # ********************************* GET/SET registers and caches *********************************

    # Method to get the value of the memory address on the cache
    def get_data_cache_value(self, memory_address):
        return self.data_cache.get_word_from_cached_block(memory_address)

    # Method to update a register value
    def set_register(self, register_index, register_value):
        self.register[register_index] = register_value

    # Method to get the register value, receives the register number x1 -> 1
    def get_register_value(self, register_number):
        return self.register[register_number]

    # *********************************************** CACHES ***********************************************

    # Method to change state of cache block
    def change_cache_block_state(self, memory_address, new_state):
        self.data_cache.change_block_state(memory_address, new_state)

    # Method to change the state on other core cache block, receives the memory address, and the new state
    def change_block_state_on_other_core_cache(self, memory_address, new_state):
        self.__cpu_instance.change_state_of_block_on_core_cache(not self.__core_id, memory_address, new_state)

    # Function to get if the memory_address block its stored on self cache
    def get_if_mem_address_is_on_self_cache(self, memory_address):
        if int(memory_address/16) == 16:
            print("")
        return self.data_cache.get_if_mem_address_is_cached(memory_address)

    # Function to get if the memory_address block its stored on other core cache
    def get_if_memory_address_on_other_cache(self, memory_address):
        return self.__cpu_instance.get_if_mem_address_is_on_core_cache(not self.__core_id, memory_address)

    # Function to get the state of the block with the memory address
    def get_memory_address_state_on_cache(self, memory_address):
        return self.data_cache.get_memory_address_block_state(memory_address)

    # Function to get the state of the block with the memory address on the other core cache
    def get_memory_address_state_on_other_cache(self, memory_address):
        return self.__cpu_instance.get_state_of_mem_address_on_core(not self.__core_id, memory_address)

    # ToDo revisar, por aquí anda el fallo
    # Method to store the block on the cache, returns the clock cycles to store
    def store_block_on_self_cache(self, state, memory_address, data_block):
        miss = False
        if not self.data_cache.get_if_mem_address_is_cached(memory_address):
            target_block_index = self.data_cache.get_target_block_index(memory_address)

            variable_prueba = self.data_cache.get_block_state(target_block_index)
            if variable_prueba == StatesEnum.MODIFIED:
                self.store_data_cache_block_on_main_mem(self.data_cache.get_block_address(target_block_index), state)
                miss = True
        self.data_cache.store_block_in_cache(state, memory_address, data_block)
        if miss:
            return 32
        else:
            return 0

    # ToDo revisar, no está haciendo nada
    # Method to store the cache block on main memory and change the block state
    def store_data_cache_block_on_main_mem(self, memory_address, cache_block_new_state):
        block_to_store = DataBlock(0)
        block_to_store.copy_data_block(self.data_cache.get_block_mem_address(memory_address))
        self.__cpu_instance.get_main_memory().set_data_block(memory_address, block_to_store)
        self.change_cache_block_state(memory_address, cache_block_new_state)
        return block_to_store

    # ToDo revisar, no está haciendo nada
    # Method to store a block on other core cache
    def store_other_core_data_cache_block_on_main_memory(self, memory_address, cache_block_new_state):
        return self.__cpu_instance.store_data_cache_block_on_mm_on_core(
            memory_address, cache_block_new_state, not self.__core_id)

    # Method to store a value in a data cache block with a memory address
    # Assumes that the block its on cache
    def change_word_value_data_cache(self, mem_address, value):
        self.data_cache.change_block_state(mem_address, StatesEnum.MODIFIED)
        self.data_cache.get_block_mem_address(mem_address).change_word_value(mem_address, value)

    # **********************************************RL**********************************************
    # Method to get the RL
    def get_self_rl(self):
        return self.RL

    # Method to invalidate RL core
    def invalidate_self_rl(self, mem_add):
        if self.RL == mem_add:
            self.RL = INVALID_RL_VALUE

    # Method to set the value of RL (for lr)
    def set_self_rl(self, mem_add):
        self.RL = mem_add

    # Method to invalidate RL on the other core
    def invalidate_other_core_rl(self, mem_add):
        self.__cpu_instance.invalidate_rl_on_core(mem_add, not self.__core_id)

    # Method to notify the CPU that the core execution ends
    def finish_execution(self):
        self.__cpu_instance.notify_core_finished()
        self.__finished = True
        self.__cpu_instance.kill_barrier()

    def get_data_cache(self):
        return self.data_cache

    def increase_cache_miss(self):
        self.__cpu_instance.get_simulation_statistics().getCoreStatistics(self.__core_id).increase_cache_miss()

    def increase_memory_access_hits(self):
        self.__cpu_instance.get_simulation_statistics().getCoreStatistics(self.__core_id).increase_memory_access_hits()

