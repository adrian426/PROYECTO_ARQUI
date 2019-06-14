class PCB:
    hililloId = -1
    registers = []
    PCAddress = 0 #Address of the instruction where the PCB should start executing
    quantum = 0
    def __init__(self, theHilillo, address, assignedQuantum):
        self.hililloId = theHilillo
        self.registers = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.PCAddress = address
        self.quantum = assignedQuantum

    def alterRegisterValue(self, registerId, value):
        self.registers[registerId] = value

    def diminishQuantumValue(self):
        self.quantum -= 1;
