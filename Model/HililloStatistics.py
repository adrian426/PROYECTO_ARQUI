class HililloStatistics:

    def __init__(self, core_id, hilillo_id, registers, cycles):
        self.hilillo_id = hilillo_id
        self.core_id = core_id
        self.registers = registers
        self.cycles = cycles

    def add_cycles(self, cycles):
        self.cycles += cycles

    def get_cycles(self, cycles):
        self.cycles += cycles

    def print(self):
        print("Hilillo " + self.id + "\n Registros: ")
        for index, value in self.registers:
            print("Registro " + str(index) + ": " + str(value))
        print("Ciclos totales: " + str(self.cycles))

    def get_id(self):
        return self.hilillo_id

