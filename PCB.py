class PCB:
    hililloId = -1
    registers = []
    PCAddress = 0 #Address of the instruction where the PCB should start executing

    def __init__(self, theHilillo, address, registers):
        self.hililloId = theHilillo
        self.registers = registers
        self.PCAddress = address

    def alterRegisterValue(self, registerId, value):
        self.registers[registerId] = value
