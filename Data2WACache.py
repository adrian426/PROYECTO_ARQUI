from AbsCache import AbsCache

class Data2WACache(AbsCache):

    dataBlock = [0,0,0,0]
    dataBlocksLoaded = [dataBlock, dataBlock, dataBlock, dataBlock, dataBlock, dataBlock, dataBlock, dataBlock]
    dataBlockAddresses = [0, 0, 0, 0, 0, 0, 0, 0]
    dataBlocksState = ["I", "I", "I", "I", "I", "I", "I", "I"]
    fifo_index_way_0 = 0
    fifo_index_way_1 = 0

    def __init__(self):
        super.__init__()

    def getIfMemAddressIsCached(self, memAdd, way):
        addressRange = range((way*4)-1, (way*4)+3)
        #if it's in the way 0, then addressRange is 0-3,
        # 3-7 otherwise
        for index in addressRange:
            if self.dataBlockAddresses[index] == memAdd/16:
                return True
        return False

    # Returns the way assigned to the memory Address received as parameter.
    def getBlockWay(self, memAdd):
        return (memAdd % 16) / 2

    def getWayRange(self, way):
        if way == 0:
            return range(0,3)
        else:
            return range(4,7)

    def getBlockIndex(self, memAdd, way):
        addressRange = self.getWayRange(way)
        for index in addressRange:
            if self.dataBlockAddresses[index] == memAdd / 16:
                return index

    def getDataFromCachedBlock(self, memAdd):
        way = self.getBlockWay(memAdd)
        return self.dataBlocksLoaded[self.getBlockIndex(memAdd,way)][self.getDataIndex(memAdd)]

    def storeDataBlockInCache(self, state, memAdd, dataBlock):
        targetBlock, way = self.getTargetBlockIndex(memAdd)
        self.dataBlocksLoaded[targetBlock] = dataBlock
        self.dataBlockAddresses[targetBlock] = memAdd/16 #Store the block address
        self.changeBlockState(memAdd, state)
        self.augmentWayFIFOIndex(way)

    def augmentWayFIFOIndex(self,way):
        if way == 0:
            self.fifo_index_way_0 = (self.fifo_index_way_0 + 1) % 4
        else:
            self.fifo_index_way_1 = (self.fifo_index_way_1 + 1) % 4

    def getTargetBlockIndex(self,memAdd):
        way = self.getBlockWay(memAdd)
        if way == 0:
            return self.fifo_index_way_0, way
        else:
            return 4 + self.fifo_index_way_1, way



