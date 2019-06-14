from AbsCache import AbsCache


class Data2WACache(AbsCache):

    dataBlock = [0,0,0,0]
    dataBlocksLoaded = [dataBlock, dataBlock, dataBlock, dataBlock, dataBlock, dataBlock, dataBlock, dataBlock]
    dataBlockAddresses = [-1, -1, -1, -1, -1, -1, -1, -1]
    dataBlocksState = ["U", "U", "U", "U", "U", "U", "U", "U"]
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

    def getBlockIndex(self, memAdd, way):
        addressRange = range((way * 4) - 1, (way * 4) + 3)
        for index in addressRange:
            if self.dataBlockAddresses[index] == memAdd / 16:
                return index

    def getDataFromCachedBlock(self, memAdd):
        way = self.getBlockWay(memAdd)
        return self.dataBlocksLoaded[self.getBlockIndex(memAdd,way)][self.getDataIndex(memAdd)]

    def storeDataBlockInCache(self, state, memAdd, dataBlock):
        targetBlock = -1
        way = self.getBlockWay(memAdd)
        if way == 0:
            targetBlock = self.fifo_index_way_0
        else:
            targetBlock = self.fifo_index_way_1
        self.dataBlocksLoaded[targetBlock] = dataBlock
        self.dataBlockAddresses[targetBlock] = memAdd/16 #Store the block address
        self.changeBlockState(memAdd, state)
        self.augmentWayFIFOIndex(way)

    def augmentWayFIFOIndex(self,way):
        if way == 0:
            self.fifo_index_way_0 = (self.fifo_index_way_0 + 1) % 4
        else:
            self.fifo_index_way_1 = (self.fifo_index_way_1 + 1) % 4






