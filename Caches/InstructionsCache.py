from Caches.AbsCache import AbsCache


# fully associative cache
class InstructionsCache(AbsCache):

    def __init__(self, blockContent):
        AbsCache.__init__(self, blockContent)

    def get_if_mem_address_is_cached(self, memAdd):
        if self.dataBlocksAddress[self.get_block_index(memAdd)] == (memAdd / 16).asType(int):
            return True
        return False

    def get_block_index(self, memAdd):
        return ((memAdd / 16) % 8).asType(int)

    # In this case, data is referring to the instruction
    def get_data_from_cached_block(self, memAdd):
        return self.dataBlocksLoaded[self.get_block_index(memAdd)][self.getDataIndex(memAdd)]

    def store_block_in_cache(self, state, memAdd, dataBlock):
        targetBlock = self.get_block_index(memAdd)
        self.dataBlocksLoaded[targetBlock] = dataBlock
        self.dataBlocksAddress[targetBlock] = (memAdd / 16).asType(int)  # Store the block address
        # memAdd - memAdd % 16 is used to know the address of the memory BLOCK using
        # the address of the data.
        self.changeBlockState(memAdd, state)

    def get_target_block_index(self, memAdd):
        return self.get_block_index(memAdd)