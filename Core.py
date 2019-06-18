from Caches.Data2WACache import Data2WACache
from Caches.DataFACache import DataFACache
from DataMemory.DataBlock import DataBlock
from InstructionMemory.Instruction import Instruction
from Caches.InstructionsCache import InstructionsCache
from threading import Thread


class Core(Thread):

    def __init__(self, cache_type: int, PCBStructure):
        self.__cache_id = cache_type
        #se inicializa 32 registros en 0
        self.__registers = [0] * 32
        self.rl = 0
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

    def run(self):
        for iterator in range(1, 99):
            print("Iteracion # ", iterator, "del nucleo # ", self.__cache_id)






