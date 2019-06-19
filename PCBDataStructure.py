from queue import Queue


class PCBDataStructure:

    def __init__(self):
        self.availablePCBs = Queue()
        self.finishedPCBs = Queue()
        self.count = 0

    def queuePCB(self, PCB):
        self.availablePCBs.put(PCB, block=True)
        self.count += 1

    def queueFinishedPCB(self, PCB):
        self.finishedPCBs.put(PCB, block=True)

    def get_finished_pcb_queue(self):
        return self.finishedPCBs

    def dequeuePCB(self):
        pcb = self.availablePCBs.get(block=True)
        self.count -= 1
        return pcb

    def get_count(self):
        return self.count

    # Metodo para imprimir los pcbs
    def print_all_pcbs(self):
        pcb_list = list(self.availablePCBs.queue)
        for pcb in pcb_list:
            print("\n")
            pcb.print_pcb_data()
