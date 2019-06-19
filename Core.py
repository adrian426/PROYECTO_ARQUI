from Caches.Data2WACache import Data2WACache
from Caches.DataFACache import DataFACache
from DataMemory.DataBlock import DataBlock
from InstructionMemory.Instruction import Instruction
from Caches.InstructionsCache import InstructionsCache
from PCB import PCB
from threading import Thread
from Model.LW import LW


class Core(Thread):

    def __init__(self, cache_type: int, PCBStructure, cpu_instance, quantum_val):
        self.__core_id = cache_type
        self.__cpu_instance = cpu_instance

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

    def run(self):
        for iterator in range(0, 5):
            self.context_switch()
            self.__cpu_instance.wait(self.__core_id)

            instruction_to_execute = self.get_instruction_to_execute(self.PC)
            instruction_to_print  = str(self.hilillo_id) + " owner " + str(self.__core_id)
            print(instruction_to_print + " instruction " + instruction_to_execute.instruction_to_string())
            # Test to execute LW instruction
            # lw_exec = LW(self, instruction_to_execute)
            # print("Iteracion # ", iterator, "del nucleo # ", self.__core_id)

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
    def set_instruction_system_clock_cycles(self):
        pass
    # ToDo Se tiene que hacer un metodo que las instrucciones puedan llamar para indicarle al Core cuantos
    #  ciclos debe esperar para solicitar la siguiente instruccion y para liberar los candados

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
