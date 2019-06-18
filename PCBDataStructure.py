from queue import Queue

class PCBDataStructure:
    availablePCBs = Queue()
    finishedPCBs = Queue()

    def __init__(self):
        pass

    def queuePCB(self, PCB):
        self.availablePCBs.put(PCB, block=True)

    def queueFinishedPCB(self, PCB):
        self.finishedPCBs.put(PCB, block=True)

    def dequeuePCB(self, PCB):
        self.availablePCBs.get(PCB, block=True)

    # Metodo para imprimir los pcbs
    def print_all_pcbs(self):
        pcb_list = list(self.availablePCBs.queue)
        for pcb in pcb_list:
            print("\n")
            pcb.print_pcb_data()
