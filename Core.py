from Caches.Data2WACache import Data2WACache
from Caches.DataFACache import DataFACache
from DataMemory.DataBlock import DataBlock
from InstructionMemory.Instruction import Instruction
from Caches.InstructionsCache import InstructionsCache
from PCB import PCB
from threading import Thread


class Core(Thread):

    def __init__(self, cache_type: int, PCBStructure, cpu_instance):
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
        self.quantum = 0

    def run(self):
        for iterator in range(0, 5):
            self.__cpu_instance.wait(self.__core_id)
            # print("Iteracion # ", iterator, "del nucleo # ", self.__core_id)



    # Loads the data from the pcb
    def load_pcb(self):
        pcb = self.__cpu_instance.get_pcb_ds().dequeuePCB()
        self.register = pcb.registers
        self.PC = pcb.PCAddress
        self.hilillo_id = pcb.hililloId

    def context_switch(self):
        # No se si se manda PC, depende donde se aumente.
        pcb = PCB(self.hilillo_id, self.PC, self.register)

        #if the quantum hasn't ended, the PCB is added again to the queue.
        if self.quantum != 0:
            self.__cpu_instance.queuePCB(pcb)
        else:
            self.__cpu_instance.queueFinishedPCB(pcb)
        # We call the pcb load function to load the next "hilillo" to execute
        self.load_pcb()
        self.load_pcb()

    def load_instruction(self, mem_add):
        if self.instructionCache.get_if_mem_address_is_cached(mem_add) == False:
            instructionBlock = self.__cpu_instance.get_main_memory()
            instructionBlock = instructionBlock.get_instruction_block(mem_add)
            self.instructionCache.store_block_in_cache("C", mem_add, instructionBlock)


