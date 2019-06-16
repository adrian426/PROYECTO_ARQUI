from Caches.Data2WACache import Data2WACache
from Caches.DataFACache import DataFACache
from DataMemory.DataBlock import DataBlock
from InstructionMemory.Instruction import Instruction
from Caches.InstructionsCache import InstructionsCache


class Core:

    def __init__(self, cacheType: int, PCBStructure):
        dataBlock = DataBlock(0)
        if cacheType == 0:
            self.dataCache = Data2WACache(dataBlock)
        elif cacheType == 1:
            self.dataCache = DataFACache(dataBlock)
        else:
            raise TypeError("Unknown Value for cache type.")
        instruction = Instruction.__init__()
        instruction.set_instruction_values([0, 0, 0, 0])
        self.instructionCache = InstructionsCache(instruction)





