class PCB:

    def __init__(self, theHilillo, address, registers):
        self.hililloId = theHilillo
        self.registers = registers
        self.PCAddress = address

    def alterRegisterValue(self, registerId, value):
        self.registers[registerId] = value


    # Metodo para imprimir el pcb
    def print_pcb_data(self):
        print("Hilillo : " + self.hililloId)
        print("Registros : " + str(self.registers))
        print("DirMem : " + str(self.PCAddress))
