from abc import ABC, abstractmethod

class AbsCache(ABC):

    @property
    @abstractmethod
    def dataBlock(self):
        #Should be an array with the content of each cached memory block.
        raise NotImplementedError


    @property
    @abstractmethod
    def dataBlocksLoaded(self):
        #Should be an array with the content of each cached memory block.
        raise NotImplementedError

    @property
    @abstractmethod
    def dataBlockAddresses(self):
        #Should be an array containing the address of each cached memory block
        raise NotImplementedError


    @property
    @abstractmethod
    def dataBlocksState(self):
        #Should be an array with the state of each cached memory block
        #States allowed should be the following:
        # "U" = Uncached.
        # "M" = Modified
        # "S" = Shared
        # "I" = Invalid
        raise NotImplementedError


    #Default builder, empty for now
    def __init__(self):
        super.__init__()

    #FOR ALL THE METHODS BELOW, memAdd SHOULD BE THE ADDRESS OF THE DATA,
    #NOT THE BLOCK ADDRESS.

    #Used to know if given a memory address, the related memory block is
    #loaded in cache.
    @abstractmethod
    def getIfMemAddresIsCached(self, memAdd):
        pass

    #Used to know if given a memory address, the related memory block is
    #loaded in cache. Should only be used if the block is known to be
    #in cache.
    @abstractmethod
    def getBlockIndex(self, memAdd):
        pass

    #Returns the index of the address inside a data block, ie, the index
    #in which the required data is stored in the data block
    @abstractmethod
    def getDataIndex(self, memAdd):
        return ((memAdd % 16) / 4).asType(int)

    @abstractmethod
    def getDataFromCachedBlock(self, memAdd):
        pass

    @abstractmethod
    def storeBlockInCache(self, state, memAdd, dataBlock):
        pass

    #Changes the state of the memory address in the cache.
    def changeBlockState(self, memAdd, state):
        self.dataBlocksState[self.getBlockIndex(memAdd)] = state
