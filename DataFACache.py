from AbsCache import AbsCache

class DataFACache():
    dataBlock = [0,0,0,0]
    dataBlocksLoaded = [dataBlock, dataBlock, dataBlock, dataBlock, dataBlock, dataBlock, dataBlock, dataBlock]
    dataBlockAddresses = [0, 0, 0, 0, 0, 0, 0, 0]
    dataBlocksState = ["I", "I", "I", "I", "I", "I", "I", "I"]

    def __init__(self):
        super.__init__()

    def getIfMemAddressIsCached(self, memAdd):
        if self.dataBlockAddresses[self.getBlockIndex(memAdd)] == (memAdd/16).asType(int):
            return True
        return False

    def getBlockIndex(self, memAdd):
        return ((memAdd/16) % 8).asType(int)

    def getDataFromCachedBlock(self, memAdd):
        return self.dataBlocksLoaded[self.getBlockIndex(memAdd)][self.getDataIndex(memAdd)]

    def storeBlockInCache(self, state, memAdd, dataBlock):
        targetBlock = self.getBlockIndex(memAdd)
        self.dataBlocksLoaded[targetBlock] = dataBlock
        self.dataBlockAddresses[targetBlock] = (memAdd/16).asType(int) #Store the block address
        #memAdd - memAdd % 16 is used to know the address of the memory BLOCK using
        #the address of the data.
        self.changeBlockState(memAdd, state)



