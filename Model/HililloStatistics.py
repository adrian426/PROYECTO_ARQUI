class HililloStatistics:

    def __init__(self, core_id, hilillo_id, registers, cycles, rl, runs):
        self.hilillo_id = hilillo_id
        self.core_id = core_id
        self.registers = registers
        self.cycles = cycles
        self.rl = rl
        self.runs = runs

    def add_cycles(self, cycles):
        self.cycles += cycles

    def add_runs(self, runs):
        self.runs += runs

    def get_cycles(self):
        return self.cycles

    def get_runs(self):
        return self.runs

    def print(self):
        print("Hilillo " + str(self.hilillo_id) + "\n Registros: ")
        for i in range(0, len(self.registers)):
            print("Registro " + str(i) + ": " + str(self.registers[i]))
        print("Ciclos totales: " + str(self.cycles))

    def get_id(self):
        return self.hilillo_id

