from queue import Queue

class PCBDataStructure:

    def __init__(self):
        self.availablePCBs = Queue()
        self.finishedPCBs = Queue()

    def queuePCB(self, PCB):
        self.availablePCBs.put(PCB, block=True)

    def queueFinishedPCB(self, PCB):
        self.finishedPCBs.put(PCB, block=True)

    def get_finished_pcb_queue(self):
        return self.finishedPCBs

    def dequeuePCB(self):
        self.availablePCBs.get(block=True)

    # Metodo para imprimir los pcbs
    def print_all_pcbs(self):
        pcb_list = list(self.availablePCBs.queue)
        for pcb in pcb_list:
            print("\n")
            pcb.print_pcb_data()
