from Caches.AbsCache import AbsCache
from StatesEnum import StatesEnum


#  2 way associative cache
class Data2WACache(AbsCache):

    fifo_index_way_0 = 0
    fifo_index_way_1 = 0

    def __init__(self, blockContent):
        AbsCache.__init__(self, blockContent)

    def get_if_mem_address_is_cached(self, memAdd):
        way = self.get_block_way(memAdd)
        addressRange = self.get_way_range(way)
        # if it's in the way 0, then addressRange is 0-3,
        #  3-7 otherwise
        for index in addressRange:
            if self.dataBlocksAddress[index] == int(memAdd/16):
                if self.get_block_state(index) != StatesEnum.INVALID:
                    return True
                else:
                    return False
        return False

    @staticmethod
    #  Returns the way assigned to the memory Address received as parameter.
    def get_block_way(memAdd):
        return int(memAdd / 16) % 2

    @staticmethod
    def get_way_range(way):
        if way == 0:
            return range(0,4)
        else:
            return range(4,8)

    def get_block_index(self, memAdd):
        way = self.get_block_way(memAdd)
        addressRange = self.get_way_range(way)
        for index in addressRange:
            if self.dataBlocksAddress[index] == int(memAdd / 16):
                return index

    def get_word_from_cached_block(self, memAdd):
        return self.dataBlocksLoaded[self.get_block_index(memAdd)].get_value(self.get_word_index(memAdd))

    def store_block_in_cache(self, state, memAdd, dataBlock):
        targetBlock = self.get_target_block_index(memAdd)
        if targetBlock > 3:
            way = 1
        else:
            way = 0
        self.dataBlocksLoaded[targetBlock] = dataBlock
        self.dataBlocksAddress[targetBlock] = int(memAdd/16) # Store the block address
        self.change_block_state(memAdd, state)
        self.augment_way_fifo_index(way)

    def augment_way_fifo_index(self, way):
        if way == 0:
            self.fifo_index_way_0 = (self.fifo_index_way_0 + 1) % 4
        else:
            self.fifo_index_way_1 = (self.fifo_index_way_1 + 1) % 4

    def get_target_block_index(self, memAdd):
        way = self.get_block_way(memAdd)
        if way == 0:
            return self.fifo_index_way_0
        else:
            return 4 + self.fifo_index_way_1

