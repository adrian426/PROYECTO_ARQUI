from abc import ABC, abstractmethod


class AbsCache(ABC):

    def __init__(self, blockContents):
        self.dataBlocksLoaded = []
        self.dataBlocksAddress = []
        self.dataBlocksState = []
        for i in range(0, 7):
            self.dataBlocksLoaded.extend(blockContents)
            self.dataBlockAddresses.extend(0)
            self.dataBlocksState.extend("I")
        super.__init__()

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
    def get_data_from_cached_block(self, memAdd):
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
    def get_data_index(memAdd):
        return ((memAdd % 16) / 4).asType(int)

    @staticmethod
    def get_block_state(self, index):
        return self.dataBlocksState[index]

    def get_block_address(self, index):
        return self.dataBlocksAddress[index]

    def get_block(self, index):
        return self.dataBlocksLoaded[index]

    # Changes the state of the memory address in the cache.
    def change_block_state(self, memAdd, state):
        self.dataBlocksState[self.getBlockIndex(memAdd)] = state
