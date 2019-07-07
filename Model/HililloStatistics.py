class HililloStatistics:

    def __init__(self, core_id, hilillo_id, registers, cycles, rl, runs):
        self.hilillo_id = hilillo_id
        self.core = [0, 0]
        self.core[core_id] = runs
        self.registers = registers
        self.cycles = cycles
        self.rl = rl

    def add_cycles(self, cycles):
        self.cycles += cycles

    def add_runs(self, core):
        self.core[0] += core[0]
        self.core[1] += core[1]

    def get_cycles(self):
        return self.cycles

    def print(self):
        print("\nHilillo: "+ str(self.hilillo_id) + "\n----------------")
        print("Corridas \ncore 0: " + str(self.core[0]) + "\ncore 1 : " + str(self.core[1]))
        print("\nCiclos totales: " + str(self.cycles))
        print("\nRegistros: ")
        print("RL: " + str(self.rl))
        for i in range(0, len(self.registers)):
            print("R" + str(i) + ": " + str(self.registers[i]))

    def get_id(self):
        return self.hilillo_id

