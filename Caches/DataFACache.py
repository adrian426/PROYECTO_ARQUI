from Caches.AbsCache import AbsCache
from StatesEnum import StatesEnum


# fully associative cache
class DataFACache(AbsCache):

    def __init__(self, blockContent):
        AbsCache.__init__(self, blockContent)

    def get_if_mem_address_is_cached(self, memAdd):
        block_index = self.get_block_index(memAdd)
        if self.dataBlocksAddress[block_index] == int(memAdd/16):
            if self.get_block_state(block_index) != StatesEnum.INVALID:
                return True
        return False

    def get_block_index(self, memAdd):
        result = int(memAdd/16) % 8
        return result

    def get_word_from_cached_block(self, memAdd):
        return self.dataBlocksLoaded[self.get_block_index(memAdd)].get_value(self.get_word_index(memAdd))

    def store_block_in_cache(self, state, memAdd, dataBlock):
        targetBlock = self.get_block_index(memAdd)
        self.dataBlocksLoaded[targetBlock] = dataBlock
        self.dataBlocksAddress[targetBlock] = int(memAdd/16) #Stores the block address
        #memAdd - memAdd / 16 is used to know the address of the memory BLOCK using
        #the address of the data.
        self.change_block_state(memAdd, state)

    def get_target_block_index(self, memAdd):
        return self.get_block_index(memAdd)

    def print(self):
        for i in range(0, len(self.dataBlocksLoaded)):
            self.dataBlocksLoaded[i].print(self.dataBlocksAddress[i])
            print(self.dataBlocksState[i])