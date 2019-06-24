from abc import ABC, abstractmethod


class AbsCache(ABC):

    def __init__(self, blockContents):
        self.dataBlocksLoaded = []
        self.dataBlocksAddress = []
        self.dataBlocksState = []
        for i in range(0, 8):
            self.dataBlocksLoaded.append(blockContents)
            self.dataBlocksAddress.append(0)
            self.dataBlocksState.extend("I")
        # super.__init__()

    # FOR ALL THE METHODS BELOW, memAdd SHOULD BE THE ADDRESS OF THE DATA,
    # NOT THE BLOCK ADDRESS.

    # Used to know if given a memory address, the related memory block is
    # loaded in cache.
    @abstractmethod
    def get_if_mem_address_is_cached(self, memAdd):
        pass

    # Used to know if given a memory address, the related memory block is
    # loaded in cache. Should only be used if the block is known to be
    # in cache.
    @abstractmethod
    def get_block_index(self, memAdd):
        pass

    @abstractmethod
    def get_word_from_cached_block(self, memAdd):
        pass

    @abstractmethod
    def store_block_in_cache(self, state, memAdd, dataBlock):
        pass

    @abstractmethod
    # The definition of this method is different only for the 2WA cache.
    def get_target_block_index(self, memAdd):
        pass

    @staticmethod
    # Returns the index of the address inside a data block, ie, the index
    # in which the required data is stored in the data block
    def get_word_index(memAdd):
        return int((memAdd % 16) / 4)

    def get_block_state(self, index):
        return self.dataBlocksState[index]

    # Returns the state of the block that contains the memory address value
    def get_memory_address_block_state(self, memory_address):
        return self.dataBlocksState[self.get_block_index(memory_address)]

    def get_block_address(self, index):
        return self.dataBlocksAddress[index]

    def get_block(self, index):
        return self.dataBlocksLoaded[index]

    # Changes the state of the memory address in the cache.
    def change_block_state(self, memAdd, state):
        self.dataBlocksState[self.get_block_index(memAdd)] = state

    # Method to get the data block
    def get_block_mem_address(self, mem_add):
        return self.get_block(self.get_block_index(mem_add))
