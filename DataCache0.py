from AbsCache import AbsCache

# Fully associative cache
class DataCache0(AbsCache):

    dataBlock = [0,0,0,0]
    dataBlocksLoaded = [dataBlock, dataBlock, dataBlock, dataBlock, dataBlock, dataBlock, dataBlock, dataBlock]
    dataBlockAddresses = [-1, -1, -1, -1, -1, -1, -1, -1]
    dataBlocksState = ["U", "U", "U", "U", "U", "U", "U", "U"]
    def __init__(self):
        super.__init__()

    def getIfMemAddressIsCached(self, memAdd):
        if self.dataBlockAddresses[self.getBlockIndex(memAdd)] == memAdd/16:
            return True
        else:
            return False

    def getBlockIndex(self, memAdd):
        return ((memAdd/16) % 8).asType(int)

    def getDataFromCachedBlock(self, memAdd):
        return self.dataBlocksLoaded[self.getBlockIndex(memAdd)][self.getDataIndex(memAdd)]

    def storeDataBlockInCache(self, state, memAdd, dataBlock):
        targetBlock = self.getBlockIndex(memAdd)
        self.dataBlocksLoaded[targetBlock] = dataBlock
        self.dataBlockAddresses[targetBlock] = memAdd - (memAdd % 16) #Store the block address
        self.changeBlockState(memAdd, state)





